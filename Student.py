class Student:

    def __init__ (self,ID,preferences,alloted,CG):
        self.ID=ID
        self.preferences=preferences
        self.alloted=alloted
        self.CG=CG

    def allotCourse(self, alloted):
    	self.alloted=alloted

    def getAllotedCourse(self):
    	return self.alloted

    def getPreferences(self):
    	return self.preferences

    def getCG(self):
    	return self.CG

    def getID(self):
    	return self.ID

