import * as path from 'path';
import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind,
} from 'vscode-languageclient/node';

export function createLspClient(context: vscode.ExtensionContext): LanguageClient {
    const config = vscode.workspace.getConfiguration('dspygen');
    const lspPath = config.get<string>('lsp.path', 'dspygen-lsp');

    const serverOptions: ServerOptions = {
        command: lspPath,
        args: [],
        transport: TransportKind.stdio,
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'dspy' },
        ],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.{py,dspy,dsg,yaml}'),
        },
        outputChannelName: 'DSPyGen LSP',
    };

    return new LanguageClient(
        'dspygen-lsp',
        'DSPyGen Language Server',
        serverOptions,
        clientOptions,
    );
}
