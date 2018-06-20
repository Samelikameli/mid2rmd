#!/usr/bin/python2
import midi
import sys
if len(sys.argv)!=2:
   print("Usage: midi")
   exit(1)
sourcename=sys.argv[1]
target=".".join(sourcename.split(".")[0:-1])
def getFrequency(toneId):
    return int(round(440*2**((float(toneId)-69)/12)))
pattern=midi.read_midifile(sourcename)
print(pattern)
if len(pattern)==0:
    print("No tracks")
#print(pattern)
resolution=pattern.resolution
tick=0
queue=[]
eventI=[]
keysignature=[]
notes=[]
current_note=[]
EOT=[]
for i in range(len(pattern)):
    queue.append(0)
    eventI.append(0)
    keysignature.append(0)
    notes.append([])
    current_note.append([0,0])
    EOT.append(False)
tick2ms=1
while False in EOT:
    for i in range(len(pattern)):
        #print("Track "+str(i))
        track=pattern[i]
        if queue[i]==0 and not EOT[i]:
            event=track[eventI[i]]
            print(event,tick)
            #raw_input()
            eventI[i]+=1
            #raw_input(event.name)
            if event.name=="Key Signature":
                keysignature[i]=[event.data[0],event.data[1]]
            if event.name=="End of Track":
                print("EOT")
                notes[i].append([current_note[i][0],tick-current_note[i][1]])
                EOT[i]=True
            if event.name=="Set Tempo":
                microseconds=int(hex(event.data[0])[2:]+hex(event.data[1])[2:]+hex(event.data[2])[2:],16)
            
                tick2ms=microseconds/(1000.0*resolution)
            if event.name=="Note On":
                print(event.data)
                print(current_note)
                notes[i].append([current_note[i][0],int(round((tick-current_note[i][1])*tick2ms))])
                if event.data[1]==0:
                    current_note[i]=[0,tick]
                else:
                    current_note[i]=[getFrequency(event.data[0]),tick]
            if event.name=="Note Off":
                notes[i].append([current_note[i][0],int(round((tick-current_note[i][1])*tick2ms))])
                current_note[i]=[0,tick]
            if not EOT[i]:
                queue[i]=track[eventI[i]].tick
        else:
            queue[i]-=1
    no_tick=False
    for i in queue:
        if i==0:
            no_tick=True
    if not no_tick:
        tick+=1
    no_tick=False

    #print(tick)
    #for event in track:
        #print(event)
        #if event.name=="Time Signature":
        #    timesignature=[event.data[0],event.data[1]**2,event.data[2],event.data[3]]
        #if event.name=="Key Signature":
        #    keysignature=[event.data[0],event.data[1]]
        #if event.name=="Set Tempo":
        #    microseconds=int(hex(event.data[0])[2:]+hex(event.data[1])[2:]+hex(event.data[2])[2:],16)
        #    
        #    tick2ms=microseconds/(1000.0*resolution)
        #    print(tick2ms)
        #if event.name=="Note On":
        #    duration=int(round(event.tick*tick2ms))
        #    if event.data[1]!=0:
        #        notes.append([0,duration])
        #    else:
        #        notes.append([getFrequency(event.data[0]),duration])
                #print(event.data[0])
                #print(getFrequency(event.data[0]))
print(notes)

for i in range(len(notes)):
    notes_single=notes[i]
    #magic number
    rmd="0600".decode("hex")
    if len(notes_single)!=0:
        rmd+="{0:0{1}x}".format(len(notes_single)*4-4,4).decode("hex")
        rmd+="{0:0{1}x}".format(0,4).decode("hex")
        rmd+="{0:0{1}x}".format(0,4).decode("hex")
        for note in notes_single:
            rmd+="{0:0{1}x}".format(note[0],4).decode("hex")

            rmd+="{0:0{1}x}".format(min(note[1],65534),4).decode("hex")
        with open(target+str(i)+".rmd","wb") as f:
            print(target+str(i)+".rmd")
            f.write(rmd)