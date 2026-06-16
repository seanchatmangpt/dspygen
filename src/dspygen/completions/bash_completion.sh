#!/usr/bin/env bash
# Bash completion script for dspygen
# Source this file or add to ~/.bashrc:
#   source <(_DSPYGEN_COMPLETE=bash_source dspygen)
# Or use the static script:
#   source /path/to/bash_completion.sh

_dspygen_completion() {
    local IFS=$'\n'
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local cmd="${COMP_WORDS[1]}"
    local subcmd="${COMP_WORDS[2]}"

    # Top-level commands
    local top_commands="mcp lsp doctor config version status completion module agent rm wkf sig lm wrt init tutor"

    if [[ "${COMP_CWORD}" -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${top_commands}" -- "${cur}"))
        return
    fi

    case "${cmd}" in
        mcp)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "serve" -- "${cur}"))
            elif [[ "${COMP_CWORD}" -ge 3 && "${subcmd}" == "serve" ]]; then
                case "${prev}" in
                    --transport|-t)
                        COMPREPLY=($(compgen -W "stdio sse" -- "${cur}"))
                        ;;
                    *)
                        COMPREPLY=($(compgen -W "--transport --host --port --help" -- "${cur}"))
                        ;;
                esac
            fi
            ;;
        lsp)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "serve" -- "${cur}"))
            elif [[ "${COMP_CWORD}" -ge 3 && "${subcmd}" == "serve" ]]; then
                case "${prev}" in
                    --transport|-t)
                        COMPREPLY=($(compgen -W "stdio tcp" -- "${cur}"))
                        ;;
                    *)
                        COMPREPLY=($(compgen -W "--transport --host --port --help" -- "${cur}"))
                        ;;
                esac
            fi
            ;;
        config)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "show set get init" -- "${cur}"))
            fi
            ;;
        completion)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "install show" -- "${cur}"))
            elif [[ "${COMP_CWORD}" -eq 3 ]]; then
                COMPREPLY=($(compgen -W "bash zsh fish powershell" -- "${cur}"))
            fi
            ;;
        module)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list help" -- "${cur}"))
            elif [[ "${COMP_CWORD}" -ge 3 && "${subcmd}" == "run" ]]; then
                # Dynamic completion: attempt to list available modules
                local modules
                modules=$(dspygen module list --quiet 2>/dev/null)
                if [[ -n "${modules}" ]]; then
                    COMPREPLY=($(compgen -W "${modules}" -- "${cur}"))
                fi
            fi
            ;;
        agent)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list" -- "${cur}"))
            fi
            ;;
        rm)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list" -- "${cur}"))
            fi
            ;;
        wkf)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list" -- "${cur}"))
            fi
            ;;
        sig)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list" -- "${cur}"))
            fi
            ;;
        lm)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new" -- "${cur}"))
            fi
            ;;
        wrt)
            if [[ "${COMP_CWORD}" -eq 2 ]]; then
                COMPREPLY=($(compgen -W "new run list" -- "${cur}"))
            fi
            ;;
        doctor|version|status)
            COMPREPLY=()
            ;;
        *)
            COMPREPLY=($(compgen -W "${top_commands}" -- "${cur}"))
            ;;
    esac
}

complete -F _dspygen_completion dspygen
