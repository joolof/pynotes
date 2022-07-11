#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import tempfile
import errno
import datetime
import subprocess
import npyscreen, curses
from pathlib import Path
"""
Some environment variables
"""
EDITOR = os.environ.get('EDITOR','vim') #that easy!
# os.environ['TERM']='xterm-256color' 
maindir = os.environ['HOME'] + '/.pynotes/'
if not os.path.isdir(maindir):
    os.mkdir(maindir)
"""
Some global variables for the formatting of the list
"""
lines, columns = os.popen('stty size', 'r').read().split()
lines, columns = int(lines), int(columns)
len_ellipsis = 60

class RecordList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
            "?": self.help,
            "a": self.new_directory,
            "n": self.new_entry,
            "d": self.delete_record,
            "r": self.refresh_view
        })

    def refresh_view(self,*args, **keywords):
        # npyscreen.notify_confirm(str(self.parent.value), title= 'popup')
        self.parent.update_list()

    def help(self, *args, **keywords):
        text = 'Shortcuts:\n'
        text += '  - \"Enter\": Expand the directory\n'
        text += '  - \"a\": Create a new "directory"\n'
        text += '  - \"n\": Create a new entry in the directory\n'
        text += '  - \"d\": Delete the whole directory\n'
        text += '  - \"r\": Refresh the list\n'
        text += '  - \"q\": Quit\n'
        npyscreen.notify_confirm(text)

    def display_value(self, vl):
        """
        Method to format how to display each individual entry
        """
        if vl[1] == 0:
            entry = '+ ' + vl[0] + '  [{}]'.format(vl[3])
        else:
            entry = ' '*5 + '- ' + vl[0]
        return "%s" % (entry)

    def actionHighlighted(self, act_on_this, keypress):
        if act_on_this[1] == 0:
            cline = self.values[self.cursor_line][2]
            if self.parent.dirname == '':
                self.parent.dirname = self.values[self.cursor_line][0]
            else:
                if self.parent.dirname == self.values[self.cursor_line][0]:
                    self.parent.dirname = ''
                else:
                    self.parent.dirname = self.values[self.cursor_line][0]
            self.cursor_line = cline
        else:
            filename = maindir + self.parent.dirname + '/' + act_on_this[0] + '.md'
            with tempfile.NamedTemporaryFile(suffix = '.md', dir = os.path.dirname(filename)) as tf:
                if os.path.isfile(filename):
                    f = open(filename, 'r')
                    initial_message = str.encode(f.read())
                    f.close
                else:
                    initial_message = b"" # if you want to set up the file somehow
                tf.write(initial_message)
                tf.flush()
                subprocess.call([EDITOR, tf.name])
                try:
                    os.link(tf.name, filename)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        os.remove(filename)
                        os.link(tf.name, filename)
                    else:
                        raise e
            npyscreen.blank_terminal()
            self.parent.DISPLAY()
            self.parent.dirname = ''
            self.cursor_line = 0
        self.parent.update_list()

    def new_directory(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').dir = True
        self.parent.parentApp.switchForm('EDITRECORDFM')
        self.parent.dirname = ''

    def new_entry(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').dir = False
        self.parent.parentApp.getForm('EDITRECORDFM').which_dir = self.values[self.cursor_line][0]
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def delete_record(self, *args, **keywords):
        if self.parent.dirname == '':
            filename = self.values[self.cursor_line][0]
        else:
            if self.parent.dirname == self.values[self.cursor_line][0]:
                filename = self.values[self.cursor_line][0]
            else:
                filename = self.parent.dirname + '/' + self.values[self.cursor_line][0] + '.md'
        message_to_display = 'Do you want to delete {}?'.format(filename)
        notify_result = npyscreen.notify_ok_cancel(message_to_display, title= '')
        # npyscreen.notify_confirm(filename, title= 'popup')
        if notify_result:
            args = ['rm', '-rf', maindir + filename]
            rmfile = subprocess.Popen(args, stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w')).wait()
        self.parent.update_list()


class RecordListDisplay(npyscreen.FormBaseNew):
    def create(self):
        new_handlers = {
            "q": self.exit_func
        }
        self.add_handlers(new_handlers)
        y, x = self.useable_space()
        self.dirname = ''
        self.InputBox = self.add(RecordList)

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        directories = list(Path(maindir).rglob('*'))
        directories.sort(key=lambda x: os.path.getmtime(x))
        directories = directories[::-1]
        values = []
        indice = 0
        for directory in directories:
            if os.path.isdir(maindir + directory.name):
                files = list(Path(maindir + directory.name+'/').rglob('*'))
                files.sort(key=lambda x: os.path.getmtime(x))
                files = files[::-1]
                values.append((directory.name, 0, indice, len(files)))
                indice += 1
                if directory.name == self.dirname:
                    files = list(Path(maindir + self.dirname+'/').rglob('*'))
                    files.sort(key=lambda x: os.path.getmtime(x))
                    files = files[::-1]
                    for file in files:
                        values.append((file.name.replace('.md',''), 1))
        self.InputBox.values = values
        self.InputBox.display()

    def exit_func(self, _input):
        npyscreen.blank_terminal()
        # os.system('cls' if os.name == 'nt' else 'clear')
        exit(0)


class EditRecord(npyscreen.ActionPopup):
    def create(self):
        self.show_aty = 1
        self.defaults_lines = 4
        self.dir = True
        self.which_dir = None
        self.wgEntry = self.add(npyscreen.TitleText, name = "Entry:", begin_entry_at = 12)

    def beforeEditing(self):
        self.wgEntry.value = ''

    def on_ok(self):
        if self.dir:
            os.mkdir(maindir + self.wgEntry.value)
        else:
            args = ['touch', maindir + self.which_dir + '/' + self.wgEntry.value + '.md']
            open_pdf = subprocess.Popen(args, stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))
            # npyscreen.notify_confirm(self.which_dir, title= 'popup')
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class NotesApp(npyscreen.NPSAppManaged):

    def onStart(self):
        # npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)
        # npyscreen.setTheme(npyscreen.Themes.TransparentThemeDarkText) # yata!
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme) # me gusta
        self.MainForm = self.addForm("MAIN", RecordListDisplay, framed = 1, name = 'PyNotes')
        self.addForm("EDITRECORDFM", EditRecord)


if __name__ == '__main__':
    myApp = NotesApp()
    myApp.run()

