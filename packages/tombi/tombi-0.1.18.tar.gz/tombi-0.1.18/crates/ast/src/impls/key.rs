use toml_version::TomlVersion;

use crate::{support, AstChildren};

impl crate::Key {
    pub fn token(&self) -> Option<syntax::SyntaxToken> {
        match self {
            Self::BareKey(key) => key.token(),
            Self::BasicString(key) => key.token(),
            Self::LiteralString(key) => key.token(),
        }
    }

    pub fn try_to_raw_text(
        &self,
        toml_version: TomlVersion,
    ) -> Result<String, support::string::ParseError> {
        match self {
            Self::BareKey(key) => Ok(key.token().unwrap().text().to_string()),
            Self::BasicString(key) => {
                support::string::try_from_basic_string(key.token().unwrap().text(), toml_version)
            }
            Self::LiteralString(key) => {
                support::string::try_from_literal_string(key.token().unwrap().text())
            }
        }
    }
}

impl AstChildren<crate::Key> {
    pub fn starts_with(&self, other: &AstChildren<crate::Key>) -> bool {
        self.clone().zip(other.clone()).all(|(a, b)| {
            match (
                a.try_to_raw_text(TomlVersion::latest()),
                b.try_to_raw_text(TomlVersion::latest()),
            ) {
                (Ok(a), Ok(b)) => a == b,
                _ => false,
            }
        })
    }

    pub fn same_as(&self, other: &AstChildren<crate::Key>) -> bool {
        (self.clone().count() == other.clone().count()) && self.starts_with(other)
    }

    #[inline]
    pub fn into_vec(self) -> Vec<crate::Key> {
        self.collect()
    }

    pub fn rev(self) -> impl Iterator<Item = crate::Key> {
        self.into_vec().into_iter().rev()
    }
}
