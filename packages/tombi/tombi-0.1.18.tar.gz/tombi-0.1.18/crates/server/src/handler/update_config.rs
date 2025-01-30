use config::SUPPORTED_CONFIG_FILENAMES;
use tower_lsp::lsp_types::{
    notification::ShowMessage, MessageType, ShowMessageParams, TextDocumentIdentifier, Url,
};

use crate::backend::Backend;

#[tracing::instrument(level = "debug", skip_all)]
pub async fn handle_update_config(
    backend: &Backend,
    TextDocumentIdentifier {
        uri: config_url, ..
    }: TextDocumentIdentifier,
) -> Result<bool, tower_lsp::jsonrpc::Error> {
    tracing::info!("handle_update_config");
    let Some(workspace_folders) = backend.client.workspace_folders().await? else {
        return Ok(false);
    };

    for workspace_folder in workspace_folders {
        let workspace_folder_uri = if !workspace_folder.uri.as_str().ends_with('/') {
            Url::parse(&format!("{}/", workspace_folder.uri.as_str())).unwrap()
        } else {
            workspace_folder.uri
        };

        for config_filename in SUPPORTED_CONFIG_FILENAMES {
            let Ok(workspace_config_url) = workspace_folder_uri.join(config_filename) else {
                continue;
            };

            if config_url == workspace_config_url {
                match config::Config::try_from_url(workspace_config_url) {
                    Ok(Some(config)) => {
                        backend
                            .update_workspace_config(config_url.clone(), config)
                            .await;
                        return Ok(true);
                    }
                    Ok(None) => {
                        continue;
                    }
                    Err(err) => {
                        backend
                            .client
                            .send_notification::<ShowMessage>(ShowMessageParams {
                                typ: MessageType::ERROR,
                                message: err.to_string(),
                            })
                            .await;

                        return Ok(false);
                    }
                }
            }
        }
    }

    tracing::info!("No workspace found for config settings: {}", config_url);

    Ok(false)
}
