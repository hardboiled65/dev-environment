syntax on
set ruler

au Bufenter *.\(c\|cpp\|h\|html\|css\|php\|ejs\|py\|rs\) set et
set ts=4
set autoindent
set nu
set smartindent
set shiftwidth=4
set laststatus=2	" Always show filename
ab Inc #include 
ab pf printf(
ab sf scanf(
ab im int main(){
ab rt0 return 0;

hi Comment cterm=bold

if exists('+colorcolumn')
	set colorcolumn=80
endif

if filereadable(expand("~/.vim/autoload/pathogen.vim"))
	execute pathogen#infect()
endif

""""""""""""""""""""""""
""     Mapping
""""""""""""""""""""""""
:map \\ :set number!<CR>
:map \[ :tabp<CR>			" Move to previous tab
:map \] :tabn<CR>			" Move to next tab

""""""""""""""""""""""""
""     Functions
""""""""""""""""""""""""
" MakeCGuard: Return C header guard format by filename
function MakeCGuard()
	let filename=expand('%:t')
	let guard=system('python3 -c "print(\"_' . filename . '\".upper().replace(\".\", \"_\"), end=\"\")"')
	return guard " ex) _HEADER_H
endfunction
" MakeCHeaderComment: Return C header comment template
function MakeCHeaderComment()
	let filename=expand('%:t')
	let c_date=system('python3 -c "import time; print(time.strftime(\"%Y. %m. %d. %H:%M\", time.localtime()), end=\"\")"')
	let template="/*\n//  " . filename . "\n//\n" . "//  Author:     <OWNER>\n" . "//  Created:    " . c_date . "\n" . "//  Copyright (c) 2016 <OWNER>. All rights reserved.\n" . "//\n" . "//\n" . "*/"
	return template
endfunction

""""""""""""""""""""""""
""     Commands
""""""""""""""""""""""""
" Cguard: Make C header guard
command Cguard :execute "normal! i#ifndef " . MakeCGuard() . "#define " .MakeCGuard() . "#endif /* " . MakeCGuard() . " */"
" Ccomment: Make C header comment
command Ccomment :0put=MakeCHeaderComment()
