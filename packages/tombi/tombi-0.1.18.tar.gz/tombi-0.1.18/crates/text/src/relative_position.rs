use std::{
    cmp::Ordering,
    ops::{Add, AddAssign},
};

use crate::{Column, Line};

#[derive(Default, Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub struct RelativePosition {
    pub(crate) line: Line,
    pub(crate) column: Column,
}

impl RelativePosition {
    pub fn of(text: &str) -> Self {
        let mut line = 0;
        let mut column = 0;
        for c in text.chars() {
            if c == '\n' {
                line += 1;
                column = 0;
            } else {
                column += 1;
            }
        }
        Self { line, column }
    }

    #[inline]
    pub fn line(&self) -> Line {
        self.line
    }

    #[inline]
    pub fn column(&self) -> Column {
        self.column
    }
}

impl Ord for RelativePosition {
    fn cmp(&self, other: &Self) -> Ordering {
        self.line
            .cmp(&other.line)
            .then_with(|| self.column.cmp(&other.column))
    }
}

impl PartialOrd for RelativePosition {
    #[inline]
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl From<(Line, Column)> for RelativePosition {
    #[inline]
    fn from((line, column): (Line, Column)) -> Self {
        Self { line, column }
    }
}

impl From<char> for RelativePosition {
    #[inline]
    fn from(c: char) -> Self {
        if c == '\n' {
            Self { line: 1, column: 0 }
        } else {
            Self { line: 0, column: 1 }
        }
    }
}

impl Add for RelativePosition {
    type Output = RelativePosition;

    #[inline]
    fn add(self, rhs: RelativePosition) -> Self::Output {
        Self {
            line: self.line + rhs.line(),
            column: rhs.column(),
        }
    }
}

impl AddAssign for RelativePosition {
    #[inline]
    fn add_assign(&mut self, rhs: RelativePosition) {
        self.line += rhs.line();
        if rhs.line() == 0 {
            self.column += rhs.column();
        } else {
            self.column = rhs.column();
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("", (0, 0))]
    #[case("a", (0, 1))]
    #[case("abc\ndef\nghi", (2, 3))]
    #[case("abc\r\ndef\r\nghi", (2, 3))]
    fn test_position(#[case] source: &str, #[case] expected: (Line, Column)) {
        assert_eq!(RelativePosition::of(source), expected.into());
    }
}
