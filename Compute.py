import Course
import Instructor
import Student
#Returns lambda_c for a single course
def lambda_c(course, student_list): #course is an object of course class, student_list is a list of Students
    c1=0
    c2=0
    c3=0
    for j in student_list: 
        for i in j.getPreferences(): #Checking priority for particular course.
            if(i[0]==course.course_code):
                c1=c1+1
            elif(i[1]==course.course_code):
                c2=c2+1
            elif(i[2]==course.course_code):
                c3=c3+1
        
    app=3*c1+2*c2+1*c3 #Calculating lambda_c
    lam_c=app/course.size_remaining

    return lam_c

def lambda_s(student, p): #Returns lambda_s
    return (student.getPreferences()[0][1]*0.8+student.CG*0.2)
    
def instructorAllotPreference(instructor_list, course_list): #Not checking for clashes, not checking if student applied for the course.
    #List of all instructors, list of all courses.
    for i in instructor_list:
        for k, l in i.getPreferences():
            l.allotCourse(k.course_code)
            k.decrementSize()

def fillAppliedFirstPreference(course_list, student_list):
#List of all courses, list of all students
    for i in student_list:
        for j in course_list:
            if(i.getPreferences()[0][0]==j.course_code):
                ls=lamda_s(i, 0)
                j.addToApplied()

def sortCourses(course_list, student_list):
#List of all courses, list of all students
     lambda_c_list=[]
     for i in course_list:
         c=lambda_c(i, student_list) 
         lambda_c_list.append((i, c))
         
     sorted(lambda_c_list, key=getKey)
     return lambda_c_list


    
def getKey(item):
        return item[1]

def allot(course):
    while(course.size_remaining>0):
        most_deserving=heapq.heappop(course.applied)
        
        for k,l in most_deserving: #Not sure if this is correct
            most_deserving=(-k, l)
        
        heapq.heappush(course.selected, most_deserving)
        l.alloted=course.course_code
        fillRemaining(course.applied, course)

        
def fillRemaining(applied, course):
    while(len(applied)>0): 
        most_deserving=heapq.heappop(applied)
        for k, l in most_deserving:       
            nextPreference(-k, l, course)

def nextPreference(ls, student, course):
        most_deserving=(ls, student)
        for k, l in most_deserving:
            for j in l.preferences:
                if(j[0]==course): #If course matches
                    j=j+1 #Not sure. How to increment? 
                    ls=lamda_s(l, j)
                    if(j[0].size_remaining!=0): #And next preference is not full                        
                        heapq.heappush(j[0].applied, (-ls, l)) #Push student into applied of next preference
                    else:
                        ifFull(ls, student,course)

def ifFull(ls, student, course):
    worst_student=heapq.heappop(course.selected)
    for k, l in worst_student:
        if(k<ls):
            heapq.heappush(course.selected, (ls, student))
            l.alloted=""
            student.alloted=course.course_code
            nextPreference(k, l, course)
        else:
            heapq.heappush(course.selected, worst_student)
            nextPreference(ls, student, course)
