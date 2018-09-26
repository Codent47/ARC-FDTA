class Instructor:
	
	def __init__(self, preference):
		self.preference=preference #here preference is a list of pairs (Course, Student)

	#list of students given by the instructors of their respective courses:-
	def getPreferences(self):
		return self.preference

	#adding students into the above preference list:-
	def addToPreferences(self,course,student):
		self.preference.append((course,student))
