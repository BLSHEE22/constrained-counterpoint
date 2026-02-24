import random
import time
import subprocess
import shutil
from config import *
from constraint import *


# solve for CF based on first species counterpoint rules
def make_cantus_firmus(cfLength, scale):
    #print("Starting cantus firmus creation sequence...\n")
    p = Problem()
    #print("Adding variables...")
    for i in range(1, cfLength+1):
        p.addVariable(i, scales[scale])
    #print(f'\'{scale} scale\' added.')
    #print("Variables added.\n")
    #print("Adding constraints...")
    # START AND END ON TONIC
    for j in range(1, cfLength+1):
        if j == 1 or j == cfLength:
            p.addConstraint(lambda x: x == 0, [j])
    #print("\'Start and end on tonic\' constraint added.")
    # PENULTIMATE TONE IS LEADING TONE/SUPERTONIC
    for j in range(1, cfLength+1):
        if j == cfLength-1:
            p.addConstraint(lambda x: x == -1 or x == 2, [j])
    #print("\'Penultimate note leading tone/supertonic\' constraint added.")
    # LEADING TONE ALWAYS LEADS TO TONIC
    for j in range(1, cfLength+1):
        if j > 1:
            p.addConstraint(lambda x,y: y == 0 if x == -1 else (y == 12 if x == 11 else y), [j-1,j])            
    #print("\'Leading tone leads to tonic\' constraint added.")
    # ALWAYS RESOLVE LEAPS BY STEP IN OPPOSITE DIRECTION
    for j in range(1, cfLength+1):
        if j > 2:
            p.addConstraint(lambda x,y,z: z == scales[scale][scales[scale].index(y)+1] if abs(x-y) > 2 and x>y else (z == scales[scale][scales[scale].index(y)-1] if abs(x-y) > 2 and x<y else z), [j-2,j-1,j])
    #print("\'Resolve leaps by step in opposite direction\' constraint added.")
    # NO DISSONANT LEAPS OR STATIC MOTION
    for j in range(1, cfLength+1):
        if j != cfLength:
            p.addConstraint(lambda x,y: abs(x-y) < 17 and abs(x-y) != 16 and abs(x-y) != 15 and abs(x-y) != 14 and abs(x-y) != 13 and abs(x - y) != 12 and abs(x-y) != 11 and abs(x-y) != 10 and abs(x-y) != 7 and abs(x - y) != 6 and abs(x - y) != 0, (j, j+1))
    #print("\'No dissonant leaps or static motion\' constraint added.")
    #print("Constraints added.\n")
    #print(f'Finding all {cfLength}-note cantus firmi that meet the requirements...\n')
    solutions = p.getSolutions()
    #print(f'{len(solutions)} found!\n')
    #print("Choosing a random solution...\n")
    randomSolution = random.choice(solutions)
    print(f"Cantus firmus: {[f"{val:2}" for k, val in (sorted(dict(randomSolution).items()))]}")
    return randomSolution


# solve for bassline given CF
def make_bass(cf, cfLength, scale):
    #print("Starting bass creation sequence...")
    p = Problem()
    for i in range(1, cfLength+1):
        p.addVariable(i, scales[scale])
    #print(f'\'{scale} scale\' added.')
    #print("Variables added.\n")
    #print("Adding constraints...")
    # CONSTRAINTS
    for j in range(1, cfLength+1):
        if j == 1 or j == cfLength:
            # START AND END ON TONIC
            p.addConstraint(lambda x: x == 0, [j])
        elif j == cfLength-1:
            # PENULTIMATE TONE IS LEADING TONE/SUPERTONIC/DOMINANT
            p.addConstraint(lambda x: (x == -1 or x == 2 or x == -5 or x == 7) and x != cf[cfLength-1], [j])
        else:
            # NO m2, M2, P4, b5, m7 or M7
            p.addConstraint(lambda val, k=j: (cf[k]-val)%12 in [0, 3, 4, 7, 8, 9], [j])
            # NO PARALLEL OCTAVES/DISSONANCES
            p.addConstraint(lambda prev_val, curr_val, i=j: not (((cf[i-1] - prev_val)%12 in disallowed_parallel_intervals) and
                                                                 ((cf[i] - curr_val)%12 in disallowed_parallel_intervals)), [j-1, j])
            # NO DISSONANCES BY SIMILAR MOTION
            cf_up   = cf[j-1] < cf[j]
            cf_down = cf[j-1] > cf[j]
            p.addConstraint(lambda prev_val, curr_val, i=j, CF_up=cf_up, CF_down=cf_down: not (
                        (
                            (CF_up   and prev_val < curr_val) or
                            (CF_down and prev_val > curr_val)
                        )
                        and
                        ((cf[i] - curr_val)%12 in disallowed_parallel_intervals)
                    ),
                [j-1, j]
            )
            if j == cfLength-2:
                # prepare the V-I with a consonance (preferably a predominant)
                p.addConstraint(lambda val, k=j: (cf[k]-val)%12 not in disallowed_parallel_intervals, [j])
            #p.addConstraint(lambda val, prev, y=j: if cf[k-1] cf_i   else val, (j-1, j))
            #p.addConstraint(lambda x: x in scales[scale][2:9], [j])

    # ALWAYS RESOLVE LEAPS BY STEP IN OPPOSITE DIRECTION
    for j in range(1, cfLength):
        if j > 2:
            p.addConstraint(lambda x,y,z: z == scales[scale][scales[scale].index(y)+1] if abs(x-y) > 2 and x>y else (z == scales[scale][scales[scale].index(y)-1] if abs(x-y) > 2 and x<y else z), [j-2,j-1,j])
    #print("\'Resolve leaps by step in opposite direction\' constraint added.")
    # NO DISSONANT LEAPS OR STATIC MOTION
    for j in range(1, cfLength+1):
        if j != cfLength:
            p.addConstraint(lambda x,y: abs(x-y) < 17 and abs(x-y) != 16 and abs(x-y) != 15 and abs(x-y) != 14 and abs(x-y) != 13 and abs(x-y) != 11 and abs(x - y) != 6 and abs(x - y) != 0, (j, j+1))
    #print("\'No dissonant leaps or static motion\' constraint added.")
    # NO PARALLEL FOURTHS, FIFTHS, AND OCTAVES
    
    solutions = p.getSolutions()
    randomSolution = random.choice(solutions)
    print(f"Counterpoint:  {[f"{val:2}" for k, val in (sorted(dict(randomSolution).items()))]}")
    return randomSolution


# translate melody notes to LilyPond symbols
def lilyize(solution, offset=0, part="cf"):
    notes = []
    if part == "cf":
        notes = [n+12+offset for k, n in sorted(solution.items())]
    elif part == "bass":
        notes = [n-12+offset for k, n in sorted(solution.items())]
    return melToLily(notes, majScales[0])


# helper function
def melToLily(mel, sc):
    lilyMelody = []
    i = 0
    while i < len(mel):
        semis = mel[i]
        s = ""
        if semis < -12:
            while semis < -12:
                s += ","
                semis += 12
            semis = mel[i]
        while semis > -1:
            s += "'"
            semis -= 12
        # whole note
        s += "1"
        lilyMelody.append(sc[mel[i]%12] + s)
        i += 1

    # put together return string
    mel = [sc[x%12] for x in mel]
    retStr = ""
    for x in lilyMelody:
        retStr += x + " "

    return retStr


# write the lilyPond code to output file
def write_lilyfile(scale, offset, bpm, cf, bass):
    code = "\\version \"2.22.4\"\n"
    code += "\\header{\n  title = \"" + "First Species Counterpoint in " + scaleStartTrans[scale[offset]] + " Major\"\n}\n\n"
    code += "\\score {\n"
    code += "\\new PianoStaff <<\n"
    code += "\\" + "new Staff { \\" + "set Staff.midiInstrument = \"" + INSTRUMENT + "\" \\" + "clef \"treble\" \\key  " + scale[offset] + "\\" + "major " + "\\tempo 4 = " + str(bpm) + " " + cf + "}\n"
    code += "\\" + "new Staff { \\" + "set Staff.midiInstrument = \"" + INSTRUMENT + "\" \\" + "clef \"bass\" \\key " + scale[offset] + "\\" + "major " + bass + "}\n"
    code += ">>\n"
    code += "\\layout{}\n"
    code += "\\midi{}\n"
    code += "}\n"
    f = open("first_species.ly", "w")
    f.write(code)
    f.close()


# MAIN
def main():
    print("Get ready for some counterpoint!\n")
    offset = random.randrange(0, 11)
    chosen_scale = majScales[offset]
    print(f"Key: {scaleStartTrans[chosen_scale[offset]]}\n")
    cf = make_cantus_firmus(cfLength=CF_LENGTH, scale=SCALE)
    bass = make_bass(cf, cfLength=CF_LENGTH, scale=SCALE)

    # debug
    intervals = [interval_dict[(cf[i]-bass[i])%12] for i in range(1, CF_LENGTH+1)]
    print(f"\nIntervals:     {intervals}")

    # generate lilypond code
    lilyized_cf = lilyize(cf, offset=offset)
    lilyized_bass = lilyize(bass, offset=offset, part="bass")

    # write lilypond code to file
    write_lilyfile(chosen_scale, offset, 200, lilyized_cf, lilyized_bass)

    # convert file to midi and open
    print("\n\nConverting LilyPond file to MIDI...\n")
    subprocess.run(["lilypond", f"first_species.ly"], check=True)
    time.sleep(.33)
    # open the generated MIDI file with default app
    print("Opening MIDI file...")    
    process = subprocess.Popen([
        "open",
        "-a", "MuseScore 4",
        "-W",  # wait until the app exits
        "first_species.midi"
    ])

    # wait for midi app to close before killing script
    print("Waiting for MIDI application to close...")
    process.wait()

    # end script
    print("MIDI application has closed.")

if __name__ == "__main__":
    main()