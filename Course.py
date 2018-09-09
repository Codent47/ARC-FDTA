import heapq
class Course:
	
	def __init__(self, course_code, size_remaining, selected, applied):
		self.course_code=course_code;
		self.size_remaining=size_remaining;
		self.selected=selected;
		heapq.heapify(selected);
		self.applied=applied
		heapq.heapify(applied);