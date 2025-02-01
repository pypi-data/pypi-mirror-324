mod completion_content;
mod completion_edit;
mod completion_kind;
mod hint;
mod value;

use std::ops::Deref;

use ast::{algo::ancestors_at_position, AstNode};
pub use completion_content::CompletionContent;
pub use completion_edit::CompletionEdit;
use completion_kind::CompletionKind;
use config::TomlVersion;
use document_tree::{IntoDocumentTreeResult, TryIntoDocumentTree};
pub use hint::CompletionHint;
use itertools::Itertools;
use schema_store::{Accessor, SchemaDefinitions, Schemas, ValueSchema};
use syntax::{SyntaxElement, SyntaxKind};
use tower_lsp::lsp_types::Url;

pub fn get_completion_contents(
    root: ast::Root,
    position: text::Position,
    document_schema: Option<&schema_store::DocumentSchema>,
    toml_version: config::TomlVersion,
) -> Vec<CompletionContent> {
    let mut keys: Vec<document_tree::Key> = vec![];
    let mut completion_hint = None;

    for node in ancestors_at_position(root.syntax(), position) {
        // tracing::debug!("node: {:?}", node);
        // tracing::debug!(
        //     "prev_sibling_or_token(): {:?}",
        //     node.prev_sibling_or_token()
        // );
        // tracing::debug!(
        //     "next_sibling_or_token(): {:?}",
        //     node.next_sibling_or_token()
        // );
        // tracing::debug!("first_child_or_token(): {:?}", node.first_child_or_token());
        // tracing::debug!("last_child_or_token(): {:?}", node.last_child_or_token());

        let ast_keys = if ast::Keys::cast(node.to_owned()).is_some() {
            match node.last_child_or_token() {
                Some(SyntaxElement::Token(last_token)) => match last_token.kind() {
                    SyntaxKind::DOT => {
                        completion_hint = Some(CompletionHint::DotTrigger {
                            range: last_token.range(),
                        });
                    }
                    _ => {}
                },
                Some(SyntaxElement::Node(last_node)) => match last_node.kind() {
                    SyntaxKind::BARE_KEY
                    | SyntaxKind::BASIC_STRING
                    | SyntaxKind::LITERAL_STRING => {
                        if last_node.range().end() != position {
                            completion_hint = Some(CompletionHint::SpaceTrigger {
                                range: text::Range::new(last_node.range().end(), position),
                            })
                        }
                    }
                    _ => {}
                },
                None => {}
            }
            continue;
        } else if let Some(kv) = ast::KeyValue::cast(node.to_owned()) {
            if let Some(SyntaxElement::Token(last_token)) = node.last_child_or_token() {
                match last_token.kind() {
                    SyntaxKind::EQUAL => {
                        completion_hint = Some(CompletionHint::EqualTrigger {
                            range: last_token.range(),
                        });
                    }
                    _ => {}
                }
            }
            kv.keys()
        } else if let Some(table) = ast::Table::cast(node.to_owned()) {
            let (bracket_start_range, bracket_end_range) =
                match (table.bracket_start(), table.bracket_end()) {
                    (Some(bracket_start), Some(blacket_end)) => {
                        (bracket_start.range(), blacket_end.range())
                    }
                    _ => return Vec::with_capacity(0),
                };

            if position < bracket_start_range.start()
                || (bracket_end_range.end() <= position
                    && position.line() == bracket_end_range.end().line())
            {
                return Vec::with_capacity(0);
            } else {
                if table.contains_header(position) {
                    completion_hint = Some(CompletionHint::InTableHeader);
                }
                table.header()
            }
        } else if let Some(array_of_tables) = ast::ArrayOfTables::cast(node.to_owned()) {
            let (double_bracket_start_range, double_bracket_end_range) = {
                match (
                    array_of_tables.double_bracket_start(),
                    array_of_tables.double_bracket_end(),
                ) {
                    (Some(double_bracket_start), Some(double_bracket_end)) => {
                        (double_bracket_start.range(), double_bracket_end.range())
                    }
                    _ => return Vec::with_capacity(0),
                }
            };

            if position < double_bracket_start_range.start()
                && (double_bracket_end_range.end() <= position
                    && position.line() == double_bracket_end_range.end().line())
            {
                return Vec::with_capacity(0);
            } else {
                if array_of_tables.contains_header(position) {
                    completion_hint = Some(CompletionHint::InTableHeader);
                }
                array_of_tables.header()
            }
        } else {
            continue;
        };

        let Some(ast_keys) = ast_keys else { continue };
        let mut new_keys = if ast_keys.range().contains(position) {
            let mut new_keys = Vec::with_capacity(ast_keys.keys().count());
            for key in ast_keys
                .keys()
                .take_while(|key| key.token().unwrap().range().start() <= position)
            {
                match key.try_into_document_tree(toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return vec![],
                }
            }
            new_keys
        } else {
            let mut new_keys = Vec::with_capacity(ast_keys.keys().count());
            for key in ast_keys.keys() {
                match key.try_into_document_tree(toml_version) {
                    Ok(Some(key)) => new_keys.push(key),
                    _ => return vec![],
                }
            }
            new_keys
        };

        new_keys.extend(keys);
        keys = new_keys;
    }

    let document_tree = root.into_document_tree_result(toml_version).tree;

    let completion_contents = document_tree.deref().find_completion_contents(
        &Vec::with_capacity(0),
        document_schema.map(|schema| schema.value_schema()),
        toml_version,
        position,
        &keys,
        document_schema.as_ref().map(|schema| &schema.schema_url),
        document_schema.as_ref().map(|schema| &schema.definitions),
        completion_hint,
    );

    // NOTE: If there are completion contents with the same priority,
    //       remove the completion contents with lower priority.
    completion_contents
        .into_iter()
        .fold(dashmap::DashMap::new(), |acc, content| {
            acc.entry(content.label.clone())
                .or_insert_with(Vec::new)
                .push(content);
            acc
        })
        .into_iter()
        .filter_map(|(_, contents)| {
            contents
                .into_iter()
                .sorted_by(|a, b| a.priority.cmp(&b.priority))
                .next()
        })
        .collect()
}

pub trait FindCompletionContents {
    fn find_completion_contents(
        &self,
        accessors: &Vec<Accessor>,
        value_schema: Option<&ValueSchema>,
        toml_version: TomlVersion,
        position: text::Position,
        keys: &[document_tree::Key],
        schema_url: Option<&Url>,
        definitions: Option<&SchemaDefinitions>,
        completion_hint: Option<CompletionHint>,
    ) -> Vec<CompletionContent>;
}

pub trait CompletionCandidate {
    fn title(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String>;

    fn description(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String>;

    fn detail(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        self.title(definitions, completion_hint)
    }

    fn documentation(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        self.description(definitions, completion_hint)
    }
}

impl<T: CompositeSchema> CompletionCandidate for T {
    fn title(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        let mut candidates = ahash::AHashSet::new();
        {
            if let Ok(mut schemas) = self.schemas().write() {
                for schema in schemas.iter_mut() {
                    if let Ok(schema) = schema.resolve(definitions) {
                        if matches!(schema, ValueSchema::Null) {
                            continue;
                        }
                        if let Some(candidate) =
                            CompletionCandidate::title(schema, definitions, completion_hint)
                        {
                            candidates.insert(candidate.to_string());
                        }
                    }
                }
            }
        }
        if candidates.len() == 1 {
            return candidates.into_iter().next();
        }

        self.title().as_deref().map(|title| title.into())
    }

    fn description(
        &self,
        definitions: &SchemaDefinitions,
        completion_hint: Option<CompletionHint>,
    ) -> Option<String> {
        let mut candidates = ahash::AHashSet::new();
        {
            if let Ok(mut schemas) = self.schemas().write() {
                for schema in schemas.iter_mut() {
                    if let Ok(schema) = schema.resolve(definitions) {
                        if matches!(schema, ValueSchema::Null) {
                            continue;
                        }
                        if let Some(candidate) =
                            CompletionCandidate::description(schema, definitions, completion_hint)
                        {
                            candidates.insert(candidate.to_string());
                        }
                    }
                }
            }
        }

        if candidates.len() == 1 {
            return candidates.into_iter().next();
        }

        self.description()
            .as_deref()
            .map(|description| description.into())
    }
}

pub trait CompositeSchema {
    fn title(&self) -> Option<String>;
    fn description(&self) -> Option<String>;
    fn schemas(&self) -> &Schemas;
}

fn find_one_of_completion_items<T>(
    value: &T,
    accessors: &Vec<Accessor>,
    one_of_schema: &schema_store::OneOfSchema,
    toml_version: TomlVersion,
    position: text::Position,
    keys: &[document_tree::Key],
    schema_url: Option<&Url>,
    definitions: Option<&SchemaDefinitions>,
    completion_hint: Option<CompletionHint>,
) -> Vec<CompletionContent>
where
    T: FindCompletionContents,
{
    let Some(definitions) = definitions else {
        unreachable!("definitions must be provided");
    };

    let mut completion_items = Vec::new();

    if let Ok(mut schemas) = one_of_schema.schemas.write() {
        for schema in schemas.iter_mut() {
            if let Ok(schema) = schema.resolve(definitions) {
                let schema_completions = value.find_completion_contents(
                    accessors,
                    Some(schema),
                    toml_version,
                    position,
                    keys,
                    schema_url,
                    Some(definitions),
                    completion_hint,
                );

                completion_items.extend(schema_completions);
            }
        }
    }

    for completion_item in completion_items.iter_mut() {
        if completion_item.detail.is_none() {
            completion_item.detail = one_of_schema.detail(definitions, completion_hint);
        }
        if completion_item.documentation.is_none() {
            completion_item.documentation =
                one_of_schema.documentation(definitions, completion_hint);
        }
    }

    if let Some(default) = &one_of_schema.default {
        if let Some(completion_item) =
            serde_value_to_completion_item(default, position, schema_url, completion_hint)
        {
            completion_items.push(completion_item);
        }
    }

    completion_items
}

fn find_any_of_completion_items<T>(
    value: &T,
    accessors: &Vec<Accessor>,
    any_of_schema: &schema_store::AnyOfSchema,
    toml_version: TomlVersion,
    position: text::Position,
    keys: &[document_tree::Key],
    schema_url: Option<&Url>,
    definitions: Option<&SchemaDefinitions>,
    completion_hint: Option<CompletionHint>,
) -> Vec<CompletionContent>
where
    T: FindCompletionContents,
{
    let Some(definitions) = definitions else {
        unreachable!("definitions must be provided");
    };

    let mut completion_items = Vec::new();

    if let Ok(mut schemas) = any_of_schema.schemas.write() {
        for schema in schemas.iter_mut() {
            if let Ok(schema) = schema.resolve(definitions) {
                let schema_completions = value.find_completion_contents(
                    accessors,
                    Some(schema),
                    toml_version,
                    position,
                    keys,
                    schema_url,
                    Some(definitions),
                    completion_hint,
                );

                completion_items.extend(schema_completions);
            }
        }
    }

    for completion_item in completion_items.iter_mut() {
        if completion_item.detail.is_none() {
            completion_item.detail = any_of_schema.detail(definitions, completion_hint);
        }
        if completion_item.documentation.is_none() {
            completion_item.documentation =
                any_of_schema.documentation(definitions, completion_hint);
        }
    }

    if let Some(default) = &any_of_schema.default {
        if let Some(completion_item) =
            serde_value_to_completion_item(default, position, schema_url, completion_hint)
        {
            completion_items.push(completion_item);
        }
    }

    completion_items
}

fn find_all_if_completion_items<T>(
    value: &T,
    accessors: &Vec<Accessor>,
    all_of_schema: &schema_store::AllOfSchema,
    toml_version: TomlVersion,
    position: text::Position,
    keys: &[document_tree::Key],
    schema_url: Option<&Url>,
    definitions: Option<&SchemaDefinitions>,
    completion_hint: Option<CompletionHint>,
) -> Vec<CompletionContent>
where
    T: FindCompletionContents,
{
    let Some(definitions) = definitions else {
        unreachable!("definitions must be provided");
    };

    let mut completion_items = Vec::new();

    if let Ok(mut schemas) = all_of_schema.schemas.write() {
        for schema in schemas.iter_mut() {
            if let Ok(schema) = schema.resolve(definitions) {
                let schema_completions = value.find_completion_contents(
                    accessors,
                    Some(schema),
                    toml_version,
                    position,
                    keys,
                    schema_url,
                    Some(definitions),
                    completion_hint,
                );

                completion_items.extend(schema_completions);
            }
        }
    }

    for completion_item in completion_items.iter_mut() {
        if completion_item.detail.is_none() {
            completion_item.detail = all_of_schema.detail(definitions, completion_hint);
        }
        if completion_item.documentation.is_none() {
            completion_item.documentation =
                all_of_schema.documentation(definitions, completion_hint);
        }
    }

    if let Some(default) = &all_of_schema.default {
        if let Some(completion_item) =
            serde_value_to_completion_item(default, position, schema_url, completion_hint)
        {
            completion_items.push(completion_item);
        }
    }

    completion_items
}

fn serde_value_to_completion_item(
    value: &serde_json::Value,
    position: text::Position,
    schema_url: Option<&Url>,
    completion_hint: Option<CompletionHint>,
) -> Option<CompletionContent> {
    let (kind, value) = match value {
        serde_json::Value::String(value) => (CompletionKind::String, format!("\"{value}\"")),
        serde_json::Value::Number(value) => {
            if value.is_i64() {
                (CompletionKind::Integer, value.to_string())
            } else {
                (CompletionKind::Float, value.to_string())
            }
        }
        serde_json::Value::Bool(value) => (CompletionKind::Boolean, value.to_string()),
        _ => return None,
    };

    Some(CompletionContent::new_default_value(
        kind,
        value.to_string(),
        CompletionEdit::new_literal(&value, position, completion_hint),
        schema_url,
    ))
}
