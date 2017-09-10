#!/usr/bin/env python3
import os, sys, shutil

def print_intro(msg):
    print('=== {} ==='.format(msg))
def print_done():
    print('Done.\n')

SUBLIME_SETTINGS_PATH = ''
if sys.platform in ('win32', 'cygwin'):
    SUBLIME_SETTINGS_PATH = os.getenv('HOMEPATH') + '/AppData/Roaming/Sublime Text 3'
ZSH_INSTALLED = True if shutil.which('zsh') is not None else False
CURL_INSTALLED = True if shutil.which('curl') is not None else False
WGET_INSTALLED = True if shutil.which('wget') is not None else False
OH_MY_ZSH_CURL = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"'
OH_MY_ZSH_WGET = 'sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"'

# Sublime Text 3 settings.
print_intro('Sublime Text 3')

subl_fname = 'Preferences.sublime-settings'
confirm = 'n'
if subl_fname in os.listdir(SUBLIME_SETTINGS_PATH + '/Packages/User'):
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
    shutil.copy('./' + subl_fname,
        SUBLIME_SETTINGS_PATH + '/Packages/User/' + subl_fname)
    print_done()
else:
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
