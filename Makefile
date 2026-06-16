.PHONY: completions completions-bash completions-zsh completions-fish install-completion-bash install-completion-zsh install-completion-fish

# ── Shell completion targets ─────────────────────────────────────────────────

## Generate all completion scripts into src/dspygen/completions/
completions: completions-bash completions-zsh completions-fish

## Regenerate bash completion script via Typer
completions-bash:
	_DSPYGEN_COMPLETE=bash_source dspygen > src/dspygen/completions/bash_completion.sh
	@echo "Bash completion written to src/dspygen/completions/bash_completion.sh"

## Regenerate zsh completion script via Typer
completions-zsh:
	_DSPYGEN_COMPLETE=zsh_source dspygen > src/dspygen/completions/zsh_completion.zsh
	@echo "Zsh completion written to src/dspygen/completions/zsh_completion.zsh"

## Regenerate fish completion script via Typer
completions-fish:
	_DSPYGEN_COMPLETE=fish_source dspygen > src/dspygen/completions/fish_completion.fish
	@echo "Fish completion written to src/dspygen/completions/fish_completion.fish"

## Install bash completion for the current user (~/.bashrc)
install-completion-bash:
	dspygen completion install bash

## Install zsh completion for the current user (~/.zshrc)
install-completion-zsh:
	dspygen completion install zsh

## Install fish completion for the current user
install-completion-fish:
	dspygen completion install fish
