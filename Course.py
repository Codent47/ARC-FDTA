from heapq import heappush,heappop
class Course:
	applied=[]
	selected=[]
	def __init__(self, course_code, size_remaining, selected, applied):
		self.course_code=course_code
		self.size_remaining=size_remaining
		self.selected=selected
		self.applied=applied

	def addtoApplied(student,lambda_s):
		heappush(self.applied,{-lambda_s,student})

	def appliedRemaining():
		return length(self.applied)>0

	def decrementSize():
		self.size_remaining-=1

	def isFull():
		return size_remaining==0

	def allot(student,lambda_s):
		heappush(self.selected,{lambda_s,student})
	
	def getWorstSelected():
		return selected[0]

	def popWorsrSelected():
		heappop(selected)





	