# PyNotes

https://user-images.githubusercontent.com/22960520/178684031-107cd1be-479b-47f0-aacf-5d5267b613e7.mp4

Simple command line tool to take notes in your favorite (terminal) editor. The structure is quite simple, you can have different "directories" that are akin to different projects, and in each of those directories you will have your notes, saved as markdown files.

The ordering of the directories will depend on the last modified file, as they are ordered chronologically, meaning that your last modified file should always appear on top.

## Installation and tweaks

The dependencies are quite straightforward, and you might only need to install `npyscreen` for the script to work. Then, simply put an alias directing to where you downloaded the `pynotes.py` file and you should be ready to go.

The script will search for a directory under $HOME/.pynotes and create it if it does not exist (this is hard coded in the script but can easily be changed). It also needs the environment variable `$EDITOR` to be set, in my case `nvim`, and I don't know how the script will work if it is an external editor (e.g., sublime text, gedit, or something similar).

One small detail, I wanted to use the letter `n` to create a new not, and this shortcut is reserved by `npyscreen` to do something else. To avoid this, in ` ~/.local/lib/python3.8/site-packages/npyscreen/wgmultiline.py` I had to comment out line 447 to unbind the shortcut (for reference, this is the line `# ord('n'):       self.move_next_filtered,`).

## Shortcuts

Once you are in PyNotes, you can press `?` to display a window with the shortcuts:

- "Enter": Expand or collapse the highlighted directory
- "a": Create a new directory
- "n": Create a new file in the directory
- "d": Delete the whole directory or the selected file (there will be a confirmation window)
- "r": Refresh the list
- "q": Quit




