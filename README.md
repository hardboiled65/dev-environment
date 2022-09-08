dev-environment
===============
personal dotfiles and other config files for unix or Linux

Files
-----

### bashrc
for bash shell

### zshrc
for zsh. Symlink to `~/.zshrc`.

For local environments, create `~/.zshrc.local` file.

Because it uses internal theme, run `./zshtheme.sh` to install the theme
before symlink this file.

### vimrc
for vim

### misc/
not always used. however, the files may needed some specific situations

### prompt.sh
[deprecated]will executed by .bashrc for set PS1 environment variable

### manual/
Various manuals as plain text file

### bin/
Useful executable files

- **path**: Print each path on one line.
- **install-rust**: Install Rust toolchain.
- **battery**: Print battery percentage for laptop.

### Xresources
For xterm. Symlink to `~/.Xresources`

Installation
------------

Python 3 required.

```sh
$ ./setup.py
```

For oh-my-zsh
```sh
$ export SHELL=/bin/zsh
```

