import json

json_converted = None

with open('PSO7_GEN2_T9000_PER3_c10.5_c20.5_w0.5.json', 'r') as json_file:
    json_converted = json.loads(json_file.read())


numbers  = [0.5, 1.0, 1.5]
numbers2 = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for iteral in numbers:
    for iteral2 in numbers:
        for iteral3 in numbers2:

            json_converted["c1"] = iteral
            json_converted["c2"] = iteral2
            json_converted["w"]  = iteral3

            with open('PSO7_GEN2_T9000_PER3_c1' + str(iteral) + '_c2' + str(iteral2) + '_w' + str(iteral3) +  '.json', 'w') as outfile:
                json.dump(json_converted, outfile, indent=4)
