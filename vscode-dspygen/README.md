# DSPyGen VS Code Extension

DSPy/dspygen IDE support — AI-powered module generation, pipeline execution, and LSP integration.

---

## Installation

### From VS Code Marketplace

Search for **DSPyGen** in the Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`) and click **Install**.

Or install via the command line:

```bash
code --install-extension seanchatmangpt.dspygen
```

### Manual Install from VSIX

1. Download the latest `.vsix` file from the [Releases](https://github.com/seanchatmangpt/dspygen/releases) page.
2. Open VS Code.
3. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
4. Run **Extensions: Install from VSIX...** and select the downloaded file.

### Build from Source

```bash
git clone https://github.com/seanchatmangpt/dspygen.git
cd dspygen/vscode-dspygen
npm install
npm run compile
```

Press `F5` in VS Code to launch the Extension Development Host.

### Prerequisites

- VS Code 1.85.0 or newer
- Python 3.10+
- `dspygen` installed in your Python environment:
  ```bash
  pip install dspygen
  ```
- (Optional) `dspygen-lsp` for language server features:
  ```bash
  pip install dspygen[lsp]
  ```

---

## Features

### Commands and Keybindings

All commands are available in the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).

| Command | Title | Keybinding (Win/Linux) | Keybinding (Mac) |
|---|---|---|---|
| `dspygen.runModule` | DSPyGen: Run Module | `Ctrl+Shift+D R` | `Cmd+Shift+D R` |
| `dspygen.generateModule` | DSPyGen: Generate Module | `Ctrl+Shift+D G` | `Cmd+Shift+D G` |
| `dspygen.validateSignature` | DSPyGen: Validate Signature | — | — |
| `dspygen.showModuleInfo` | DSPyGen: Show Module Info | — | — |
| `dspygen.startLSP` | DSPyGen: Start LSP Server | — | — |

#### Command Details

- **Run Module** (`dspygen.runModule`): Prompts for a DSPyGen module name and executes `dspygen modules run <name>` in a terminal. Available in the editor context menu for Python files.
- **Generate Module** (`dspygen.generateModule`): Prompts for a module name and runs `dspygen modules generate <name>` to scaffold a new module. Also available in the Python editor context menu.
- **Validate Signature** (`dspygen.validateSignature`): Validates DSPy signatures in the active editor by running `dspygen signatures validate` in a terminal.
- **Show Module Info** (`dspygen.showModuleInfo`): Runs `dspygen modules list` in a terminal to display all available modules.
- **Start LSP Server** (`dspygen.startLSP`): Manually starts the DSPyGen Language Server if it is not already running.

### Status Bar

The extension displays the active LLM model in the VS Code status bar (bottom-right):

```
$(brain) DSPyGen: gpt-4o-mini
```

The icon and model name update to reflect the `dspygen.model` setting.

### Context Menu

Right-clicking inside any Python file shows DSPyGen commands in the editor context menu:
- **DSPyGen: Run Module**
- **DSPyGen: Generate Module**

---

## Configuration Reference

All settings are in the `dspygen` namespace. Configure them in **File > Preferences > Settings** or directly in `settings.json`.

| Setting | Type | Default | Description |
|---|---|---|---|
| `dspygen.lsp.enabled` | `boolean` | `true` | Enable the DSPyGen Language Server |
| `dspygen.lsp.path` | `string` | `"dspygen-lsp"` | Path to the `dspygen-lsp` executable |
| `dspygen.model` | `string` | `"gpt-4o-mini"` | Default LM model used by DSPyGen |
| `dspygen.ollamaHost` | `string` | `"http://localhost:11434"` | Ollama host URL for local model inference |

### Example `settings.json`

```json
{
  "dspygen.model": "ollama/llama3",
  "dspygen.ollamaHost": "http://localhost:11434",
  "dspygen.lsp.enabled": true,
  "dspygen.lsp.path": "/home/user/.venv/bin/dspygen-lsp"
}
```

---

## Language Support

The extension registers a custom language for DSPyGen DSL files:

| Extension | Language ID | Description |
|---|---|---|
| `.py` | `python` | Standard Python — LSP diagnostics and all commands active |
| `.dspy` | `dspy` | DSPy DSL — syntax highlighting, bracket matching, LSP support |
| `.dsg` | `dspy` | DSPyGen DSL shorthand — same support as `.dspy` |

### Syntax Features for `.dspy` / `.dsg` Files

- Line comments with `#`
- Auto-closing pairs for `[]`, `{}`, `()`, `""`, `''`
- Bracket matching for `[]`, `{}`, `()`

---

## LSP Features

The extension connects to the `dspygen-lsp` language server over stdio. Configure the executable path with `dspygen.lsp.path`.

When active, the language server provides:

- **Diagnostics**: Real-time error reporting for invalid DSPy signatures and module declarations
- **Autocompletion**: Suggestions for DSPy predictor types (`Predict`, `ChainOfThought`, `Retrieve`, etc.) and module fields
- **Hover Documentation**: Inline docs for DSPy fields, modules, and signatures
- **File Watching**: Monitors `**/*.{py,dspy,dsg,yaml}` for changes and updates diagnostics automatically
- **Output Channel**: Server logs available in the **DSPyGen LSP** output channel (`View > Output`, select `DSPyGen LSP`)

The LSP starts automatically when a Python or `.dspy`/`.dsg` file is opened (if `dspygen.lsp.enabled` is `true`). To start it manually, run **DSPyGen: Start LSP Server** from the Command Palette.

---

## Project Structure

```
vscode-dspygen/
  src/
    extension.ts              # Main extension entry point and command handlers
    lsp-client.ts             # LSP client configuration and factory
  syntaxes/
    dspygen.tmLanguage.json   # TextMate grammar for .dspy/.dsg syntax highlighting
  dist/                       # Compiled JavaScript output (generated by tsc)
  package.json                # Extension manifest (commands, settings, keybindings)
  tsconfig.json               # TypeScript compiler configuration
  language-configuration.json # Bracket/comment/auto-closing config for DSL
  .vscodeignore               # Files excluded from the VSIX package
  README.md                   # This file
```

---

## Contributing

1. Fork the repository at https://github.com/seanchatmangpt/dspygen
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and run `npm run compile` to verify TypeScript compiles cleanly.
4. Press `F5` in VS Code to test in the Extension Development Host.
5. Submit a pull request.

---

## License

MIT License. See [LICENSE](../LICENSE) for details.

---

## Links

- [DSPyGen on PyPI](https://pypi.org/project/dspygen/)
- [DSPy Framework](https://github.com/stanfordnlp/dspy)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)
