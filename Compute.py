from Course import *
from Student import *
from Instructor import *
import operator
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

courseAllotmentDone={}
#Returns lambda_c for a single course
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

def lambda_s(student, grade): #Returns lambda_s
    grade=float(grade)
    return (grade*10+float(student.getCG()))
    
def instructorAllotPreference(instructor_list, course_list): #Not checking for clashes, not checking if student applied for the course.
    #List of all instructors, list of all courses.
    for i in instructor_list:
        for k, l in i.getPreferences():
            l.allotCourse(k.getCourseCode())
            k.decrementSize()

def fillAppliedFirstPreference(course_list, student_list):
#List of all courses, list of all students
    for i in student_list:
        if (i.getAllotedCourse()!="None"):
            continue
        x=i.getPreferences()
        ls=lambda_s(i, x[0][1])

        '''if (i.getID()=="2016A7PS0066G"):
            for j in x:
                print("ayayya",j[0],j[1])'''

        if (x[0][0]=="None"):
            i.allotCourse("None")
        elif (x[0][1]<2):
            nextPreference(i,course_code_dict[x[0][0]])
        else:
            course_code_dict[x[0][0]].addToApplied(i, ls)

def sortCourses(course_list, student_list):
#List of all courses, list of all students
     lambda_c_list=[]
     for i in course_list:
         c=lambda_c(i, student_list) 
         lambda_c_list.append((i, c))
         
     lambda_c_list.sort(key=operator.itemgetter(1))
     lambda_c_list=[course for course, lam_c in lambda_c_list]
     return lambda_c_list

def allot(course):
    courseAllotmentDone[course.getCourseCode()]=True
    while(course.getSizeRemaining()>0  and course.appliedRemaining()>0):
        most_deserving=course.popApplied()
        course.allot(most_deserving[1],-most_deserving[0])
        most_deserving[1].allotCourse(course.getCourseCode())
    fillRemaining(course)
    
        
def fillRemaining(course):
    while(course.appliedRemaining()>0): 
        most_deserving=course.popApplied()               
        nextPreference(most_deserving[1], course)

def nextPreference(student, course):
        flag=False
        for j in student.getPreferences():
            if(j[0]==course.getCourseCode()): #If course matches
                flag=True 
            elif(flag):
                ls=lambda_s(student, j[1])
                if (j[0]=="None"):
                    student.allotCourse("None")
                    return
                if (j[1]<2):
                    student.allotCourse("None")
                    continue

                if(course_code_dict[j[0]].getSizeRemaining()>0): #And next preference is not full 
                    if (j[0] in courseAllotmentDone):
                        course_code_dict[j[0]].allot(student,ls)
                        student.allotCourse(j[0])
                        return
                    course_code_dict[j[0]].addToApplied(student, ls) #Push student into applied of next preference                     
                    if (student.getID()=="2016A7PS0066G" and j[0]=="CS F212"):
                        print("Ishan in dbms")
                else:
                    ifFull(ls, student, course_code_dict[j[0]]) #Check this line. Changed it
                break

def ifFull(ls, student, course):
    worst_student=course.getWorstSelected()
    if (course.getCourseCode()=="CS F111"):
        #print(worst_student[1].getID())
        print("List of selected")
        course.printSelected()

        print("this stud comes",student.getID())

        print("worst ka ls",worst_student[0],"stud ka ls",ls)

    if(worst_student[0]<ls):
        student.allotCourse(course.getCourseCode())
        course.popWorstSelected()
        course.allot(student,ls)
        worst_student[1].allotCourse("None")
        nextPreference(worst_student[1], course)
    else:
        nextPreference(student, course)

df=pd.read_csv('course_details.csv')
course_list=[]
course_code_dict={}
for index, row in df.iterrows():
    c=Course(row['Course No'],row["No. of FDTA's given"])
    course_list.append(c)
    course_code_dict[c.getCourseCode()]=c

df=pd.read_csv('Student.csv')
df_cg=pd.read_csv('cgpa_list.csv')
df_grade1=[]
for i in range(10):
    df_grade1.append(0)
df_grade1[2]=pd.read_csv('2012_grades.csv')
df_grade1[3]=pd.read_csv('2013_grades.csv')
df_grade1[4]=pd.read_csv('2014_grades.csv')
df_grade1[5]=pd.read_csv('2015_grades.csv')
df_grade1[6]=pd.read_csv('2016_grades.csv')
#df_grade1[7]=pd.read_csv('2017_grades.csv')

grade_dict={'A':10,'A-':9, 'B': 8, 'B-': 7, 'C': 6, 'C-': 5, 'D': 4, 'D-': 3, 'E': 2, 'NC': 0, 'W': 0, '            ':-1, 'NA':-1 }

student_list=[]
student_id_dict={}

for index, row in df.iterrows():
    stud_id=row['ID']
    stud_cg=df_cg[(df_cg['Campus ID']==stud_id)]['CGPA']
    stud_cg=float(stud_cg)
    stud_grade=[]
    j=int(stud_id[3])
    for i in range(1,6):
        course_pref_str='Course'+str(i)
        if (pd.isnull(row[course_pref_str])):
            row[course_pref_str]="None"

        grade_arr=( df_grade1[j][ (df_grade1[j]['Campus ID']==stud_id) & (df_grade1[j]['Subject']==row[course_pref_str][0:2]) &( (df_grade1[j]['Catalog']==row[course_pref_str][-4:]) | (df_grade1[j]['Catalog']=="    "+row[course_pref_str][-4:]))& (df_grade1[j]["Grade In"]<'C')]["Grade In"]) 
        stud_grade.append('NC')
        if (len(grade_arr)>0):
            stud_grade[len(stud_grade)-1]=grade_arr.iat[len(grade_arr)-1]
        else:
            stud_grade[len(stud_grade)-1]='NA'

    prefs=[(row['Course1'],grade_dict[stud_grade[0]]),(row['Course2'],grade_dict[stud_grade[1]]),(row['Course3'],grade_dict[stud_grade[2]]),(row['Course4'],grade_dict[stud_grade[3]]),(row['Course5'],grade_dict[stud_grade[4]])]
    s=Student(row['ID'],prefs,"None",stud_cg)
    student_list.append(s)
    student_id_dict[s.getID()]=s

df_instr=pd.read_csv('Instructor.csv')
instructor_list=[]
instructor_id_dict={}
for index, row in df_instr.iterrows():
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

#course_list=sortCourses(course_list,student_list)

fillAppliedFirstPreference(course_list,student_list)

for c in course_list:
    print(c.getCourseCode())
    c.printApplied()

for c in course_list:
    allot(c)

print(len(student_list))

for s in student_list:
    print(s.getID(),s.getAllotedCourse())



