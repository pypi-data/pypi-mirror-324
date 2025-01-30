mod array;
mod boolean;
mod date_time;
mod float;
mod integer;
mod string;
mod table;

pub use array::{Array, ArrayKind};
use ast::AstNode;
pub use boolean::Boolean;
pub use date_time::{LocalDate, LocalDateTime, LocalTime, OffsetDateTime};
pub use float::Float;
pub use integer::{Integer, IntegerKind};
pub use string::{String, StringKind};
pub use table::{Table, TableKind};

use crate::{support::comment::try_new_comment, DocumentTreeResult, IntoDocumentTreeResult};

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    Boolean(Boolean),
    Integer(Integer),
    Float(Float),
    String(String),
    OffsetDateTime(OffsetDateTime),
    LocalDateTime(LocalDateTime),
    LocalDate(LocalDate),
    LocalTime(LocalTime),
    Array(Array),
    Table(Table),
    Incomplete { range: text::Range },
}

impl Value {
    #[inline]
    pub fn range(&self) -> text::Range {
        match self {
            Value::Boolean(value) => value.range(),
            Value::Integer(value) => value.range(),
            Value::Float(value) => value.range(),
            Value::String(value) => value.range(),
            Value::OffsetDateTime(value) => value.range(),
            Value::LocalDateTime(value) => value.range(),
            Value::LocalDate(value) => value.range(),
            Value::LocalTime(value) => value.range(),
            Value::Array(value) => value.range(),
            Value::Table(value) => value.range(),
            Value::Incomplete { range } => *range,
        }
    }

    #[inline]
    pub fn symbol_range(&self) -> text::Range {
        match self {
            Value::Boolean(value) => value.symbol_range(),
            Value::Integer(value) => value.symbol_range(),
            Value::Float(value) => value.symbol_range(),
            Value::String(value) => value.symbol_range(),
            Value::OffsetDateTime(value) => value.symbol_range(),
            Value::LocalDateTime(value) => value.symbol_range(),
            Value::LocalDate(value) => value.symbol_range(),
            Value::LocalTime(value) => value.symbol_range(),
            Value::Array(value) => value.symbol_range(),
            Value::Table(value) => value.symbol_range(),
            Value::Incomplete { range } => *range,
        }
    }
}

impl crate::ValueImpl for Value {
    fn value_type(&self) -> crate::ValueType {
        match self {
            Value::Boolean(boolean) => boolean.value_type(),
            Value::Integer(integer) => integer.value_type(),
            Value::Float(float) => float.value_type(),
            Value::String(string) => string.value_type(),
            Value::OffsetDateTime(offset_date_time) => offset_date_time.value_type(),
            Value::LocalDateTime(local_date_time) => local_date_time.value_type(),
            Value::LocalDate(local_date) => local_date.value_type(),
            Value::LocalTime(local_time) => local_time.value_type(),
            Value::Array(array) => array.value_type(),
            Value::Table(table) => table.value_type(),
            Value::Incomplete { .. } => crate::ValueType::Incomplete,
        }
    }

    fn range(&self) -> text::Range {
        self.range()
    }
}

impl IntoDocumentTreeResult<crate::Value> for ast::Value {
    fn into_document_tree_result(
        self,
        toml_version: toml_version::TomlVersion,
    ) -> DocumentTreeResult<crate::Value> {
        let mut errors = Vec::new();
        for comment in self.leading_comments() {
            if let Err(error) = try_new_comment(comment.as_ref()) {
                errors.push(error);
            }
        }

        if let Some(comment) = self.tailing_comment() {
            if let Err(error) = try_new_comment(comment.as_ref()) {
                errors.push(error);
            }
        }

        let mut document_tree_result = match self {
            ast::Value::BasicString(string) => string.into_document_tree_result(toml_version),
            ast::Value::LiteralString(string) => string.into_document_tree_result(toml_version),
            ast::Value::MultiLineBasicString(string) => {
                string.into_document_tree_result(toml_version)
            }
            ast::Value::MultiLineLiteralString(string) => {
                string.into_document_tree_result(toml_version)
            }
            ast::Value::IntegerBin(integer) => integer.into_document_tree_result(toml_version),
            ast::Value::IntegerOct(integer) => integer.into_document_tree_result(toml_version),
            ast::Value::IntegerDec(integer) => integer.into_document_tree_result(toml_version),
            ast::Value::IntegerHex(integer) => integer.into_document_tree_result(toml_version),
            ast::Value::Float(float) => float.into_document_tree_result(toml_version),
            ast::Value::Boolean(boolean) => boolean.into_document_tree_result(toml_version),
            ast::Value::OffsetDateTime(dt) => dt.into_document_tree_result(toml_version),
            ast::Value::LocalDateTime(dt) => dt.into_document_tree_result(toml_version),
            ast::Value::LocalDate(date) => date.into_document_tree_result(toml_version),
            ast::Value::LocalTime(time) => time.into_document_tree_result(toml_version),
            ast::Value::Array(array) => array.into_document_tree_result(toml_version),
            ast::Value::InlineTable(inline_table) => {
                inline_table.into_document_tree_result(toml_version)
            }
        };

        errors.extend(document_tree_result.errors);
        document_tree_result.errors = errors;

        document_tree_result
    }
}
