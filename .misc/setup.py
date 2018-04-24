#!/usr/bin/env python3
import os, sys, shutil

def print_intro(msg):
    print('=== {} ==='.format(msg))
def print_done():
    print('Done.\n')

paths = {'SUBLIME_SETTINGS': ''}
if sys.platform in ('win32', 'cygwin'):
    paths['SUBLIME_SETTINGS'] = 'c:' + os.getenv('HOMEPATH') + '/AppData/Roaming/Sublime Text 3'
elif sys.platform in ('linux'):
    paths['SUBLIME_SETTINGS'] = os.getenv('HOME') + '/.config/sublime-text-3'
ZSH_INSTALLED = True if shutil.which('zsh') is not None else False
CURL_INSTALLED = True if shutil.which('curl') is not None else False
WGET_INSTALLED = True if shutil.which('wget') is not None else False
OH_MY_ZSH_CURL = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"'
OH_MY_ZSH_WGET = 'sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"'

# Sublime Text 3 settings.
print_intro('Sublime Text 3')

subl_fnames = os.listdir('sublime/')
subl_settings = 'Preferences.sublime-settings'
confirm = 'n'
if os.path.isdir(paths['SUBLIME_SETTINGS']):
    if subl_settings in os.listdir(paths['SUBLIME_SETTINGS'] + '/Packages/User'):
        print('The settings file is already exists.')
        confirm = input('Override? [y/N]: ')
        if confirm not in ('y', 'Y'):
            confirm = 'n' # Default value is `N`.
    else:
        confirm = input('Install? [Y/n]: ')
        if confirm not in ('n', 'N'):
            confirm = 'y' # Default value is `Y`.
    if confirm.lower() == 'y':
        print('Copying settings file ...')
        for subl_fname in subl_fnames:
            shutil.copy('./sublime/' + subl_fname,
                paths['SUBLIME_SETTINGS'] + '/Packages/User/' + subl_fname)
        print_done()
    else:
        print_done()
else:
    print('It seems Sublime Text 3 is not installed in this system.')
    print_done()

# Oh My Zsh.
print_intro('Oh My Zsh')

if ZSH_INSTALLED:
    if os.getenv('ZSH') is None:
        print('It seems zsh is not current shell.')
        print('Try again with zsh.')
        print('Aborted.\n')
    elif not os.path.isdir(os.getenv('ZSH')):
        # Not installed.
        print('Oh My Zsh is not installed.')
        confirm = input('Install? [Y/n]: ')
        if confirm not in ('n', 'N'):
            confirm = 'y' # Default value is `Y`
        if confirm.lower() == 'y':
            install_cmd = ''
            if CURL_INSTALLED:
                install_cmd = OH_MY_ZSH_CURL
            elif WGET_INSTALLED:
                install_cmd = OH_MY_ZSH_WGET

            if install_cmd is not '':
                cmd = 'cd ~ ; ' + install_cmd
                os.system(cmd)
                print_done()
            else:
                # Cannot install.
                print('Neither `curl` nor `wget` installed.')
                print('Aborted.\n')
        else:
            print_done()
    else:
        # Installed.
        print('Oh My Zsh is already installed.')
        print_done()
else:
    print('zsh is not installed yet.')
    print('Aborted.\n')
