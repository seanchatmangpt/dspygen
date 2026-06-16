# Fish shell completion script for dspygen
# To install:
#   dspygen completion install fish
# Or manually:
#   cp fish_completion.fish ~/.config/fish/completions/dspygen.fish

# Disable file completion by default
complete -c dspygen -f

# Helper function condition: no subcommand yet
function __dspygen_no_subcommand
    set cmd (commandline -opc)
    if test (count $cmd) -eq 1
        return 0
    end
    return 1
end

function __dspygen_using_subcommand
    set cmd (commandline -opc)
    if test (count $cmd) -ge 2; and test $cmd[2] = $argv[1]
        return 0
    end
    return 1
end

function __dspygen_using_subcommand_and
    set cmd (commandline -opc)
    if test (count $cmd) -ge 3; and test $cmd[2] = $argv[1]; and test $cmd[3] = $argv[2]
        return 0
    end
    return 1
end

# ── Top-level commands ───────────────────────────────────────────────────────
complete -c dspygen -n __dspygen_no_subcommand -a mcp        -d "MCP server commands"
complete -c dspygen -n __dspygen_no_subcommand -a lsp        -d "LSP server commands"
complete -c dspygen -n __dspygen_no_subcommand -a doctor     -d "Check dspygen environment"
complete -c dspygen -n __dspygen_no_subcommand -a config     -d "Manage configuration"
complete -c dspygen -n __dspygen_no_subcommand -a version    -d "Show version information"
complete -c dspygen -n __dspygen_no_subcommand -a status     -d "Show system status"
complete -c dspygen -n __dspygen_no_subcommand -a completion -d "Shell completion scripts"
complete -c dspygen -n __dspygen_no_subcommand -a module     -d "Generate or call DSPy modules"
complete -c dspygen -n __dspygen_no_subcommand -a agent      -d "Agent management commands"
complete -c dspygen -n __dspygen_no_subcommand -a rm         -d "Resource model commands"
complete -c dspygen -n __dspygen_no_subcommand -a wkf        -d "Workflow commands"
complete -c dspygen -n __dspygen_no_subcommand -a sig        -d "Signature generation commands"
complete -c dspygen -n __dspygen_no_subcommand -a lm         -d "Language model commands"
complete -c dspygen -n __dspygen_no_subcommand -a wrt        -d "Writer commands"
complete -c dspygen -n __dspygen_no_subcommand -a init       -d "Initialize a DSPygen project"
complete -c dspygen -n __dspygen_no_subcommand -a tutor      -d "Interactive development tutor"

# ── mcp ──────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand mcp" -a serve -d "Start MCP server"
complete -c dspygen -n "__dspygen_using_subcommand_and mcp serve" -l transport -d "Transport type" -a "stdio sse" -r
complete -c dspygen -n "__dspygen_using_subcommand_and mcp serve" -l host      -d "Host to bind" -r
complete -c dspygen -n "__dspygen_using_subcommand_and mcp serve" -l port      -d "Port to bind" -r

# ── lsp ──────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand lsp" -a serve -d "Start LSP server"
complete -c dspygen -n "__dspygen_using_subcommand_and lsp serve" -l transport -d "Transport type" -a "stdio tcp" -r
complete -c dspygen -n "__dspygen_using_subcommand_and lsp serve" -l host      -d "Host to bind" -r
complete -c dspygen -n "__dspygen_using_subcommand_and lsp serve" -l port      -d "Port to bind" -r

# ── config ───────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand config" -a show -d "Show current configuration"
complete -c dspygen -n "__dspygen_using_subcommand config" -a set  -d "Set a configuration value"
complete -c dspygen -n "__dspygen_using_subcommand config" -a get  -d "Get a configuration value"
complete -c dspygen -n "__dspygen_using_subcommand config" -a init -d "Initialize configuration"

# ── completion ───────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand completion" -a install -d "Install completions"
complete -c dspygen -n "__dspygen_using_subcommand completion" -a show    -d "Print completion script"
complete -c dspygen -n "__dspygen_using_subcommand_and completion install" -a "bash zsh fish powershell"
complete -c dspygen -n "__dspygen_using_subcommand_and completion show"    -a "bash zsh fish powershell"

# ── module ───────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand module" -a new  -d "Generate a new DSPy module"
complete -c dspygen -n "__dspygen_using_subcommand module" -a run  -d "Run a module"
complete -c dspygen -n "__dspygen_using_subcommand module" -a list -d "List available modules"
complete -c dspygen -n "__dspygen_using_subcommand module" -a help -d "Module help"
# Dynamic module name completion
complete -c dspygen -n "__dspygen_using_subcommand_and module run" -a "(dspygen module list --quiet 2>/dev/null)"

# ── agent ────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand agent" -a new  -d "Create a new agent"
complete -c dspygen -n "__dspygen_using_subcommand agent" -a run  -d "Run an agent"
complete -c dspygen -n "__dspygen_using_subcommand agent" -a list -d "List agents"

# ── rm ───────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand rm" -a new  -d "Create resource model"
complete -c dspygen -n "__dspygen_using_subcommand rm" -a run  -d "Run resource model"
complete -c dspygen -n "__dspygen_using_subcommand rm" -a list -d "List resource models"

# ── wkf ──────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand wkf" -a new  -d "Create workflow"
complete -c dspygen -n "__dspygen_using_subcommand wkf" -a run  -d "Run workflow"
complete -c dspygen -n "__dspygen_using_subcommand wkf" -a list -d "List workflows"

# ── sig ──────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand sig" -a new  -d "Create signature"
complete -c dspygen -n "__dspygen_using_subcommand sig" -a run  -d "Run signature"
complete -c dspygen -n "__dspygen_using_subcommand sig" -a list -d "List signatures"

# ── lm ───────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand lm" -a new -d "Generate a new language model"

# ── wrt ──────────────────────────────────────────────────────────────────────
complete -c dspygen -n "__dspygen_using_subcommand wrt" -a new  -d "Create writer"
complete -c dspygen -n "__dspygen_using_subcommand wrt" -a run  -d "Run writer"
complete -c dspygen -n "__dspygen_using_subcommand wrt" -a list -d "List writers"
