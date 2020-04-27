from music21 import converter, note, tempo
import glob

#gets the first .mid file in the directory and converts it to a Music21 score
score = converter.parse(glob.glob("./*.mid")[0])

#finds the tempo of the score
for p in score.flat.elements:
    if isinstance(p, tempo.MetronomeMark):
        tempo = p
        break
timeBetweenNotes = (1 / tempo.number) * 60 * 1000 #calculates the seconds between quarter notes

# finds all the instruments in the score
partStream = score.parts.stream()
for i in range(0, len(partStream)):
    print(i, end = ": ")
    print (partStream[i].partName)

#select the track
tracksSel = input("\nSelect which track you would like to play by typing in the corresponding number. To select multiple tracks, type them with a space between each number. For all tracks, type \"all\"\n").split()
if  not tracksSel or tracksSel[0] == "all":
    tracksToPlay = score.flat.elements
else:
    tracksToPlay = score.elements[int(tracksSel[0])]
    for t in range(1, len(tracksSel)):
        tracksToPlay += score.elements[int(tracksSel[t])]

#pull the notes from the midi
notes = []
for p in tracksToPlay: #pulls notes from selected tracks
    if isinstance(p, note.Note):
        notes.append([p.name, p.octave, p.quarterLength]) #functional, only one where the program actually works
        # notes.append(p.fullName) #somewhat readable while maintaining all necessary information
        # notes.append(p.name) #very readable

print("\nAll notes in the track where the format is [<note name>, <octave>, <length in relation to a quarter note>]:")
print(notes)

#finds the range of octaves
octaves = []
for p in notes:
    if not p[1] in octaves:
        octaves.append(p[1])
octaveCount = []
for i in range(0, len(octaves)):
    count = 0
    for n in notes:
        if octaves[i] == n[1]:
            count += 1
    octaveCount.append(count)
print("The list of octaves with the number of notes in each octave, in order as they first appear in the song:")
for o in range (0, len(octaves)):
    print(str(octaves[o]) + ":\t" + str(octaveCount[o]))

#find the range of notes
songkey = set([])
for p in notes:
    if not p[0] in songkey:
        songkey.add(p[0])
songkeylist = list(songkey)
keyCount = []
for i in range(0, len(songkeylist)):
    count = 0
    for n in notes:
        if songkeylist[i] == n[0]:
            count += 1
    keyCount.append(count)
print("The list of notes with the number of times the note appears, in order as they first appear in the song:")
for n in range (0, len(songkeylist)):
    print(str(songkeylist[n]) + ":\t" + str(keyCount[n]))
print("There are " + str(len(songkeylist)) + " notes.")

#removes notes to fit into a specific major
print("Enter the notes you would like removed. To remove multiple notes, enter them with a space between each note. To remove no notes, simply hit enter.")
removedNotes = input().split()
it = 0
while it < len(notes):
    for r in removedNotes:
        if notes[it][0] == r:
            notes[it - 1][2] += notes[it][2]
            notes.pop(it)
            it -= 1
    it += 1
for r in removedNotes:
    songkey.remove(r)

#maps each keybind from the keybinds.txt file to the notes of c major
noteRange = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
keybinds = []
keybindsFile = open('keybinds.txt', 'r')
for i in range(0, 10):
    keybinds.append(keybindsFile.read(1))
keymap = {}
for i in range(0, 7):
    keymap[noteRange[i]] = keybinds[i]

#c minor transpose
noteRangeCMINOR = ['C', 'D', 'E-', 'F', 'G', 'A-', 'B-']
keymapCMINOR = {}
for i in range(0, 7):
    keymapCMINOR[noteRangeCMINOR[i]] = noteRange[i]

#f major transpose
noteRangeFMAJOR = ['F', 'G', 'A', 'B-', 'C', 'D', 'E']
keymapFMAJOR = {}
for i in range(0, 7):
    keymapFMAJOR[noteRangeFMAJOR[i]] = noteRange[i]

#d major transpose
noteRangeDMAJOR = ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']
keymapDMAJOR = {}
for i in range(0, 7):
    keymapDMAJOR[noteRangeDMAJOR[i]] = noteRange[i]

#g major transpose
noteRangeGMAJOR = ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
keymapGMAJOR = {}
for i in range(0, 7):
    keymapGMAJOR[noteRangeGMAJOR[i]] = noteRange[i]

#a major transpose
noteRangeAMAJOR = ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']
keymapAMAJOR = {}
for i in range(0, 7):
    keymapAMAJOR[noteRangeAMAJOR[i]] = noteRange[i]

#b flat major transpose
noteRangeBFMAJOR = ['B-', 'C', 'D', 'E-', 'F', 'G', 'A']
keymapBFMAJOR = {}
for i in range(0, 7):
    keymapBFMAJOR[noteRangeBFMAJOR[i]] = noteRange[i]

#autodetect the key
tmap = {}
cmajor = set(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
cminor = set(['C', 'D', 'E-', 'F', 'G', 'A-', 'B-'])
fmajor = set(['F', 'G', 'A', 'B-', 'C', 'D', 'E'])
dmajor = set(['D', 'E', 'F#', 'G', 'A', 'B', 'C#'])
gmajor = set(['G', 'A', 'B', 'C', 'D', 'E', 'F#'])
amajor = set(['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'])
bfmajor = set(['B-', 'C', 'D', 'E-', 'F', 'G', 'A'])

if songkey & cmajor == songkey:
    transpose = False
elif songkey & cminor == songkey:
    transpose = True
    tmap = keymapCMINOR
elif songkey & fmajor == songkey:
    transpose = True
    tmap = keymapFMAJOR
elif songkey & dmajor == songkey:
    transpose = True
    tmap = keymapDMAJOR
elif songkey & gmajor == songkey:
    transpose = True
    tmap = keymapGMAJOR
elif songkey & amajor == songkey:
    transpose = True
    tmap = keymapAMAJOR
elif songkey & bfmajor == songkey:
    transpose = True
    tmap = keymapBFMAJOR

#play the music
ahk = open("script.ahk", "w")
ahk.write("Sleep, 5000\n") #gives you time to tab into GW2
for i in range(0, len(notes)):
    noteTime = notes[i][2] * timeBetweenNotes
    if noteTime > 1500:
        noteTime = noteTime * 4 / 5
    if transpose: #play the note
        keypress = keymap[tmap[notes[i][0]]]
    else:
        keypress = keymap[notes[i][0]]
    ahk.write("SendInput, " + keypress + "\n")
    octaveDiff = notes[i][1] - notes[i + 1][1] #this index out of ranges, it's fine. your script is properly generated!
    if octaveDiff > 0:
        for i in range(0, octaveDiff):
            ahk.write("SendInput, " + keybinds[8] + "\n")
            ahk.write("Sleep, 1\n")
    elif octaveDiff < 0:
        for i in range(0, octaveDiff * -1):
            ahk.write("SendInput, " + keybinds[9] + "\n")
            ahk.write("Sleep, 1\n")
    ahk.write("Sleep, " + str(noteTime) + "\n") #wait before playing next note
