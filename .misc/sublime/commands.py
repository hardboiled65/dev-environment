import sublime
import sublime_plugin
from sublime_plugin import TextCommand
from sublime import Region

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")

class CShortBannerCommand(TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        current = sel[0].begin()
        line = self.view.line(current)
        length = line.end() - line.begin()

        upper = '/*==' + ('-' * (length - 1))
        bottom = '/' + ('-' * (length - 1)) + '==*/'

        added = self.view.insert(edit, line.begin(), upper + '\n/ ')
        line = Region(line.begin() + added, line.end() + added)
        self.view.insert(edit, line.end(), '\n' + bottom)
