# PyNotes

Simple command line tool to take notes. Notes are saved as markdown files, located at {$HOME}/.pynotes (the directory will be created if it doesn't exist).

## Installation and tweaks

The dependencies are quite straightforward, and you might only need to install `npyscreen` for the script to work. Then, simply put an alias directing to the `pynotes.py` file and you should be ready to go.

The script will search for a directory under $HOME/.pynotes and create it if it does not exist (this is hard coded in the script but can easily be changed). It also needs the environment variable `EDITOR` to be set, in my case `nvim`, and I don't know how the script will work if it is an external editor (e.g., sublime text, gedit, or something similar).

In ` ~/.local/lib/python3.8/site-packages/npyscreen/wgmultiline.py` I had to edit line 447 to unbind the shortcut `n` as I wanted to use it for adding a new entry (for reference, this is the line `# ord('n'):       self.move_next_filtered,`).

