#*-          Prompt          -*#

local ret_status="%(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ )"
PROMPT='${ret_status}%{$reset_color%}%{$bg[white]%}%{$fg[black]%}%D{%H:%M}%{$reset_color%} %B%{$fg_bold[green]%}%n%{$fg_bold[white]%}@%{$fg_bold[cyan]%}%M%{$reset_color%}:%{$fg[cyan]%}%B%~%{$reset_color%} $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
