# ai-evaluation-codes

### code directory structure :

> {assign1,assign2,assign3}/roll_no/question_no/code.{c,py,cpp,java}

For example :
```
assign1/irm2015001/1/q1.java
assign3/irm2015001/6/q1.c
```

### testcases directory structure

>testcases/question_no/in{00,01,02,03,04}.txt         #input

>testcases/question_no/out{00,01,02,03,04}.txt        #output

For example :
```
testcases/1/in00.txt
testcases/1/out00.txt
```

NOTE : curly braces "{}" means one of them.


Command to run individual code :
```
python3 main.py [no_of_questions_in_the_assignment] [assignment_code_directory_name] [roll_number]
```

Command to run all codes :
```
python3 run.py [no_of_questions_in_the_assignment] [assignment_code_directory_name] 
```
