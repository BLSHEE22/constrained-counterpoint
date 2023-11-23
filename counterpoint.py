import random
from constraint import *

scales = {"Major": [-5,-3,-1,0,2,4,5,7,9,11,12,14,16], "Minor":[-5,-4,-1,0,2,3,5,7,8,10,12,14,15]}

def makeCantusFirmus(cfLength, scale):
    print("Starting cantus firmus creation sequence...\n")
    p = Problem()
    print("Adding variables...")
    for i in range(1, cfLength+1):
        p.addVariable(i, scales[scale])
    print(f'\'{scale} scale\' added.')
    print("Variables added.\n")
    # START AND END ON TONIC
    print("Adding constraints...")
    for j in range(1, cfLength+1):
        if j == 1 or j == cfLength:
            p.addConstraint(lambda x: x == 0, [j])
    print("\'Start and end on tonic\' constraint added.")
    # PENULTIMATE NOTE IS LEADING TONE/SUPERTONIC
    for j in range(1, cfLength+1):
        if j == cfLength-1:
            p.addConstraint(lambda x: x == -1 or x == 2, [j])
    print("\'Penultimate note leading tone/supertonic\' constraint added.")
    # LEADING TONE ALWAYS LEADS TO TONIC
    for j in range(1, cfLength+1):
        if j > 1:
            p.addConstraint(lambda x,y: y == 0 if x == -1 else (y == 12 if x == 11 else y), [j-1,j])            
    print("\'Leading tone leads to tonic\' constraint added.")
    # ALWAYS RESOLVE LEAPS BY STEP IN OPPOSITE DIRECTION
    for j in range(1, cfLength+1):
        if j > 2:
            p.addConstraint(lambda x,y,z: z == scales[scale][scales[scale].index(y)+1] if abs(x-y) > 3 and x>y else (z == scales[scale][scales[scale].index(y)-1] if abs(x-y) > 3 and x<y else z), [j-2,j-1,j])
    print("\'Resolve leaps by step in opposite direction\' constraint added.")
    # NO DISSONANT LEAPS OR STATIC MOTION
    for j in range(1, cfLength+1):
        if j != cfLength:
            p.addConstraint(lambda x,y: abs(x-y) < 17 and abs(x-y) != 14 and abs(x-y) != 13 and abs(x - y) != 12 and abs(x-y) != 11 and abs(x-y) != 10 and abs(x-y) != 7 and abs(x - y) != 6 and abs(x - y) != 0, (j, j+1))
    print("\'No dissonant leaps or static motion\' constraint added.")
    # TODO: REPETITION CONSTRAINT
    print("Constraints added.\n")
    print(f'Finding all {cfLength}-note cantus firmi that meet the requirements...\n')
    solutions = p.getSolutions()
    print(f'{len(solutions)} found!\n')
    print("Choosing a random solution...\n")
    randomSolution = random.choice(p.getSolutions())
    print((sorted(dict(randomSolution).items())))

def main():
    print("Get ready for some counterpoint!\n")
    makeCantusFirmus(cfLength=15, scale="Major")

if __name__ == "__main__":
    main()