import Course
import Instructor
import Student
#Returns lambda_c for a single course
def lambda_c(course, student_list): #course is an object of course class, student_list is a list of Students
    c1=0;
    c2=0;
    c3=0;
    for j in student_list: 
        for i in j.preferences: #Checking priority for particular course.
            if(i[0]==course.course_code):
                c1=c1+1;
            elif(i[1]==course.course_code):
                c2=c2+1;
            elif(i[2]==course.course_code):
                c3=c3+1;
        
    app=3*c1+2*c2+1*c3; #Calculating lambda_c
    lam_c=app/course.size_remaining;

    return lam_c;

def lambda_s(student): #Returns lambda_s
    return (student.preferences[0][1]*0.8+student.CG*0.2);
