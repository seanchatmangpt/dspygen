# dspygen LSP — Server Capabilities

All capabilities registered by the `dspygen-lsp` server (v1.1.0).

| # | Capability | Description |
|---|---|---|
| 1 | `textDocument/completion` | Context-aware completions for DSPy signatures, RDDDY base classes, model names, and module methods. Triggers on `(`, `.`, ` `, `'`. |
| 2 | `textDocument/hover` | Hover documentation for `init_dspy`, `dspy.Predict`, `dspy.ChainOfThought`, `dspy.ReAct`, `dspy.ProgramOfThought`, signature literals, and module classes. |
| 3 | `textDocument/publishDiagnostics` | Publishes diagnostics on `didOpen` and `didChange`: invalid signatures, missing `forward()`, missing `init_dspy()`, and `ReAct` with empty tools. |
| 4 | `textDocument/definition` | Go-to-definition for dspygen module classes — jumps to the class declaration in the module file. |
| 5 | `textDocument/documentSymbol` | Outline of classes, functions, and methods in the current file. |
| 6 | `workspace/symbol` | Workspace-wide symbol search across all indexed dspygen module files. |
| 7 | `textDocument/rename` | Rename a dspygen module class or symbol across the workspace (also implements `prepareRename` to validate the target). |
| 8 | `textDocument/codeAction` | Quick-fix code actions: add missing `forward()` stub, insert `init_dspy()` call, and fix signature formatting. |
| 9 | `textDocument/semanticTokens/full` | Full-file semantic token highlighting for DSPy-specific identifiers (signatures, predictors, module names). |
| 10 | `textDocument/formatting` | Document formatting via `black` (or a lightweight fallback) for dspygen source files. |
| 11 | `textDocument/references` | Find all references to a dspygen module class or symbol across the workspace. |
| 12 | `textDocument/inlayHint` | Inline hints showing inferred signature field types and resolved model names. |
| 13 | `textDocument/foldingRange` | Folding ranges for class bodies, function bodies, and multi-line signature strings. |
| 14 | `textDocument/prepareCallHierarchy` / `callHierarchy/incomingCalls` / `callHierarchy/outgoingCalls` | Call hierarchy for DSPy module `forward()` methods — shows callers and callees. |
| 15 | `workspace/executeCommand` | Execute server-side commands: `dspygen.reindexModules`, `dspygen.showSignature`, `dspygen.insertInitDspy`. |
