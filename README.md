# Guild Wars 2 MIDI-to-Harp Script

To use this, you must have [Python 3](https://www.python.org/), [Music21](https://web.mit.edu/music21/), and [AutoHotkey](https://www.autohotkey.com/) installed. You must also have an environment to run Python scripts in! I recommend [VSCode](https://code.visualstudio.com/) if you don't have one already.

The script requires there to be exactly one .mid file in the same directory. If there isn't one, you will get an index out of range. If there is more than one, it will simply use the first one it finds.  Instructions are printed to the terminal, so all you have to do is follow along for the most part. Before you start, set up the keybinds.txt file with your keybinds for the 10 abilities. If you had the default keybinds, the file would read "1234567890".

Notes about selecting a track and removing notes:
* Many MIDIs simply will not work or will be quite painful to get to work with this script. Try to find a MIDI where the *main* piece of the music is in its own track.
* For a track to work, it must fit into a key. This means the track must follow 3 rules:
    1. There must be no more than 7 notes in the track.
    2. There can't be both sharps (notated as #) and flats (notated as -) in the same track.
    3. There can't be two versions of the same note in the track. For example, there can't be both a C and a C#.
* The strategy that worked for me is to compare the sharp and flat notes to their duplicate counterparts, and remove whichever one is used less.

The script will then ask you if you want to replace any octaves. This script requires there to be only 3 octaves, and they must be consecutive. If there are more than 3 octaves, decide which octave you don't want. Use the number of notes in each octave to figure that out. For example, if the octaves are 4, 3, 5, 2 then figure out whether 2 or 5 has less notes. If 5 has less notes, type "5 4" to shift all notes in octave 5 to octave 4. If 2 has less notes, type "2 3" instead. If the octaves are 6, 4, 2 then type "6 5" and "2 3".

The Python script will generate a .ahk (AutoHotkey) file that starts with sleeping for 5 seconds. Use this time to tab into GW2 and make sure you're on the middle octave. I included the MIDIs I got to work and their corresponding scripts in the two separate folders. If you want to use a script I generated, just Find-and-Replace each keybind with your own. If you have default keybinds, replace c with 6, e with 7, r with 8, t with 9, and q with 0. However, if you use a script that has a (#) at the end of the file name, you must start on that specific octave (1 for low, 2 for middle, and 3 for high). Newer scripts have this issue resolved.

The script will also generate a sheet music text file as long as the MIDI isn't too janky. Currently, it supports notes that are 0 to 9.75 quarter notes. Within each "quarter note section", it supports decimals of .25, .33, .5, .66, and .75. The sheet music may be horrible to read if the MIDI isn't great, so you may need to go in and custom edit some notes. The sheet music gives you pretty much all the information you should need to make any changes you'd like including tempo, the number of notes for each note type, and how long in milliseconds each note type is. If that isn't enough information for you, I encourage you to look more into Music21's documentation and edit my code. The MIDIs have pretty much everything in there if you look hard enough.

If you're getting an error stating list index out of range, you might be in the wrong directory. Make sure you're in the GW2-MIDI-to-Harp folder, and not the directory above.
