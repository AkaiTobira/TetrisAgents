
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

    #    if f.find("TLimit6000") == -1: continue
    #    if f.find("PER2") == -1: continue
    #    if f.find("PSO7_") == -1: continue
    #    if f.find("T2000_PER3_c11.5_c20.5_w0.8") == -1: continue
    #    if f.find("PSO7_GEN3_T8000_PER2_c10.5_c20.5_w0.5") == -1 and f.find("PSO7_GEN2_T8000_PER2_c10.5_c20.5_w0.5") == -1: continue
        #if f.find("_GEN2_T8000_PER3_") == -1: continue
    #    if f.find("250")  == -1: continue
    #    if f.find("PARSEL") != -1 : continue
    #    if f.find("MRATE40") == -1: continue
    #    if f.find("SEL_PAR0.0-2") == -1: continue
    #    if f.find("SELType1")  == -1 : continue
        
        output.write( f + " : [MAXES] : " + str(maxes) + "\n")

        if count == 0 : continue
        for i in range(len(avg)):
            avg[i] /= count
        output.write( f + " : [AVG] : " + str(avg) + "\n")
        output.write("\n")


