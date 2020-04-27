# Guild Wars 2 MIDI-to-Harp Script

To use this, you must have [Python 3](https://www.python.org/), [Music21](https://web.mit.edu/music21/), and [AutoHotkey](https://www.autohotkey.com/) installed. You must also have an environment to run Python scripts in! I recommend [VSCode](https://code.visualstudio.com/) if you don't have one already.
Instructions are printed to the terminal, so all you have to do is follow along for the most part. Before you start, set up the keybinds.txt file with your keybinds for the 10 abilities. If you had the default keybinds, the file would read "1234567890". The
Notes about selecting a track and removing notes:
* Many MIDIs simply will not work or will be quite painful to get to work with this script. Try to find a MIDI where the *main* piece of the music is in its own track.
* For a track to work, it must fit into a key. This means the track must follow 3 rules:
    1. There must be no more than 7 notes in the track.
    2. There can't be both sharps (notated as #) and flats (notated as -) in the same track.
    3. There can't be two versions of the same note in the track. For example, there can't be both a C and a C#.
* The strategy that worked for me is to compare the sharp and flat notes to their duplicate counterparts, and remove whichever one is used less.
The script does end with an index out of range. It works perfectly fine and I'm too lazy to fix it. The Python script will generate a .ahk (AutoHotkey) file that starts with sleeping for 5 seconds. Use this time to tab into GW2 and make sure you're on the right octave. To determine which octave to start on, just look at the list of octaves. The first octave in that list is what octave the first note is in. For example, if the octaves are 4, 3, 5 then start in the harp's middle octave. If there are more than 3 octaves, decide which octave you don't want. Use the number of notes in each octave to figure that out. For example, if the octaves are 4, 3, 5, 2 then figure out whether 2 or 5 has less notes. If 5 has less notes, start in the harp's higher octave. If 2 has less notes, start in the harp's middle octave.
I included the MIDIs I got to work and their corresponding scripts in the two separate folders. If you want to use a script I generated, just Find-and-Replace each keybind with your own. If you have default keybinds, replace c with 6, e with 7, r with 8, t with 9, and q with 0.
