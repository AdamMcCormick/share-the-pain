import sublime
from sublime_plugin import EventListener, TextCommand, WindowCommand

from .pain import yay, wtf, setReason

class Prompter(EventListener):
  def onLoad(self, view):
    pass

class WtfCommand(TextCommand):
  def run(self, view, args):
    pass

class YayCommand(TextCommand):
  def run(self, view, args):

    pass

class MuxCommand(TextCommand):
  def run(self, view, args):
    pass
