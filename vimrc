syntax on
set ruler

au Bufenter *.\(c\|cpp\|h\|html\|css\|php\|ejs\|py\|rs\) set et
set ts=4
set autoindent
set nu
set smartindent
set shiftwidth=4
set laststatus=2	" Always show filename
set softtabstop=4
if v:version > 703
	set list listchars=trail:^,tab:->,space:^
endif
ab Inc #include 
ab pf printf(
ab sf scanf(
ab im int main()
ab rt0 return 0;

autocmd Filetype html setlocal ts=2 softtabstop=2
" reopening a file for old versions - from /etc/vim/vimrc
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

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
	let template="/*\n//  " . filename . "\n//\n" . "//  Author:     <OWNER>\n" . "//  Created:    " . c_date . "\n" . "//  Copyright (c) 2018 <OWNER>. All rights reserved.\n" . "//\n" . "//\n" . "*/"
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
command Cguard :execute "normal! i#ifndef " . MakeCGuard() . "
" Ccomment: Make C header comment
command Ccomment :0put=MakeCHeaderComment()
" Cexterncstart: Make start extern C
command Cexterncstart :execute "normal! i" . MakeCExternCStart()
" Cexterncend: Make end extern C
command Cexterncend :execute "normal! i" . MakeCExternCEnd()