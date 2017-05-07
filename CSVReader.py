import csv


class ReadCSVRecord:
	def __init__(self, filename):
		self.filename = filename
		self.data = []

	def read(self):
		with open(self.filename, 'r') as f:
			reader = csv.reader(f)
			self.data = [float(row[0]) for row in reader]
		return self.data
	
	def print_data(self):
		pprint.pprint(self.data)

