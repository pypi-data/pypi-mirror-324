use super::{Diff, Printer};
use crate::lang::SgLang;
use ast_grep_config::{RuleConfig, Severity};
use ast_grep_core::DisplayContext;

use ansi_term::{Color, Style};
use anyhow::Result;
use clap::ValueEnum;
use codespan_reporting::diagnostic::{self, Diagnostic, Label};
use codespan_reporting::files::SimpleFile;
use codespan_reporting::term::termcolor::{ColorChoice, StandardStream, WriteColor};
use codespan_reporting::term::{self, DisplayStyle};
use similar::{ChangeTag, DiffOp, TextDiff};

use std::borrow::Cow;
use std::fmt::Display;
use std::io::Write;
use std::path::Path;

mod test;

use ast_grep_core::{NodeMatch as SgNodeMatch, StrDoc};
type NodeMatch<'a, L> = SgNodeMatch<'a, StrDoc<L>>;

// add this macro because neither trait_alias nor type_alias_impl is supported.
macro_rules! Matches {
  ($lt: lifetime) => { impl Iterator<Item = NodeMatch<$lt, SgLang>> };
}
macro_rules! Diffs {
  ($lt: lifetime) => { impl Iterator<Item = Diff<$lt>> };
}

#[derive(Clone, Copy, ValueEnum)]
pub enum ReportStyle {
  /// Output a richly formatted diagnostic, with source code previews.
  Rich,
  /// Output a condensed diagnostic, with a line number, severity, message and notes (if any).
  Medium,
  /// Output a short diagnostic, with a line number, severity, and message.
  Short,
}

#[derive(Clone, Copy, ValueEnum)]
pub enum Heading {
  /// Print heading for terminal tty but not for piped output
  Auto,
  /// Always print heading regardless of output type.
  Always,
  /// Never print heading regardless of output type.
  Never,
}

impl Heading {
  fn should_print(&self) -> bool {
    use Heading as H;
    match self {
      H::Always => true,
      H::Never => false,
      H::Auto => atty::is(atty::Stream::Stdout),
    }
  }
}

pub struct ColoredPrinter<W: WriteColor> {
  writer: W,
  config: term::Config,
  styles: PrintStyles,
  heading: Heading,
  context: (u16, u16),
}
impl ColoredPrinter<StandardStream> {
  pub fn stdout<C: Into<ColorChoice>>(color: C) -> Self {
    let color = color.into();
    ColoredPrinter::new(StandardStream::stdout(color)).color(color)
  }
}

impl<W: WriteColor> ColoredPrinter<W> {
  pub fn new(writer: W) -> Self {
    Self {
      writer,
      styles: PrintStyles::from(ColorChoice::Auto),
      config: term::Config::default(),
      heading: Heading::Auto,
      context: (0, 0),
    }
  }

  pub fn color<C: Into<ColorChoice>>(mut self, color: C) -> Self {
    let color = color.into();
    self.styles = PrintStyles::from(color);
    self
  }

  pub fn style(mut self, style: ReportStyle) -> Self {
    let display_style = match style {
      ReportStyle::Rich => DisplayStyle::Rich,
      ReportStyle::Medium => DisplayStyle::Medium,
      ReportStyle::Short => DisplayStyle::Short,
    };
    self.config.display_style = display_style;
    self
  }

  pub fn heading(mut self, heading: Heading) -> Self {
    self.heading = heading;
    self
  }

  pub fn context(mut self, context: (u16, u16)) -> Self {
    self.context = context;
    self.config.start_context_lines = context.0 as usize;
    self.config.end_context_lines = context.1 as usize;
    self
  }

  fn context_span(&self) -> usize {
    (self.context.0 + self.context.1) as usize
  }

  fn diff_context(&self) -> usize {
    if self.context.0 == 0 {
      3
    } else {
      self.context.0 as usize
    }
  }
}

impl<W: WriteColor> Printer for ColoredPrinter<W> {
  fn print_rule<'a>(
    &mut self,
    matches: Matches!('a),
    file: SimpleFile<Cow<str>, &String>,
    rule: &RuleConfig<SgLang>,
  ) -> Result<()> {
    let config = &self.config;
    let writer = &mut self.writer;
    let severity = match rule.severity {
      Severity::Error => diagnostic::Severity::Error,
      Severity::Warning => diagnostic::Severity::Warning,
      Severity::Info => diagnostic::Severity::Note,
      Severity::Hint => diagnostic::Severity::Help,
      Severity::Off => unreachable!("turned-off rule should not have match."),
    };
    for m in matches {
      let range = m.range();
      let mut labels = vec![Label::primary((), range)];
      if let Some(secondary_nodes) = m.get_env().get_labels("secondary") {
        labels.extend(secondary_nodes.iter().map(|n| {
          let range = n.range();
          Label::secondary((), range)
        }));
      }
      let diagnostic = Diagnostic::new(severity)
        .with_code(&rule.id)
        .with_message(rule.get_message(&m))
        .with_notes(rule.note.iter().cloned().collect())
        .with_labels(labels);
      term::emit(&mut *writer, config, &file, &diagnostic)?;
    }
    Ok(())
  }

  fn print_matches<'a>(&mut self, matches: Matches!('a), path: &Path) -> Result<()> {
    if self.heading.should_print() {
      print_matches_with_heading(matches, path, self)
    } else {
      print_matches_with_prefix(matches, path, self)
    }
  }

  fn print_diffs<'a>(&mut self, diffs: Diffs!('a), path: &Path) -> Result<()> {
    let context = self.diff_context();
    let writer = &mut self.writer;
    print_diffs(diffs, path, &self.styles, writer, context)
  }
  fn print_rule_diffs(
    &mut self,
    diffs: Vec<(Diff<'_>, &RuleConfig<SgLang>)>,
    path: &Path,
  ) -> Result<()> {
    let context = self.diff_context();
    let writer = &mut self.writer;
    let mut start = 0;
    print_prelude(path, &self.styles, writer)?;
    for (diff, rule) in diffs {
      let range = &diff.range;
      // skip overlapping diff
      if range.start < start {
        continue;
      }
      start = range.end;
      print_rule_title(rule, &diff.node_match, &self.styles.rule, writer)?;
      let source = diff.get_root_text();
      let new_str = format!(
        "{}{}{}",
        &source[..range.start],
        diff.replacement,
        &source[start..],
      );
      print_diff(source, &new_str, &self.styles, writer, context)?;
      if let Some(note) = &rule.note {
        writeln!(writer, "{}", self.styles.rule.note.paint("Note:"))?;
        writeln!(writer, "{note}")?;
      }
    }
    Ok(())
  }
}

fn print_rule_title<W: WriteColor>(
  rule: &RuleConfig<SgLang>,
  nm: &NodeMatch<SgLang>,
  style: &RuleStyle,
  writer: &mut W,
) -> Result<()> {
  let (level, level_style) = match rule.severity {
    Severity::Error => ("error", style.error),
    Severity::Warning => ("warning", style.warning),
    Severity::Info => ("note", style.info),
    Severity::Hint => ("help", style.hint),
    Severity::Off => unreachable!("turned-off rule should not have match."),
  };
  let header = format!("{level}[{}]:", &rule.id);
  let header = level_style.paint(header);
  let message = style.message.paint(rule.get_message(nm));
  writeln!(writer, "{header} {message}")?;
  Ok(())
}

#[cfg(not(target_os = "windows"))]
fn adjust_dir_separator(p: &Path) -> Cow<str> {
  p.to_string_lossy()
}

// change \ to / on windows
#[cfg(target_os = "windows")]
fn adjust_dir_separator(p: &Path) -> String {
  const VERBATIM_PREFIX: &str = r#"\\?\"#;
  let p = p.display().to_string();
  if p.starts_with(VERBATIM_PREFIX) {
    p[VERBATIM_PREFIX.len()..].to_string()
  } else {
    p
  }
}

fn print_prelude(path: &Path, styles: &PrintStyles, writer: &mut impl Write) -> Result<()> {
  let filepath = adjust_dir_separator(path);
  writeln!(writer, "{}", styles.file_path.paint(filepath))?;
  Ok(())
}

// merging overlapping/adjacent matches
// adjacent matches: matches that starts or ends on the same line
struct MatchMerger<'a> {
  last_start_line: usize,
  last_end_line: usize,
  last_trailing: &'a str,
  last_end_offset: usize,
  context: (u16, u16),
}

impl<'a> MatchMerger<'a> {
  fn new(nm: &NodeMatch<'a, SgLang>, (before, after): (u16, u16)) -> Self {
    let display = nm.display_context(before as usize, after as usize);
    let last_start_line = display.start_line + 1;
    let last_end_line = nm.end_pos().line() + 1;
    let last_trailing = display.trailing;
    let last_end_offset = nm.range().end;
    Self {
      last_start_line,
      last_end_line,
      last_end_offset,
      last_trailing,
      context: (before, after),
    }
  }

  // merge non-overlapping matches but start/end on the same line
  fn merge_adjacent(&mut self, nm: &NodeMatch<'a, SgLang>) -> Option<usize> {
    let display = self.display(nm);
    let start_line = display.start_line;
    if start_line <= self.last_end_line + self.context.1 as usize {
      let last_end_offset = self.last_end_offset;
      self.last_end_offset = nm.range().end;
      self.last_trailing = display.trailing;
      Some(last_end_offset)
    } else {
      None
    }
  }

  fn conclude_match(&mut self, nm: &NodeMatch<'a, SgLang>) {
    let display = self.display(nm);
    self.last_start_line = display.start_line + 1;
    self.last_end_line = nm.end_pos().line() + 1;
    self.last_trailing = display.trailing;
    self.last_end_offset = nm.range().end;
  }

  #[inline]
  fn check_overlapping(&self, nm: &NodeMatch<'a, SgLang>) -> bool {
    let range = nm.range();

    // merge overlapping matches.
    // N.B. range.start == last_end_offset does not mean overlapping
    if range.start < self.last_end_offset {
      // guaranteed by pre-order
      debug_assert!(range.end <= self.last_end_offset);
      true
    } else {
      false
    }
  }

  fn display(&self, nm: &NodeMatch<'a, SgLang>) -> DisplayContext<'a> {
    let (before, after) = self.context;
    nm.display_context(before as usize, after as usize)
  }
}

fn print_matches_with_heading<'a, W: WriteColor>(
  mut matches: Matches!('a),
  path: &Path,
  printer: &mut ColoredPrinter<W>,
) -> Result<()> {
  let styles = &printer.styles;
  let context_span = printer.context_span();
  let writer = &mut printer.writer;
  print_prelude(path, styles, writer)?;
  let Some(first_match) = matches.next() else {
    return Ok(());
  };
  let source = first_match.root().get_text();

  let mut merger = MatchMerger::new(&first_match, printer.context);

  let display = merger.display(&first_match);
  let mut ret = display.leading.to_string();
  styles.push_matched_to_ret(&mut ret, &display.matched)?;

  for nm in matches {
    if merger.check_overlapping(&nm) {
      continue;
    }
    let display = merger.display(&nm);
    // merge adjacent matches
    if let Some(last_end_offset) = merger.merge_adjacent(&nm) {
      ret.push_str(&source[last_end_offset..nm.range().start]);
      styles.push_matched_to_ret(&mut ret, &display.matched)?;
      continue;
    }
    ret.push_str(merger.last_trailing);
    let lines = ret.lines().count();
    let mut num = merger.last_start_line;
    let width = (lines + num).checked_ilog10().unwrap_or(0) as usize + 1;
    let line_num = styles.line_num.paint(format!("{num}"));
    write!(writer, "{line_num:>width$}│")?; // initial line num
    print_highlight(ret.lines(), width, &mut num, writer, styles)?;
    writeln!(writer)?; // end match new line
    if context_span > 0 {
      writeln!(writer, "{:╴>width$}┤", "")?; // make separation
    }
    merger.conclude_match(&nm);
    ret = display.leading.to_string();
    styles.push_matched_to_ret(&mut ret, &display.matched)?;
  }
  ret.push_str(merger.last_trailing);
  let lines = ret.lines().count();
  let mut num = merger.last_start_line;
  let width = (lines + num).checked_ilog10().unwrap_or(0) as usize + 1;
  let line_num = styles.line_num.paint(format!("{num}"));
  write!(writer, "{line_num:>width$}│")?; // initial line num
  print_highlight(ret.lines(), width, &mut num, writer, styles)?;
  writeln!(writer)?; // end match new line
  writeln!(writer)?; // end
  Ok(())
}

fn print_matches_with_prefix<'a, W: WriteColor>(
  mut matches: Matches!('a),
  path: &Path,
  printer: &mut ColoredPrinter<W>,
) -> Result<()> {
  let styles = &printer.styles;
  let context_span = printer.context_span();
  let writer = &mut printer.writer;
  let path = path.display();
  let Some(first_match) = matches.next() else {
    return Ok(());
  };
  let source = first_match.root().get_text();

  let mut merger = MatchMerger::new(&first_match, printer.context);
  let display = merger.display(&first_match);
  let mut ret = display.leading.to_string();
  styles.push_matched_to_ret(&mut ret, &display.matched)?;
  for nm in matches {
    if merger.check_overlapping(&nm) {
      continue;
    }
    let display = merger.display(&nm);
    // merge adjacent matches
    if let Some(last_end_offset) = merger.merge_adjacent(&nm) {
      ret.push_str(&source[last_end_offset..nm.range().start]);
      styles.push_matched_to_ret(&mut ret, &display.matched)?;
      continue;
    }
    ret.push_str(merger.last_trailing);
    for (n, line) in ret.lines().enumerate() {
      let num = merger.last_start_line + n;
      writeln!(writer, "{path}:{num}:{line}")?;
    }
    if context_span > 0 {
      writeln!(writer, "--")?; // make separation
    }
    merger.conclude_match(&nm);
    ret = display.leading.to_string();
    styles.push_matched_to_ret(&mut ret, &display.matched)?;
  }
  ret.push_str(merger.last_trailing);
  for (n, line) in ret.lines().enumerate() {
    let num = merger.last_start_line + n;
    writeln!(writer, "{path}:{num}:{line}")?;
  }
  Ok(())
}

fn print_diffs<'a, W: WriteColor>(
  mut diffs: Diffs!('a),
  path: &Path,
  styles: &PrintStyles,
  writer: &mut W,
  context: usize,
) -> Result<()> {
  print_prelude(path, styles, writer)?;
  let Some(first_diff) = diffs.next() else {
    return Ok(());
  };
  let source = first_diff.get_root_text();
  let range = first_diff.range;
  let mut start = range.end;
  let mut new_str = format!("{}{}", &source[..range.start], first_diff.replacement);
  for diff in diffs {
    let range = diff.range;
    // skip overlapping diff
    if range.start < start {
      continue;
    }
    new_str.push_str(&source[start..range.start]);
    new_str.push_str(&diff.replacement);
    start = range.end;
  }
  new_str.push_str(&source[start..]);
  print_diff(source, &new_str, styles, writer, context)?;
  Ok(())
}

fn print_highlight<'a, W: Write>(
  mut lines: impl Iterator<Item = &'a str>,
  width: usize,
  num: &mut usize,
  writer: &mut W,
  styles: &PrintStyles,
) -> Result<()> {
  if let Some(line) = lines.next() {
    write!(writer, "{line}")?;
  }
  for line in lines {
    writeln!(writer)?;
    *num += 1;
    let line_num = styles.line_num.paint(format!("{num}"));
    write!(writer, "{line_num:>width$}│{line}")?;
  }
  Ok(())
}

fn index_display(index: Option<usize>, style: Style, width: usize) -> impl Display {
  let index_str = match index {
    None => format!("{:width$}", ""),
    Some(idx) => format!("{:<width$}", idx + 1), // 0-based index -> 1-based line num
  };
  style.paint(index_str)
}

// TODO: currently diff print context is three lines before/after the match.
// This is suboptimal. We should use function/class as the enclosing scope to print relevant lines. See #155
fn compute_header(group: &[DiffOp]) -> String {
  let old_start = group[0].old_range().start;
  let new_start = group[0].new_range().start;
  let (old_len, new_len) = group.iter().fold((0, 0), |(o, n), op| {
    (o + op.old_range().len(), n + op.new_range().len())
  });
  format!(
    "@@ -{},{} +{},{} @@",
    old_start, old_len, new_start, new_len
  )
}

pub fn print_diff(
  old: &str,
  new: &str,
  styles: &PrintStyles,
  writer: &mut impl Write,
  context: usize,
) -> Result<()> {
  let diff = TextDiff::from_lines(old, new);
  for group in diff.grouped_ops(context) {
    let op = group.last().unwrap();
    let old_width = op.old_range().end.checked_ilog10().unwrap_or(0) as usize + 1;
    let new_width = op.new_range().end.checked_ilog10().unwrap_or(0) as usize + 1;
    let header = compute_header(&group);
    writeln!(writer, "{}", Color::Blue.paint(header))?;
    for op in group {
      for change in diff.iter_inline_changes(&op) {
        let (sign, s, em, line_num) = match change.tag() {
          ChangeTag::Delete => ("-", styles.delete, styles.delete_emphasis, styles.delete),
          ChangeTag::Insert => ("+", styles.insert, styles.insert_emphasis, styles.insert),
          ChangeTag::Equal => (" ", Style::new(), Style::new(), styles.line_num),
        };
        write!(
          writer,
          "{} {}│{}",
          index_display(change.old_index(), line_num, old_width),
          index_display(change.new_index(), line_num, new_width),
          s.paint(sign),
        )?;
        for (emphasized, value) in change.iter_strings_lossy() {
          if emphasized {
            write!(writer, "{}", em.paint(value))?;
          } else {
            write!(writer, "{}", s.paint(value))?;
          }
        }
        if change.missing_newline() {
          writeln!(writer)?;
        }
      }
    }
  }
  Ok(())
}

// warn[rule-id]: rule message here.
// |------------|------------------|
//    header            message
#[derive(Default)]
struct RuleStyle {
  // header style
  error: Style,
  warning: Style,
  info: Style,
  hint: Style,
  // message style
  message: Style,
  note: Style,
}

// TODO: use termcolor instead
#[derive(Default)]
pub struct PrintStyles {
  // print match color
  file_path: Style,
  matched: Style,
  line_num: Style,
  // diff insert style
  insert: Style,
  insert_emphasis: Style,
  // diff deletion style
  delete: Style,
  delete_emphasis: Style,
  rule: RuleStyle,
}

impl PrintStyles {
  fn colored() -> Self {
    static THISTLE1: Color = Color::Fixed(225);
    static SEA_GREEN: Color = Color::Fixed(158);
    static RED: Color = Color::Fixed(161);
    static GREEN: Color = Color::Fixed(35);
    let insert = Style::new().fg(GREEN);
    let delete = Style::new().fg(RED);
    Self {
      file_path: Color::Cyan.italic(),
      matched: Color::Red.bold(),
      line_num: Style::new().dimmed(),
      insert,
      insert_emphasis: insert.on(SEA_GREEN).bold(),
      delete,
      delete_emphasis: delete.on(THISTLE1).bold(),
      rule: RuleStyle {
        error: Color::Red.bold(),
        warning: Color::Yellow.bold(),
        info: Style::new().bold(),
        hint: Style::new().dimmed().bold(),
        note: Style::new().italic(),
        message: Style::new().bold(),
      },
    }
  }
  fn no_color() -> Self {
    Self::default()
  }

  fn push_matched_to_ret(&self, ret: &mut String, matched: &str) -> Result<()> {
    use std::fmt::Write;
    // TODO: use intersperse
    let mut lines = matched.lines();
    if let Some(line) = lines.next() {
      write!(ret, "{}", self.matched.paint(line))?;
    } else {
      return Ok(());
    }
    for line in lines {
      ret.push('\n');
      write!(ret, "{}", self.matched.paint(line))?;
    }
    Ok(())
  }
}
impl From<ColorChoice> for PrintStyles {
  fn from(color: ColorChoice) -> Self {
    if choose_color::should_use_color(&color) {
      Self::colored()
    } else {
      Self::no_color()
    }
  }
}

// copied from termcolor
pub(crate) mod choose_color {
  use super::ColorChoice;
  use std::env;
  /// Returns true if we should attempt to write colored output.
  pub fn should_use_color(color: &ColorChoice) -> bool {
    match *color {
      // TODO: we should check if ansi is supported on windows console
      ColorChoice::Always => true,
      ColorChoice::AlwaysAnsi => true,
      ColorChoice::Never => false,
      // NOTE tty check is added
      ColorChoice::Auto => atty::is(atty::Stream::Stdout) && env_allows_color(),
    }
  }

  fn env_allows_color() -> bool {
    match env::var_os("TERM") {
      // On Windows, if TERM isn't set, then we should not automatically
      // assume that colors aren't allowed. This is unlike Unix environments
      None => {
        if !cfg!(windows) {
          return false;
        }
      }
      Some(k) => {
        if k == "dumb" {
          return false;
        }
      }
    }
    // If TERM != dumb, then the only way we don't allow colors at this
    // point is if NO_COLOR is set.
    if env::var_os("NO_COLOR").is_some() {
      return false;
    }
    true
  }
}
