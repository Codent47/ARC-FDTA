class Instructor:
	
	def __init__(self, preference):
		self.preference=preference #List of pairs (Course, Student)

	def getPreferences(self):
		return self.preference
