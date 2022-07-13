# PyNotes

Simple command line tool to take notes in your favorite (terminal) editor. The structure is quite simple, you can have different "directories" that are akin to different projects, and in each of those directories you will have your notes, saved as markdown files.

The ordering of the directories will depend on the last modified file, as they are ordered chronologically, meaning that your last modified file should always appear on top.

## Installation and tweaks

The dependencies are quite straightforward, and you might only need to install `npyscreen` for the script to work. Then, simply put an alias directing to where you downloaded the `pynotes.py` file and you should be ready to go.

The script will search for a directory under $HOME/.pynotes and create it if it does not exist (this is hard coded in the script but can easily be changed). It also needs the environment variable `EDITOR` to be set, in my case `nvim`, and I don't know how the script will work if it is an external editor (e.g., sublime text, gedit, or something similar).

In ` ~/.local/lib/python3.8/site-packages/npyscreen/wgmultiline.py` I had to edit line 447 to unbind the shortcut `n` as I wanted to use it for adding a new entry (for reference, this is the line `# ord('n'):       self.move_next_filtered,`).

Notes are saved as markdown files, located at {$HOME}/.pynotes (the directory will be created if it doesn't exist).

![](screenshots/example.mkv)

