use toml_version::TomlVersion;

use crate::{
    support::integer::{try_from_binary, try_from_decimal, try_from_hexadecimal, try_from_octal},
    DocumentTreeResult, IntoDocumentTreeResult, ValueImpl, ValueType,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum IntegerKind {
    Binary(ast::IntegerBin),
    Decimal(ast::IntegerDec),
    Octal(ast::IntegerOct),
    Hexadecimal(ast::IntegerHex),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Integer {
    kind: IntegerKind,
    value: i64,
}

impl Integer {
    #[inline]
    pub fn kind(&self) -> &IntegerKind {
        &self.kind
    }

    #[inline]
    pub fn value(&self) -> i64 {
        self.value
    }

    #[inline]
    pub fn range(&self) -> text::Range {
        match self.kind() {
            IntegerKind::Binary(node) => node.token(),
            IntegerKind::Decimal(node) => node.token(),
            IntegerKind::Octal(node) => node.token(),
            IntegerKind::Hexadecimal(node) => node.token(),
        }
        .unwrap()
        .range()
    }

    #[inline]
    pub fn symbol_range(&self) -> text::Range {
        self.range()
    }
}

impl ValueImpl for Integer {
    fn value_type(&self) -> ValueType {
        ValueType::Integer
    }

    fn range(&self) -> text::Range {
        self.range()
    }
}

impl IntoDocumentTreeResult<crate::Value> for ast::IntegerBin {
    fn into_document_tree_result(
        self,
        _toml_version: TomlVersion,
    ) -> DocumentTreeResult<crate::Value> {
        let range = self.range();
        let Some(token) = self.token() else {
            return DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::IncompleteNode { range }],
            };
        };

        match try_from_binary(token.text()) {
            Ok(value) => DocumentTreeResult {
                tree: crate::Value::Integer(crate::Integer {
                    kind: IntegerKind::Binary(self),
                    value,
                }),
                errors: Vec::with_capacity(0),
            },
            Err(error) => DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::ParseIntError { error, range }],
            },
        }
    }
}

impl IntoDocumentTreeResult<crate::Value> for ast::IntegerOct {
    fn into_document_tree_result(
        self,
        _toml_version: TomlVersion,
    ) -> DocumentTreeResult<crate::Value> {
        let range = self.range();
        let Some(token) = self.token() else {
            return DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::IncompleteNode { range }],
            };
        };

        match try_from_octal(token.text()) {
            Ok(value) => DocumentTreeResult {
                tree: crate::Value::Integer(crate::Integer {
                    kind: IntegerKind::Octal(self),
                    value,
                }),
                errors: Vec::with_capacity(0),
            },
            Err(error) => DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::ParseIntError { error, range }],
            },
        }
    }
}

impl IntoDocumentTreeResult<crate::Value> for ast::IntegerDec {
    fn into_document_tree_result(
        self,
        _toml_version: TomlVersion,
    ) -> DocumentTreeResult<crate::Value> {
        let range = self.range();
        let Some(token) = self.token() else {
            return DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::IncompleteNode { range }],
            };
        };

        match try_from_decimal(token.text()) {
            Ok(value) => DocumentTreeResult {
                tree: crate::Value::Integer(crate::Integer {
                    kind: IntegerKind::Decimal(self),
                    value,
                }),
                errors: Vec::with_capacity(0),
            },
            Err(error) => DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::ParseIntError { error, range }],
            },
        }
    }
}

impl IntoDocumentTreeResult<crate::Value> for ast::IntegerHex {
    fn into_document_tree_result(
        self,
        _toml_version: TomlVersion,
    ) -> DocumentTreeResult<crate::Value> {
        let range = self.range();
        let Some(token) = self.token() else {
            return DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::IncompleteNode { range }],
            };
        };

        match try_from_hexadecimal(token.text()) {
            Ok(value) => DocumentTreeResult {
                tree: crate::Value::Integer(crate::Integer {
                    kind: IntegerKind::Hexadecimal(self),
                    value,
                }),
                errors: Vec::with_capacity(0),
            },
            Err(error) => DocumentTreeResult {
                tree: crate::Value::Incomplete { range },
                errors: vec![crate::Error::ParseIntError { error, range }],
            },
        }
    }
}
