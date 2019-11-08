import os;
import sys;
from shutil import copyfile;
import shutil

n = int(sys.argv[1]);#no of questions
assign=sys.argv[2]# assignment number
newpath = os.path.join(os.getcwd(),assign+'_converted');

if(os.path.exists(newpath)):
	shutil.rmtree(newpath)
os.makedirs(newpath)

path = os.path.join(os.getcwd(),assign)
os.chdir(path);

dirs =  [i for i in os.listdir(".") if os.path.isdir(i)];
for i in range(0,n):
	os.makedirs(os.path.join(newpath,str(i+1)));
	for j in range(0,len(dirs)):
		roll = os.path.join(path,dirs[j]);
		os.chdir(roll);
		if(os.path.exists(os.path.join(roll,str(i+1)))):
			os.chdir(os.path.join(roll,str(i+1)));
			files = []
			for f in os.listdir("."):
				if(os.path.isfile(f)):
					f=f.lower()
					if(f[-2:]==".c" or f[-3:]==".py" or f[-5:]==".java" or f[-4:]==".cpp"):
						files.append(f)
						ext="."+str(f.split(".")[-1])
					else:
						print(f)
		
			if(len(files)==0):
				continue;
			dest = os.path.join((os.path.join(newpath,str(i+1))),dirs[j]+ext);
			src = os.path.join(os.getcwd(),files[0]);
			# print(src,dest);
			copyfile(src,dest);
