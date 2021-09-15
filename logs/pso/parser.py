
import os

files = [f for f in os.listdir('.') if os.path.isfile(f) ]

output = open("output", 'w')
output.write("")

Dict = {}

for f in files:
    if ".py" in f: continue
    if "output" == f: continue

#    if f.find("PSO7_SIZE20_GEN2_T2000_PER3_c") == -1: continue
    #if f.find("1.5_c21.5") == -1: continue
    if f.find("PSO7_") == -1: continue
    if f.find("PSO7_GEN2_T9000_PER2_c10.5_c20.5_w0.5") == -1: continue
    
    if f.find("populations") != -1: continue
    
    with open(f, 'r') as infile:
        prev_line = ""
        line = infile.readline()
        while True:
            prev_line = line
            line = infile.readline()
            if not line:
                break



        obj3 = f.split("PSO")
        f = "PSO" + obj3[1]

        Dict[f] = prev_line

kesy = Dict.keys()
sortedKeys = []
for i in kesy:
    sortedKeys.append(i)


for i in range(len(sortedKeys)):
    for j in range(len(sortedKeys)-1):
        if sortedKeys[i] < sortedKeys[j]:
            temp = sortedKeys[i]
            sortedKeys[i] = sortedKeys[j]
            sortedKeys[j] = temp


for f in sortedKeys:

    if f.find("best") == -1:
        output.write( f + " : [AVG] : " + str(Dict[f]) + "")
    else:
        obj = Dict[f].split(",")
        if len(obj) == 0: continue
        output.write(f + " : [Best] :" + obj[len(obj)-1] + "\n")

    #    if f.find("TLimit6000") == -1: continue
    #    if f.find("PER2") == -1: continue
    #    if f.find("PSO7_GEN3_T8000_PER2_c10.5_c20.5_w0.5") == -1 and f.find("PSO7_GEN2_T8000_PER2_c10.5_c20.5_w0.5") == -1: continue
        #if f.find("_GEN2_T8000_PER3_") == -1: continue
    #    if f.find("250")  == -1: continue
    #    if f.find("PARSEL") != -1 : continue
    #    if f.find("MRATE40") == -1: continue
    #    if f.find("SEL_PAR0.0-2") == -1: continue
    #    if f.find("SELType1")  == -1 : continue
        




