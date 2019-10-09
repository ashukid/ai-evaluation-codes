import os;
import sys;

assign_no=sys.argv[1]
f = open("assign"+str(assign_no)+".txt","w");
path = os.path.join(os.getcwd(),'codes');
os.chdir(path);
dirs =  [i for i in os.listdir(".") if os.path.isdir(i)];
dirs.sort();
for i in range(0,len(dirs)):
	roll = os.path.join(path,dirs[i]);
	os.chdir(roll);
	line = dirs[i]+" - ";
	present = [];
	ques = [j for j in os.listdir(".") if os.path.isdir(j)];
	for q in ques:
		ques_path = os.path.join(roll,q);
		os.chdir(ques_path);
		codes = [k for k in os.listdir(".") if os.path.isfile(k)];
		if(len(codes)>0):
			present.append(q);
	if(len(present)==0):
		continue;
	for j in range(0,len(present)-1):
		line = line+str(present[j])+",";
	line = line+str(present[len(present)-1])+"\n";
	#print(line);
	f.write(line);
f.close(); 

