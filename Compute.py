from Course import *
from Student import *
from Instructor import *
import operator
import pandas as pd

#Calculates lambda_c(which is used to rank the courses) for a single course
def lambda_c(course, student_list): #course is an object of course class, student_list is a list of Students
    c=[0,0,0,0,0]
    for j in student_list:
        cnt=0 
        for i in j.getPreferences(): #Checking priority for particular course.
            if (i[0]==course.getCourseCode()):
                c[cnt]+=1
            cnt+=1
        
    app=5*c[0]+4*c[1]+3*c[2]+2*c[3]+c[4] #Calculating lambda_c
    lam_c=app/course.getSizeRemaining()

    return lam_c

#Calculates lambda_s (which is used to rank the students) for a single student
def lambda_s(student, grade): #returns lambda_s
    grade=float(grade)
    return (grade*10+float(student.getCG()))
    
#allots the students who have been recommended by the instructors of various courses into the respective courses
def instructorAllotPreference(instructor_list, course_list): #Not checking for clashes, not checking if student applied for the course.
    #List of all instructors, list of all courses.
    for i in instructor_list:
        for k, l in i.getPreferences():
            l.allotCourse(k.getCourseCode())
            k.decrementSize()

#alloting first preference to students from the course list sorted on the basis of lambda_c
def fillAppliedFirstPreference(course_list, student_list):
#List of all courses, list of all students
    for i in student_list:
        if (i.getAllotedCourse()!="None"):
            continue
        x=i.getPreferences()
        ls=lambda_s(i, x[0][1])
        course_code_dict[x[0][0]].addToApplied(i, ls)

#sorts the courses according to the lambda_c as parameter
def sortCourses(course_list, student_list):
#List of all courses, list of all students
     lambda_c_list=[]
     for i in course_list:
         c=lambda_c(i, student_list) 
         lambda_c_list.append((i, c))
         
     lambda_c_list.sort(key=operator.itemgetter(1))
     lambda_c_list=[course for course, lam_c in lambda_c_list]
     return lambda_c_list

#alloting the students their respective courses from the sorted list of that course    
def allot(course):
    while(course.getSizeRemaining()>0  and course.appliedRemaining()>0):
        most_deserving=course.popApplied()
        course.allot(-most_deserving[0], most_deserving[1])
        most_deserving[1].allotCourse(course.getCourseCode())
    
    fillRemaining(course)

#filling the remaining seats of the course      
def fillRemaining(course):
    while(course.appliedRemaining()>0): 
        most_deserving=course.popApplied()               
        nextPreference(most_deserving[1], course)

#pushing students into the next preference course list if their current preference is full
def nextPreference(student, course):
        flag=False
        for j in student.getPreferences():
            if(j[0]==course): #If course matches
                flag=True 
            elif(flag):
                ls=lambda_s(student, j[1])
                if(j[0].getSizeRemaining()>0): #And next preference is not full 
                    j[0].addToApplied(l, ls) #Push student into applied of next preference                     
                else:
                    ifFull(ls, student, j[0]) 
                break

#checking whether their current preference course list is full or not and sending them to next preference  if list full
def ifFull(ls, student, course):
    worst_student=getWorstSelected()
    for k, l in worst_student:
        if(k<ls):
            student.allotCourse(course.getCourseCode())
            course.popWorstSelected()
            l.allotCourse("None")
            nextPreference(k, l, course)
        else:
            nextPreference(ls, student, course)

#(don't know much about pandas so can't do documentation)
df=pd.read_csv('Course.csv')
course_list=[]
course_code_dict={}
for index, row in df.iterrows():
    c=Course(row['course_code'],row['Size-remaining'])
    course_list.append(c)
    course_code_dict[c.getCourseCode()]=c

df=pd.read_csv('Student.csv')
student_list=[]
student_id_dict={}
for index, row in df.iterrows():
    if (row['ID'] in student_id_dict): #to take care of duplicate data set
        continue                        
    prefs=[(row['Course1'],row['Grade1']),(row['Course2'],row['Grade2']),(row['Course3'],row['Grade3']),(row['Course4'],row['Grade4']),(row['Course5'],row['Grade5'])]
    s=Student(row['ID'],prefs,"None",row['CG'])
    student_list.append(s)
    student_id_dict[s.getID()]=s

df=pd.read_csv('Instructor.csv')
instructor_list=[]
instructor_id_dict={}
for index, row in df.iterrows():
    c=course_code_dict[row['Course']]
    s=student_id_dict[row['Student']]
    prefs=[(c,s)]
    if (row['Instructor'] in instructor_id_dict):
        instructor_id_dict[row['Instructor']].addToPreferences(c,s)
    else:
        i=Instructor(prefs)
        instructor_list.append(i)
        instructor_id_dict[row['Instructor']]=i

instructorAllotPreference (instructor_list,course_list)

for c in course_list:
    if (c.getSizeRemaining()==0):
        course_list.remove(c)

course_list=sortCourses(course_list,student_list)

fillAppliedFirstPreference(course_list,student_list)

for c in course_list:
    allot(c)

print(len(student_list))

for s in student_list:
    print(s.getID(),s.getAllotedCourse())



