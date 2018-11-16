from heapq import heappush,heappop
class Course:
	def __init__(self, course_code, size_remaining):
		self.course_code=course_code
		self.size_remaining=size_remaining
		self.applied=[]
		self.selected=[]
	
	def addToApplied(self, student,lambda_s):
		heappush(self.applied,(-lambda_s,student))

	def printApplied(self):
		for x in self.applied:
			print(x[1].getID())

	def printSelected(self):
		for x in self.selected:
			print(x[1].getID())

	def popApplied(self):
		return heappop(self.applied)

	def appliedRemaining(self):
		return len(self.applied)

	def decrementSize(self):
		self.size_remaining-=1

	def allot(self, student,lambda_s):
		heappush(self.selected,(lambda_s,student))
		self.decrementSize()
	
	def getWorstSelected(self):
		return self.selected[0]

	def popWorstSelected(self):
		self.size_remaining-=1
		return heappop(self.selected)

	def getCourseCode(self):
		return self.course_code

	def getSizeRemaining(self):
		return self.size_remaining
