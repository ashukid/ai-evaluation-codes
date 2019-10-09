import os;
import sys;
import subprocess;
import csv;
import numpy as np;
import pandas as pd;
runtime_failures = [];
from shutil import copyfile;

def getnames():
	curr_dir = os.getcwd();
	os.chdir(os.path.join(curr_dir,'codes'));
	names = [i for i in os.listdir('.') if os.path.isdir(i)];
	os.chdir(curr_dir);
	return names;

def getindex(final,name):
	for i in range(0,len(final)):
		if(final[i][0].upper()==name.upper()):
			return i;
	return -1;

def compare(file1,file2):
	f1 = open(file1,"r");
	f2 = open(file2,"r");
	a = f1.read().split();
	b = f2.read().split();
	if(a==b):
		score = 1;
	else:
		score = 0;
	f1.close();
	f2.close();
	return score;

def run(filename,test_input,test_output,lang_type):
	output_file = "output.txt";

	#for python
	if(lang_type=="python"):
		run_cmd = "timeout 5 python3 " + str(filename) + "< " + str(test_input)+ "> " + str(output_file)
		if(subprocess.call(run_cmd,shell=True)==0):
			score = compare(output_file,test_input);
			return score
		else:
			runtime_failures.append(filename);
			return 0;

	#for c
	if(lang_type=="c"):
		compile_cmd = "gcc "+str(filename);
		run_cmd = "timeout 5 ./a.out < "+str(test_input)+" > "+str(output_file);

	# for cpp
	elif(lang_type=="cpp"):

		# #method to compile on
		# src="/Users/ashu/ghisai_restart/stdc++.h"
		# dest=filename.split("/")[:-1]
		# dest="/".join(dest)
		# dest=os.path.join(dest,"stdc++.h")
		# print(src,dest)
		# copyfile(src,dest);

		# with open(filename,"w") as temp:
		# 	codefile=temp.read()
		# 	print(codefile)
		# 	codefile=codefile.replace("#include<bits/stdc++.h>","#include\"stdc++.h\"")
		# 	temp.write(codefile)

		compile_cmd = "g++ "+str(filename);
		print(compile_cmd)
		run_cmd = "timeout 5 ./a.out < "+str(test_input)+" > "+str(output_file); 

	#for java
	elif(lang_type=="java"):
		compile_cmd = "javac "+str(filename);
		class_file = filename.split("/")[-1].split(".")[0]
		run_cmd = "timeout 5 java " + str(class_file) +"< "+str(test_input)+" > "+str(output_file);
	
	# running commands for c,cpp and java
	if(subprocess.call(compile_cmd,shell=True)==0):
		if(subprocess.call(run_cmd,shell=True)==0):
			score = compare(output_file,test_output);
			return score;
		else:
			runtime_failures.append(filename);
			return 0;
	else:
		return 0;
	
def main(args):
	n = 5;# number of questions
	tests = 5;# number of testcases
	names = getnames();
	partial = [1,1,1,1,1];
	marks = [];
	for i in range(0,len(names)):
		temp = [names[i]];
		for i in range(0,n):
			temp.append(0);
		marks.append(temp);
	curr_dir = os.getcwd();
	os.chdir(os.path.join(curr_dir,'codes'));
	code_dir = os.getcwd();
	for i in range(0,len(names)):#all codes
		path = os.path.join(code_dir,names[i]);
		for j in range(0,n):#number of questions
			ques = os.path.join(path,str(j+1));
			if(os.path.isdir(ques)):
				os.chdir(ques);
				total = 0;
				for test in range(0,tests):#all testcases
					test_input = os.path.join(curr_dir,'testcases/'+str(j+1)+'/in0'+str(test)+'.txt');
					test_output = os.path.join(curr_dir,'testcases/'+str(j+1)+'/out0'+str(test)+'.txt');
					files = [f for f in os.listdir('.') if os.path.isfile(f)];
					score = 0;
					for f in files:
						if(f[-2:]=='.c' or f[-2:]=='.C'):
							score = max(score,run(os.path.join(ques,f),test_input,test_output,"c"));
						elif(f[-4:]=='.cpp' or f[-4:]=='.CPP'):
							continue
							score = max(score,run(os.path.join(ques,f),test_input,test_output,"cpp"));
						elif(f[-3:]=='.py' or f[-3:]=='.PY'):
							score = max(score,run(os.path.join(ques,f),test_input,test_output,"python"))
						elif(f[-5:]=='.java' or f[-5:]=='.JAVA'):
							score = max(score,run(os.path.join(ques,f),test_input,test_output,"java"))
					total += score*partial[j];
				marks[i][j+1] = total;
				os.chdir(path);
			else:
				marks[i][j+1] = 0;
		print('Completed '+names[i]+' '+str(i+1));
	os.chdir(curr_dir);
	headers = ["Roll"];
	for i in range(0,n):
		headers.append("q"+str(i+1));
	final = [];
	for i in range(0,len(marks)):
		idx = getindex(final,marks[i][0]);
		if(idx==-1):
			final.append(marks[i]);
		else:
			for j in range(0,n):
				final[idx][j+1] = max(final[idx][j+1],marks[i][j+1]);
	with open("results.csv","w+") as my_csv:
		writer = csv.writer(my_csv,delimiter=',');
		writer.writerow(headers);
		writer.writerows(final);

main(sys.argv);
runtime_failures = list(set(runtime_failures));
runtime_failures.sort();
for fail in runtime_failures:
	print(fail);
