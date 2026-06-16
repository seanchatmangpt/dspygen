import * as vscode from 'vscode';
import { LanguageClient } from 'vscode-languageclient/node';
import { createLspClient } from './lsp-client';

let client: LanguageClient | undefined;
let statusBarItem: vscode.StatusBarItem;

export async function activate(context: vscode.ExtensionContext): Promise<void> {
    // Status bar
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    const model = vscode.workspace.getConfiguration('dspygen').get<string>('model', 'gpt-4o-mini');
    statusBarItem.text = `$(brain) DSPyGen: ${model}`;
    statusBarItem.tooltip = 'DSPyGen active model';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Start LSP if enabled
    const lspEnabled = vscode.workspace.getConfiguration('dspygen').get<boolean>('lsp.enabled', true);
    if (lspEnabled) {
        client = createLspClient(context);
        await client.start();
    }

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('dspygen.runModule', runModuleCommand),
        vscode.commands.registerCommand('dspygen.generateModule', generateModuleCommand),
        vscode.commands.registerCommand('dspygen.validateSignature', validateSignatureCommand),
        vscode.commands.registerCommand('dspygen.showModuleInfo', showModuleInfoCommand),
        vscode.commands.registerCommand('dspygen.startLSP', startLSPCommand),
    );
}

export async function deactivate(): Promise<void> {
    if (client) {
        await client.stop();
    }
}

async function runModuleCommand(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return; }
    const moduleName = await vscode.window.showInputBox({ prompt: 'Enter dspygen module name', placeHolder: 'blog_module' });
    if (!moduleName) { return; }
    const terminal = vscode.window.createTerminal('DSPyGen');
    terminal.show();
    terminal.sendText(`dspygen modules run ${moduleName}`);
}

async function generateModuleCommand(): Promise<void> {
    const name = await vscode.window.showInputBox({ prompt: 'New module name', placeHolder: 'my_module' });
    if (!name) { return; }
    const terminal = vscode.window.createTerminal('DSPyGen');
    terminal.show();
    terminal.sendText(`dspygen modules generate ${name}`);
}

async function validateSignatureCommand(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return; }
    const selection = editor.document.getText(editor.selection) || editor.document.getText();
    vscode.window.showInformationMessage(`DSPyGen: Validating signature in ${editor.document.fileName}`);
    const terminal = vscode.window.createTerminal('DSPyGen Validate');
    terminal.show();
    terminal.sendText(`dspygen signatures validate`);
}

async function showModuleInfoCommand(): Promise<void> {
    const terminal = vscode.window.createTerminal('DSPyGen Info');
    terminal.show();
    terminal.sendText(`dspygen modules list`);
}

async function startLSPCommand(): Promise<void> {
    if (client && client.isRunning()) {
        vscode.window.showInformationMessage('DSPyGen LSP is already running.');
        return;
    }
    vscode.window.showInformationMessage('Starting DSPyGen LSP server...');
}
