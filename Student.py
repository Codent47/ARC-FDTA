class Student:

    def __init__ (self,ID,preferences,alloted,CG):
        self.ID=ID
        self.preferences=preferences #here preferences is a list of (grade,course)
        self.alloted=alloted
        self.CG=CG

    #redefining the greater than operator. (if two students are compared, they will be compared on the bases of ID)
    def __gt__(self, student2):
        return self.ID > student2.getID()

    #allots the course to the student:-
    def allotCourse(self, alloted):
    	self.alloted=alloted

    #returns the alloted course of the student:-
    def getAllotedCourse(self):
    	return self.alloted

    #returns preference list of the student:-
    def getPreferences(self):
    	return self.preferences

    #returns CG of the student:-
    def getCG(self):
    	return self.CG
    #returns ID of the student:-
    def getID(self):
    	return self.ID


