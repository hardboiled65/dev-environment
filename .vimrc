syntax on
set ruler

au Bufenter *.\(c\|cpp\|h\|html\|css\|php\|py\) set et
set ts=4
set autoindent
set nu
set smartindent
set shiftwidth=4
ab Inc #include 
ab stdio stdio.h
ab pf printf(
ab sf scanf(
ab im int main(){
ab rt0 return 0;

hi Comment cterm=bold

function MakeCGuard()
	let filename=expand('%:t')
	let guard=system('python3 -c "print(\"_' . filename . '\".upper().replace(\".\", \"_\"), end=\"\")"')
	return guard " ex) _HEADER_H
endfunction

" Cguard: Make C header guard
command Cguard :execute "normal! i#ifndef " . MakeCGuard() . "#define " .MakeCGuard() . "#endif /* " . MakeCGuard() . " */"
