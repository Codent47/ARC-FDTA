from heapq import heappush,heappop
class Course:
	def __init__(self, course_code, size_remaining):
		self.course_code=course_code
		self.size_remaining=size_remaining
		self.applied=[]
		self.selected=[]
	
	#adding students to the applied list
	def addToApplied(self, student,lambda_s):
		heappush(self.applied,(-lambda_s,student))
    
    #prints the student ID no.s who have applied
	def printApplied(self):
		for x in self.applied:
			print(x[1].getID())

	#pops the best student suitable for the course on the basis of lambda_s
	def popApplied(self):
		return heappop(self.applied)

    #checking the number of students in the applied list
	def appliedRemaining(self):
		return len(self.applied)

	#decrements the size of the course list
	def decrementSize(self):
		self.size_remaining-=1

	#pushing the worst student (on basis of lambda_s) to the top of the list
	def allot(self, student,lambda_s):
		heappush(self.selected,(lambda_s,student))
		self.decrementSize()
	
	#returns the worst student
	def getWorstSelected(self):
		return self.selected[0]

    #removes the worst student from the selected list
	def popWorstSelected(self):
		self.size_remaining-=1
		return heappop(self.selected)

	#returns the course code of the course
	def getCourseCode(self):
		return self.course_code

	#returns the size remaining in the course
	def getSizeRemaining(self):
		return self.size_remaining
