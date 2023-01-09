class Table:

	def __init__(self):

		# Header row. The keys are the name of the columns, the values are the position of each column
		self.header = {}

		# Curret data row
		self.row = []

		# All data rows
		self.rows = []

	def create_row(self, size: int):
		"""Creates a new empty data row. Subsequent values will be added to this row until a new data row
		is created.
		- size: initial capacity of the row
		"""

		self.rows.append(self.row)
		self.row = [None] * size

	def add(self, column: str, value: object):
		"""Adds a value to the current data row.
		- column: column name
		- value: value
		"""

		try:
			position = self.header[column]
			self.row[position] = str(value)
		except KeyError:
			self.header[column] = len(self.header)
			self.row.append(str(value))
