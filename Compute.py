import Course
import Instructor
import Student
import operator
#Returns lambda_c for a single course
def lambda_c(course, student_list): #course is an object of course class, student_list is a list of Students
    c1=0
    c2=0
    c3=0
    for j in student_list: 
        for i in j.getPreferences(): #Checking priority for particular course.
            if(i[0]==course.getCourseCode()):
                c1=c1+1
            elif(i[1]==course.getCourseCode()):
                c2=c2+1
            elif(i[2]==course.getCourseCode()):
                c3=c3+1
        
    app=3*c1+2*c2+1*c3 #Calculating lambda_c
    lam_c=app/course.getSizeRemaining()

    return lam_c

def lambda_s(student, grade): #Returns lambda_s
    
    return (grade*0.8+student.getCG()*0.2)
    
def instructorAllotPreference(instructor_list, course_list): #Not checking for clashes, not checking if student applied for the course.
    #List of all instructors, list of all courses.
    for i in instructor_list:
        for k, l in i.getPreferences():
            l.allotCourse(k.getCourseCode())
            k.decrementSize()

def fillAppliedFirstPreference(course_list, student_list):
#List of all courses, list of all students
    for i in student_list:
        for j in course_list:
            x=i.getPreferences()
            if(x[0][0]==j.getCourseCode()):
                ls=lambda_s(i, x[0][1])
                j.addToApplied(i, ls)

def sortCourses(course_list, student_list):
#List of all courses, list of all students
     lambda_c_list=[]
     for i in course_list:
         c=lambda_c(i, student_list) 
         lambda_c_list.append((i, c))
         
     lambda_c_list.sort(key=operator.itemgetter(1))
     lambda_c_list=[course for course, lam_c in lambda_c_list]
     return lambda_c_list


    
def getKey(item):
        return item[1]

def allot(course):
    while(course.getSizeRemaining()>0  and course.appliedRemaining()>0):
        most_deserving=course.popApplied()
        course.allot(-most_deserving[0], most_deserving[1])
        most_deserving[1].allotCourse(course.getCourseCode())
    
    fillRemaining(course)

        
def fillRemaining(course):
    while(course.appliedRemaining()>0): 
        most_deserving=course.popApplied()
               
        nextPreference(-most_deserving[0], most_deserving[1], course)

def nextPreference(ls, student, course):
        most_deserving=(ls, student)
        flag=false
        for k, l in most_deserving:
            for j in l.getPreferences():
                if(j[0]==course): #If course matches
                    flag=true 
                elif(flag):
                    ls=lambda_s(l, j[1])
                    if(j[0].getSizeRemaining()>0): #And next preference is not full 
                        j[0].addToApplied(l, ls) #Push student into applied of next preference                     
                     
                    else:
                        ifFull(ls, student, j[0]) #Check this line. Changed it
                    break

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
