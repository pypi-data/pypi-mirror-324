use tower_lsp::lsp_types::DidChangeTextDocumentParams;

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_did_change(
    backend: &Backend,
    DidChangeTextDocumentParams {
        text_document,
        content_changes,
    }: DidChangeTextDocumentParams,
) {
    tracing::info!("handle_did_change");

    let Some(mut document) = backend.get_document_source_mut(&text_document.uri) else {
        return;
    };

    for content_change in content_changes {
        if let Some(range) = content_change.range {
            tracing::warn!("range change is not supported: {:?}", range);
        } else {
            document.source = content_change.text;
        }
    }
}
