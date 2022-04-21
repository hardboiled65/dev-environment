scriptencoding utf-8
set encoding=utf-8

syntax on
set ruler
set showtabline=2	" Always show tabline

au Bufenter *.\(c\|cpp\|h\|html\|css\|php\|ejs\|py\|rs\) set et
set ts=4
set autoindent
set nu
set smartindent
set shiftwidth=4
set laststatus=2	" Always show filename
set softtabstop=4

if v:version > 703
	try
		set list listchars=trail:·,tab:->,space:·
	catch
		set list listchars=trail:^,tab:->,space:^
	endtry
endif

""""""""""""""""""""""""""""
""   Common code snippets
""""""""""""""""""""""""""""
ab Inc #include 
ab pf printf(
ab sf scanf(
ab im int main(int argc, char *argv[]){
ab rt0 return 0;

autocmd Bufenter *.\(js\) setlocal shiftwidth=2 expandtab ts=2 softtabstop=2
autocmd Filetype html setlocal ts=2 softtabstop=2
autocmd Filetype json setlocal shiftwidth=2 ts=2 softtabstop=2 expandtab
" reopening a file for old versions - from /etc/vim/vimrc
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

autocmd BufReadPost *.qml set syntax=javascript expandtab ts=2 softtabstop=2

""""""""""""""""""""""""
""     Themes
""""""""""""""""""""""""
colorscheme elflord
hi Comment cterm=bold

if exists('+colorcolumn')
	au BufNewFile,BufRead *.\(h\|c\|cpp\|py\|js\|rs\) set colorcolumn=81
endif

""""""""""""""""""""""""
""     Highlights
""""""""""""""""""""""""
highlight WhiteSpace ctermfg=darkgrey
match WhiteSpace /\s/
highlight TabLineFill ctermfg=grey
highlight TabLine ctermfg=black ctermbg=grey
highlight TabLineSel ctermfg=white ctermbg=black

""""""""""""""""""""""""
""     Filetype
""""""""""""""""""""""""
au BufNewFile,BufRead *.ejs set filetype=html

""""""""""""""""""""""""
""     Addons
""""""""""""""""""""""""
if filereadable(expand("~/.vim/autoload/pathogen.vim"))
	execute pathogen#infect()
endif

""""""""""""""""""""""""
""     Mapping
""""""""""""""""""""""""
:map \\ :set number!<CR>
" Move to previous tab
:map \[ :tabp<CR>
" Move to next tab
:map \] :tabn<CR>

""""""""""""""""""""""""
""     Functions
""""""""""""""""""""""""
" MakeCGuard: Return C header guard format by filename
function MakeCGuard()
	let filename=expand('%:t')
	let guard=system('python3 -c "print(\"_' . filename . '\".upper().replace(\".\", \"_\").replace(\"-\", \"_\"), end=\"\")"')
	return guard " ex) _HEADER_H
endfunction
" MakeCHeaderComment: Return C header comment template
function MakeCHeaderComment()
	let filename=expand('%:t')
	let c_date=system('python3 -c "import time; print(time.strftime(\"%Y. %m. %d. %H:%M\", time.localtime()), end=\"\")"')
	let template="/*\n//  " . filename . "\n//\n" . "//  Author:     <OWNER>\n" . "//  Created:    " . c_date . "\n" . "//  Copyright (c) 2021 <OWNER>. All rights reserved.\n" . "//\n" . "//\n" . "*/"
	return template
endfunction
" MakeCExternCStart: Return extern C with __cplusplus def
function MakeCExternCStart()
	let externc="#ifdef __cplusplus\nextern \"C\" {\n#endif // __cplusplus"
	return externc
endfunction
" MakeCExternCEnd: Return extern C end bracket with __cplusplus def
function MakeCExternCEnd()
	let externc="#ifdef __cplusplus\n}\n#endif // __cplusplus"
	return externc
endfunction

""""""""""""""""""""""""
""     Commands
""""""""""""""""""""""""
" Cguard: Make C header guard
command Cguard :execute "normal! i#ifndef " . MakeCGuard() . "#define " .MakeCGuard() . "#endif /* " . MakeCGuard() . " */"
" Cxxnamespace: Make C++ namespace
command -nargs=1 Cxxnamespace :execute "normal! inamespace " . "<args>" . " {} // namespace " . "<args>"
" Ccomment: Make C header comment
command Ccomment :0put=MakeCHeaderComment()
" Cexterncstart: Make start extern C
command Cexterncstart :execute "normal! i" . MakeCExternCStart()
" Cexterncend: Make end extern C
command Cexterncend :execute "normal! i" . MakeCExternCEnd()
