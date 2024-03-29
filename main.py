
import os
import sys
import subprocess
import csv
import numpy as np
import pandas as pd
runtime_failures = []
from shutil import copyfile

code_directory=sys.argv[2]
name=sys.argv[3]

def compare(file1,file2):
	f1 = open(file1,"r")
	f2 = open(file2,"r")
	a = f1.read().split()
	b = f2.read().split()
	if(a==b):
		score = 1
	else:
		score = 0
	f1.close()
	f2.close()
	return score

def run(filename,test_input,test_output,lang_type):
	output_file = "output.txt"

	#for python
	if(lang_type=="python"):
		run_cmd = "timeout 50 python3 " + str(filename) + "< " + str(test_input)+ "> " + str(output_file)
		if(subprocess.call(run_cmd,shell=True)==0):
			score = compare(output_file,test_output)
			return score
		else:
			runtime_failures.append(filename)
			return 0

	#for c
	if(lang_type=="c"):
		compile_cmd = "gcc "+str(filename)
		run_cmd = "timeout 10 ./a.out < "+str(test_input)+" > "+str(output_file)

	# for cpp
	elif(lang_type=="cpp"):

		compile_cmd = "g++ "+str(filename)
		run_cmd = "timeout 10 ./a.out < "+str(test_input)+" > "+str(output_file) 

	#for java
	elif(lang_type=="java"):

		compile_cmd="javac "+str(filename)
		class_file = filename.split("/")[-1].split(".")[0]
		run_cmd = "timeout 20 java " + str(class_file) +"< "+str(test_input)+" > "+str(output_file)
	
	# running commands for c,cpp and java
	if(subprocess.call(compile_cmd,shell=True)==0):
		if(subprocess.call(run_cmd,shell=True)==0):
			score = compare(output_file,test_output)
			return score
		else:
			runtime_failures.append(filename)
			return 0
	else:
		return 0
	
def main(args):

    n = int(sys.argv[1])# number of questions
    tests = 5# number of testcases
    partial = [1]*n
    marks = [0]*n

    curr_dir = os.getcwd()
    os.chdir(os.path.join(curr_dir,code_directory))
    code_dir = os.getcwd()


    temppath1 = os.path.join(code_dir,name.lower())
    temppath2 = os.path.join(code_dir,name.upper())

    if(os.path.exists(temppath1)):
        path=temppath1
    elif(os.path.exists(temppath2)):
        path=temppath2
    else:
        print("Code doesn't exists")
        return
    
    for j in range(0,n):#number of questions

        ques = os.path.join(path,str(j+1))
        if(os.path.isdir(ques)):
            os.chdir(ques)
            total = 0
            for test in range(0,tests):#all testcases
                test_input = os.path.join(curr_dir,code_directory+'_testcases/'+str(j+1)+'/in0'+str(test)+'.txt')
                test_output = os.path.join(curr_dir,code_directory+'_testcases/'+str(j+1)+'/out0'+str(test)+'.txt')
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                score = 0
                for f in files:
                    if(f[-2:]=='.c' or f[-2:]=='.C'):
                        score = max(score,run(os.path.join(ques,f),test_input,test_output,"c"))
                    elif(f[-4:]=='.cpp' or f[-4:]=='.CPP'):
                        score = max(score,run(os.path.join(ques,f),test_input,test_output,"cpp"))
                    elif(f[-3:]=='.py' or f[-3:]=='.PY'):
                        score = max(score,run(os.path.join(ques,f),test_input,test_output,"python"))
                    elif(f[-5:]=='.java' or f[-5:]=='.JAVA'):
                        score = max(score,run(os.path.join(ques,f),test_input,test_output,"java"))
                total += score*partial[j]
            marks[j] = total
            os.chdir(path)
        else:
            marks[j] = 0

    print(marks)    

main(sys.argv)
runtime_failures = list(set(runtime_failures))
runtime_failures.sort()
for fail in runtime_failures:
	print(fail)
