syntax on
set ruler

au Bufenter *.\(c\|cpp\|h\|html\|css\|php\) set et
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
