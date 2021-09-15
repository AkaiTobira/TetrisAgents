from subprocess import Popen, PIPE
import time
import os
import threading

def worker():
	while True:
		print("Initialiazed New")
		process = Popen(['python', 'main.py'], stdout=PIPE, stderr=PIPE, shell=True)
		a, b = process.communicate()

		a, b = str(a), str(b)
		a.replace("\n", "\n")

		print(str(a))
		print(str(b))

		if(str(b).find("Traceback") != -1): 
			if(str(a).find("Testing Ended") == -1): return
		

		

threads = [ threading.Thread(target=worker) for _i in range(4) ]
for thread in threads:
	thread.start()
	time.sleep(8)
	


# process = []
# stdouts = []
# stderrs  = []


# for i in range(4):
# 	process.append(Popen(['python', 'main.py'], stdout=PIPE, stderr=PIPE, shell=True))
# 	stdout, stderr = process[i].communicate()
# 	stdouts.append(stdout)
# 	stderrs.append(stderr)
# 	print("Initialiazed core " + str(i))


# while(True):
# 	for i in range(4):
# 		if process[i].returncode != 1:
# 			process[i] = Popen(['python', 'main.py'], stdout=PIPE, stderr=PIPE)
# 			process[i].wait()
# 		print(stderrs[i])
# 		print(stdouts[i])
# 	time.sleep(25)