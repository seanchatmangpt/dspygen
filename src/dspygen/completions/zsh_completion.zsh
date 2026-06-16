#compdef dspygen
# ZSH completion script for dspygen
# To install, add to ~/.zshrc:
#   source <(_DSPYGEN_COMPLETE=zsh_source dspygen)
# Or use the static script:
#   fpath=(~/.zsh/completions $fpath)
#   cp zsh_completion.zsh ~/.zsh/completions/_dspygen
#   autoload -Uz compinit && compinit

_dspygen() {
    local state

    local -a commands
    commands=(
        'mcp:MCP server commands'
        'lsp:LSP server commands'
        'doctor:Check dspygen environment'
        'config:Manage configuration'
        'version:Show version information'
        'status:Show system status'
        'completion:Shell completion scripts'
        'module:Generate or call DSPy modules'
        'agent:Agent management commands'
        'rm:Resource model commands'
        'wkf:Workflow commands'
        'sig:Signature generation commands'
        'lm:Language model commands'
        'wrt:Writer commands'
        'init:Initialize a DSPygen project'
        'tutor:Interactive development tutor'
    )

    local -a shells
    shells=(bash zsh fish powershell)

    local -a transports_mcp
    transports_mcp=(stdio sse)

    local -a transports_lsp
    transports_lsp=(stdio tcp)

    local -a config_subcommands
    config_subcommands=(show set get init)

    local -a completion_subcommands
    completion_subcommands=(install show)

    _arguments -C \
        '1:command:->command' \
        '*::args:->args' \
        && return 0

    case $state in
        command)
            _describe 'dspygen commands' commands
            ;;
        args)
            case ${words[1]} in
                mcp)
                    _arguments \
                        '1:subcommand:(serve)' \
                        '--transport[Transport protocol]:transport:(stdio sse)' \
                        '--host[Host to bind to]:host:' \
                        '--port[Port to bind to]:port:'
                    ;;
                lsp)
                    _arguments \
                        '1:subcommand:(serve)' \
                        '--transport[Transport protocol]:transport:(stdio tcp)' \
                        '--host[Host to bind to]:host:' \
                        '--port[Port to bind to]:port:'
                    ;;
                config)
                    _arguments '1:subcommand:(show set get init)'
                    ;;
                completion)
                    _arguments \
                        '1:subcommand:(install show)' \
                        '2:shell:(bash zsh fish powershell)'
                    ;;
                module)
                    local -a module_subcmds
                    module_subcmds=(new run list help)
                    _arguments '1:subcommand:(new run list help)'
                    ;;
                agent)
                    _arguments '1:subcommand:(new run list)'
                    ;;
                rm)
                    _arguments '1:subcommand:(new run list)'
                    ;;
                wkf)
                    _arguments '1:subcommand:(new run list)'
                    ;;
                sig)
                    _arguments '1:subcommand:(new run list)'
                    ;;
                lm)
                    _arguments '1:subcommand:(new)'
                    ;;
                wrt)
                    _arguments '1:subcommand:(new run list)'
                    ;;
                *)
                    _describe 'dspygen commands' commands
                    ;;
            esac
            ;;
    esac
}

compdef _dspygen dspygen
