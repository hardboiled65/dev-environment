#!/usr/bin/env python3
import os, sys, shutil
from abc import ABC, abstractmethod

def print_intro(msg):
    print('=== {} ==='.format(msg))

def print_done():
    print('Done.\n')

def confirm(text, default_yes=False):
    select_text = '[y/N]'
    if default_yes:
        select_text = '[Y/n]'
    input_text = input('{} {}: '.format(text, select_text))
    input_text = input_text.lower()
    # Set default input.
    if input_text == '' and not default_yes:
        input_text = 'n'
    elif input_text == '' and default_yes:
        input_text = 'y'

    if input_text in ('y', 'yes',):
        return True
    return False

def unix_home():
    return os.getenv('HOME')

def windows_home():
    homepath = os.getenv('HOMEPATH')
    if homepath is None:
        homepath = ''
    return 'c:' + homepath

PLATFORM = ''
if sys.platform in ('win32', 'cygwin'):
    PLATFORM = 'windows'
elif sys.platform in ('linux'):
    PLATFORM = 'linux'
else:
    PLATFORM = 'macos'

PLATFORM_HOME = ''
if PLATFORM == 'windows':
    PLATFORM_HOME = windows_home()
else:
    PLATFORM_HOME = unix_home()

DEV_ENVIRONMENT_DIR = os.path.dirname(__file__)


class Setting(ABC):
    def platform(self) -> str:
        return PLATFORM

    def home(self) -> str:
        return PLATFORM_HOME

    @abstractmethod
    def check(self) -> bool:
        """Check if the program installed and ready to install settings."""
        pass

    @abstractmethod
    def install_method(self) -> str:
        """Install method. 'system' | 'tar' | 'flatpak'"""
        pass

    @abstractmethod
    def installed(self) -> bool:
        """Check if setting files installed."""
        pass

    @abstractmethod
    def conflicted(self) -> bool:
        """Check if files conflicted."""
        return True

    @abstractmethod
    def backup(self):
        pass

    @abstractmethod
    def install(self):
        pass


class Vim(Setting):
    def __init__(self):
        pass

    def check(self) -> bool:
        return shutil.which('vim') is not None

    def install_method(self) -> str:
        return 'system'

    def installed(self) -> bool:
        if os.path.islink((os.getenv('HOME') + '/.vimrc')):
            return True
        return False

    def conflicted(self) -> bool:
        if os.path.isfile(os.path.join(self.home(), '.vimrc')):
            return True
        return False

    def backup(self):
        if os.path.isfile(os.path.join(self.home(), '.vimrc')):
            shutil.move(os.path.join(self.home(), '.vimrc'),
                os.path.join(self.home(), '.vimrc.old'))

    def install(self):
        os.symlink(os.path.join(DEV_ENVIRONMENT_DIR, 'vimrc'),
            os.path.join(self.home(), '.vimrc'))


class Zsh(Setting):
    def __init__(self):
        pass

    def check(self) -> bool:
        return shutil.which('zsh') is not None

    def install_method(self) -> str:
        return 'system'

    def installed(self) -> bool:
        if os.path.isdir(os.path.join(self.home() + '.oh-my-zsh')):
            return True
        return False


class Code(Setting):
    def __init__(self) -> None:
        pass

    def check(self) -> bool:
        if self.platform() == 'macos':
            target_dir = os.path.join(self.home(), 'Library/Application Support/Code/User')
            if os.path.isdir(target_dir):
                return True
            else:
                return False
        elif self.platform() == 'linux':
            target_dir = ''
            if self.install_method() == 'tar':
                target_dir = os.path.join(self.home(), '.config/Code/User')
            elif self.install_method() == 'flatpak':
                target_dir = os.path.join(self.home(), '.var/app/com.visualstudio.code/config/Code/User')
            else:
                return False

            if os.path.isdir(target_dir):
                return True
            else:
                return False
        elif self.platform() == 'windows':
            return False    # TODO: Implementation.

    def install_method(self) -> str:
        if self.platform() in ('windows', 'macos'):
            return 'system'
        else:
            tar_path = os.path.join(self.hone(), '.config/Code/User')
            flatpak_path = os.path.join(self.home(), '.var/app/com.visualstudio.code')
            if os.path.isdir(tar_path):
                return 'tar'
            elif os.path.isdir(flatpak_path):
                return 'flatpak'
            else:
                return 'unknown'

    def installed(self) -> bool:
        settings_json = ''
        keybindings_json = ''

        if self.platform() == 'linux':
            target_dir = ''
            if self.install_method() == 'tar':
                target_dir = '.config/Code/User'
            elif self.install_method() == 'flatpak':
                target_dir = '.var/app/com.visualstudio.code/config/Code/User'
            settings_json = os.path.join(self.home(), target_dir, 'settings.json')
            keybindings_json = os.path.join(self.home(), target_dir, 'keybindings.json')

            if os.path.islink(settings_json) and os.path.islink(keybindings_json):
                return True
            return False
        elif self.platform() == 'macos':
            target_dir = 'Library/Application Support/Code/User'
            settings_json = os.path.join(self.home(), target_dir, 'settings.json')
            keybindings_json = os.path.join(self.home(), target_dir, 'keybindings.json')

            if os.path.islink(settings_json) and os.path.islink(keybindings_json):
                return True
            return False
        elif self.platform() == 'windows':
            return False


settings = {
    'vim': {
        'directory': {
            'linux': unix_home(),
            'macos': unix_home(),
            'windows': '',
        },
    },
    'zsh': {},
    'sublime3': {
        'directory': {
            'linux': os.path.join(unix_home(), '.config/sublime-text-3'),
            'macos': unix_home(),
            'windows': os.path.join(windows_home(), 'AppData/Roaming/Subline Text 3'),
        },
    },
    'vscode': {
        'directory': {
            'linux': os.path.join(unix_home(), '.config/Code/User'),
            'macos': os.path.join(unix_home(), 'Library/Application Support/Code/User'),
            'windows': '',
        },
        'files': [
            {
                'source': '.misc/vscode/settings.json',
                'target': 'settings.json',
            },
            {
                'source': '.misc/vscode/keybindings.json',
                'target': 'keybindings.json',
            },
        ],
    },
}

paths = {
    'SUBLIME_SETTINGS': '',
    'VIMRC': (os.getenv('HOME') + '/.vimrc'),
    'VSCODE_SETTINGS': '',
}
if sys.platform in ('win32', 'cygwin'):
    paths['SUBLIME_SETTINGS'] = 'c:' + os.getenv('HOMEPATH') + '/AppData/Roaming/Sublime Text 3'
elif sys.platform in ('linux'):
    paths['SUBLIME_SETTINGS'] = os.getenv('HOME') + '/.config/sublime-text-3'
    paths['VSCODE_SETTINGS'] = os.getenv('HOME') + '/.config/Code'

ZSH_INSTALLED = True if shutil.which('zsh') is not None else False
CURL_INSTALLED = True if shutil.which('curl') is not None else False
WGET_INSTALLED = True if shutil.which('wget') is not None else False
OH_MY_ZSH_CURL = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"'
OH_MY_ZSH_WGET = 'sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"'

# VIM config.
vim = Vim()

print_intro('VIM')

if vim.installed():
    print('.vimrc file is already linked')
    print_done()
elif vim.check():
    print('VIM settings ready to be installed.')
    if confirm('Install?', default_yes=True):
        if vim.conflicted():
            print('.vimrc file is already exists.')
            if confirm('Do you want to make backup?', default_yes=True):
                vim.backup()
                print('File moved: .vimrc => .vimrc.old')
        vim.install()
        print_done()
else:
    print('VIM is not ready. Aborted.')

# Sublime Text 3 settings.
print_intro('Sublime Text 3')

subl_fnames = os.listdir('.misc/sublime/')
subl_settings = 'Preferences.sublime-settings'
if os.path.isdir(paths['SUBLIME_SETTINGS']):
    if subl_settings in os.listdir(paths['SUBLIME_SETTINGS'] + '/Packages/User'):
        print('The settings file is already exists.')
        if confirm('Override?') is not True:
            confirm_input = 'n' # Default value is `N`.
    else:
        if confirm('Install?', default_yes=True) is not False:
            confirm_input = 'y' # Default value is `Y`.
    if confirm_input.lower() == 'y':
        print('Copying settings file ...')
        for subl_fname in subl_fnames:
            shutil.copy('.misc/sublime/' + subl_fname,
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
    if os.getenv('SHELL').find('zsh') < 0:
        print('It seems zsh is not current shell.')
        print('Try again with zsh.')
        print('Aborted.\n')
    elif not os.path.isdir(os.path.join(os.getenv('HOME'), '.oh-my-zsh')):
        # Not installed.
        print('Oh My Zsh is not installed.')
        if confirm('Install?', default_yes=True):
            install_cmd = ''
            if CURL_INSTALLED:
                install_cmd = OH_MY_ZSH_CURL
            elif WGET_INSTALLED:
                install_cmd = OH_MY_ZSH_WGET

            if install_cmd != '':
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

# VSCode settings.
print_intro('VSCode')

vscode_settings_json = os.path.join(paths['VSCODE_SETTINGS'],
    'User/settings.json')
if os.path.islink(vscode_settings_json):
    print('settings.json file is already linked.')
    print_done()

if not os.path.islink(vscode_settings_json) and \
        not os.path.isfile(vscode_settings_json):
    # Not linked, file not exists.
    if confirm('Install?', default_yes=True):
        for setting_file in settings['vscode']['files']:
            source_dir = os.path.join(PLATFORM_HOME, 'dev-environment')
            target_dir = settings['vscode']['directory'][PLATFORM]
            os.symlink(
                os.path.join(source_dir, setting_file['source']),
                os.path.join(PLATFORM_HOME, target_dir, setting_file['target'])
            )
        print_done()
    else:
        print('Aborted.\n')
elif not os.path.islink(vscode_settings_json) and \
        os.path.isfile(vscode_settings_json):
    # Not linked, file exists.
    if confirm('Local file exists. Override?', default_yes=False):
        for setting_file in settings['vscode']['files']:
            source_dir = os.path.join(PLATFORM_HOME, 'dev-environment')
            target_dir = settings['vscode']['directory'][PLATFORM]
            # Backup current files.
            shutil.move(
                os.path.join(target_dir, setting_file['target']),
                os.path.join(target_dir, setting_file['target'] + '.old')
            )
            os.symlink(
                os.path.join(source_dir, setting_file['source']),
                os.path.join(PLATFORM_HOME, target_dir, setting_file['target'])
            )
        print_done()
    else:
        print('Aborted.\n')
elif not os.path.isdir(paths['VSCODE_SETTINGS']):
    print('It seems VSCode is not installed in this system.')
    print_done()

