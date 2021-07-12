
import os

files = [f for f in os.listdir('.') if os.path.isfile(f) ]

output = open("output", 'w')
output.write("")

for f in files:
    if ".py" in f: continue
    if "output" == f: continue
    with open(f, 'r') as infile:
        infile.readline()

        avg   = []
        maxes = []
        count = 0
        while True:
            line = infile.readline()
            if not line: 
                print(avg, maxes, count)

                break
            count += 1
            obj = line.split(",")

            if len(obj) == 0: continue

            for i in range(len(obj)):
                
                if len(avg) < len(obj):
                    avg.append(float(obj[i]))
                    maxes.append(float(obj[i]))
                else:
                    avg[i] += float(obj[i])
                    maxes[i] = max(float(obj[i]), maxes[i])
        output.write( f + " : [MAXES] : " + str(maxes) + "\n")

        if count == 0 : continue
        for i in range(len(avg)):
            avg[i] /= count
        output.write( f + " : [AVG] : " + str(avg) + "\n")
        output.write("\n")


