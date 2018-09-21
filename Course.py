from heapq import heappush,heappop
class Course:
	applied=[]
	selected=[]
	def __init__(self, course_code, size_remaining):
		self.course_code=course_code
		self.size_remaining=size_remaining
		
	def addtoApplied(self, student,lambda_s):
		heappush(self.applied,(-lambda_s,student))

	def popApplied(self):
		return heappop(applied)

	def appliedRemaining(self):
		return length(self.applied)>0

	def decrementSize(self):
		self.size_remaining-=1

	def allot(self, student,lambda_s):
		heappush(self.selected,(lambda_s,student))
		decrementSize()
	
	def getWorstSelected(self):
		return selected[0]

	def popWorstSelected(self):
		self.size_remaining-=1
		return heappop(selected)

	def getCourseCode(self):
		return self.course_code

	def getSizeRemaining(self):
		return self.size_remaining
