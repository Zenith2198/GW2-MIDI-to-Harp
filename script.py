from music21 import converter, note, tempo
from os import listdir
from statistics import mean

#gets the first .mid file in the directory and converts it to a Music21 score
score = converter.parse(list(f for f in listdir(".") if f.endswith(".mid"))[0])
# score = converter.parse("GW2-MIDI-to-Harp/" + str(list(f for f in listdir("GW2-MIDI-to-Harp") if f.endswith(".mid"))[0])) # for some reason if you run this in vscode it thinks it's in the directory above if you cloned from github. if this line throws an error, comment it out and uncomment the one before it. also do this with lines 137, 218, 291

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
    print(partStream[i].partName)

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
octaves = set([])
for p in notes:
    if not p[1] in octaves:
        octaves.add(p[1])
octaveslist = list(octaves)
octaveCount = []
for i in range(0, len(octaveslist)):
    count = 0
    for n in notes:
        if octaveslist[i] == n[1]:
            count += 1
    octaveCount.append(count)
print("The list of octaves with the number of notes in each octave, in order as they first appear in the song:")
for o in range (0, len(octaveslist)):
    print(str(octaveslist[o]) + ":\t" + str(octaveCount[o]))

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

#finds the range of octaves AGAIN functions are boring copypaste is WHERE ITS AT
octaves = set([])
for p in notes:
    if not p[1] in octaves:
        octaves.add(p[1])
octaveslist = list(octaves)
octaveCount = []
for i in range(0, len(octaveslist)):
    count = 0
    for n in notes:
        if octaveslist[i] == n[1]:
            count += 1
    octaveCount.append(count)
print("The new list of octaves with the number of notes in each octave, in order as they first appear in the song:")
for o in range (0, len(octaveslist)):
    print(str(octaveslist[o]) + ":\t" + str(octaveCount[o]))

#dealing with octaves jank
octaveReplaceMap = {}
while True:
    inp = input("Enter an octave you want replaced followed by the octave you want to replace it with, leaving a space between the two numbers. If you don't want to replace anything, just hit enter:\n")
    if not inp:
        break
    replacement = [int(i) for i in inp.split()]
    octaveReplaceMap[replacement[0]] = replacement[1]
for i in range(0, len(octaveslist)):
    if octaveslist[i] in octaveReplaceMap:
        octaveslist[i] = octaveReplaceMap[octaveslist[i]]
octaveslist = list(dict.fromkeys(octaveslist))

#find the range of notes AGAIN functions are boring copypaste is WHERE ITS AT
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

#maps each keybind from the keybinds.txt file to the notes of c major
noteRange = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
keybinds = []
keybindsFile = open('keybinds.txt', 'r')
# keybindsFile = open('GW2-MIDI-to-Harp/keybinds.txt', 'r') # if you're getting an error here, comment out this line and uncomment the one above
for i in range(0, 10):
    keybinds.append(keybindsFile.read(1))
keymap = {}
for i in range(0, 7):
    keymap[noteRange[i]] = keybinds[i]

sheetkeybinds = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
sheetkeymap = {}
for i in range(0, 7):
    sheetkeymap[noteRange[i]] = sheetkeybinds[i]

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

#write the ahk script
ahk = open("script.ahk", "w")
# ahk = open("GW2-MIDI-to-Harp/script.ahk", "w") #uncomment the one above if you got errors before :)
ahk.write("Sleep, 5000\n") #gives you time to tab into GW2
firstNoteO = notes[0][1] #allows you to start on middle octave in GW2
realFNO = firstNoteO if firstNoteO in octaveslist else octaveReplaceMap[firstNoteO]
if realFNO < mean(octaveslist):
    ahk.write("SendInput, " + keybinds[8] + "\n")
    ahk.write("Sleep, 1\n")
elif realFNO > mean(octaveslist):
    ahk.write("SendInput, " + keybinds[9] + "\n")
    ahk.write("Sleep, 1\n")
for i in range(0, len(notes)):
    noteTime = notes[i][2] * timeBetweenNotes
    if transpose: #play the note
        keypress = keymap[tmap[notes[i][0]]]
    else:
        keypress = keymap[notes[i][0]]
    ahk.write("SendInput, " + keypress + "\n")
    if i < len(notes) - 1: #change octaves
        note1 = notes[i][1]
        note2 = notes[i + 1][1]
        octaveDiff = (note1 if note1 in octaveslist else octaveReplaceMap[note1]) - (note2 if note2 in octaveslist else octaveReplaceMap[note2]) #deals with octaves jank
        if octaveDiff > 0:
            for i in range(0, octaveDiff):
                ahk.write("SendInput, " + keybinds[8] + "\n")
                ahk.write("Sleep, 1\n")
        elif octaveDiff < 0:
            for i in range(0, octaveDiff * -1):
                ahk.write("SendInput, " + keybinds[9] + "\n")
                ahk.write("Sleep, 1\n")
        ahk.write("Sleep, " + str(noteTime) + "\n") #wait before playing next note
ahk.close()
print("Your script has been generated!")

#write sheet music
noteTypes = {}
for n in notes:
    if not n[2] in noteTypes:
        noteTypes[float(str(float(n[2]))[:4])] = 1
    else:
        noteTypes[n[2]] = noteTypes[n[2]] + 1
ntList = []
for n in noteTypes:
    ntList.append(float(str(n)[:4]))
ntList.sort()
ntMap = {}
for nt in ntList:
    nts = str(nt)
    tempString = ""
    if nts[:1] == "1":
        tempString += " "
        if nts == "1.0":
            ntMap[nt] = tempString
            continue
    else:
        for i in range(1, int(nts[:1])):
            tempString += "\n"
    if int(nts[2:]) % 25 == 0:
        if int(nts[2:]) / 25 == 1:
            tempString += "/"
        elif int(nts[2:]) / 25 == 2:
            tempString += "-"
        elif int(nts[2:]) / 25 == 3:
            tempString += "_"
    if int(nts[2:]) % 33 == 0:
        if int(nts[2:]) / 33 == 1:
            tempString += "!"
        elif int(nts[2:]) / 33 == 2:
            tempString += "@"
    if nts[:1] == "1":
        tempString += " "
    ntMap[nt] = tempString

sheet = open("sheet.txt", "w")
# sheet = open("GW2-MIDI-to-Harp/sheet.txt", "w") #uncomment the one above if you got errors before :)
sheet.write("[] = lower octave\n() = higher octave\ntempo = " + tempo.text + " " + str(tempo.number) + "\n")
for i in range(0, len(ntList)):
    sheet.write("a")
    sheet.write(ntMap[ntList[i]])
    sheet.write("b = " + str(ntList[i]) + " quarter notes long (" + str(ntList[i] * timeBetweenNotes) + " ms)\t\t" + str(noteTypes[ntList[i]]))
    if noteTypes[ntList[i]] == 1:
        sheet.write(" note\n")
    else:
        sheet.write(" notes\n")
sheet.write("\n")
sheet.write("Sheet music:\n")
mode = mean(octaveslist) #for notation
if realFNO < mean(octaveslist):
    sheet.write("[")
    mode = realFNO
elif realFNO > mean(octaveslist):
    sheet.write("(")
    mode = realFNO
for i in range(0, len(notes)):
    noteTime = ntMap[float(str(float(notes[i][2]))[:4])]
    if transpose: #play the note
        keypress = keymap[tmap[notes[i][0]]]
    else:
        keypress = keymap[notes[i][0]]
    sheet.write(keypress)
    if i < len(notes) - 1: #change octaves
        note1 = notes[i][1]
        note2 = notes[i + 1][1]
        octaveDiff = (note1 if note1 in octaveslist else octaveReplaceMap[note1]) - (note2 if note2 in octaveslist else octaveReplaceMap[note2]) #deals with octaves jank

        #i hate notation
        if octaveDiff:
            if mode < mean(octaveslist):
                if octaveDiff == -1:
                    sheet.write("]" + noteTime)
                    mode =  mean(octaveslist)
                elif octaveDiff == -2:
                    sheet.write("]" + noteTime + "(")
                    mode =  mean(octaveslist) + 1
            elif mode > mean(octaveslist):
                if octaveDiff == 1:
                    sheet.write(")" + noteTime)
                    mode =  mean(octaveslist)
                elif octaveDiff == 2:
                    sheet.write(")" + noteTime + "[")
                    mode =  mean(octaveslist) - 1
            else:
                if octaveDiff == 1:
                    sheet.write(noteTime + "[")
                    mode =  mean(octaveslist) - 1
                elif octaveDiff == -1:
                    sheet.write(noteTime + "(")
                    mode =  mean(octaveslist) + 1
        else:
            if "\n" in noteTime:
                if mode < mean(octaveslist):
                    sheet.write("]" + noteTime + "[")
                elif mode > mean(octaveslist):
                    sheet.write(")" + noteTime + "(")
            else:
                sheet.write(noteTime)
if octaveDiff: #final notation mark
    if mode < mean(octaveslist):
        sheet.write("]")
    elif mode > mean(octaveslist):
        sheet.write(")")
sheet.close()
print("Your sheet music has been generated!")
