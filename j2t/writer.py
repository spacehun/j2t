from j2t.table import Table
from openpyxl.styles import Font
from openpyxl import Workbook

class XLSXWriter:

	def __init__(self, output: str = 'output.xlsx'):

		self.writer = Workbook()
		self.writer.remove(self.writer.active)
		self.output = output
		self.key = None

	def __del__(self):

		self.writer.save(self.output)
		self.writer.close()

	def write(self, name: str, table: Table, key: str = None):

		# Write header
		header = [0] * len(table.header)
		for field, position in table.header.items():
			header[position] = field
		sheet = self.writer.create_sheet(name)
		row = sheet.row_dimensions[1]
		row.font = Font(bold = True)
		sheet.append(header)

		if self.key is None:

			# Write values
			for row in (*table.rows, table.row):
				sheet.append(row)

		else:
			for row in (*table.rows, table.row):

				# Write key
				for i, values in enumerate(self.key):
					position = int(row[i])
					row[i] = values[1][position]

				# Write values
				sheet.append(row)

		# Build key for the next table
		if key is not None:
			position = table.header[key]
			next_key = [None] * (len(table.rows) + 1)
			for i, row in enumerate((*table.rows, table.row)):
				next_key[i] = row[position]
			if self.key is None:
				self.key = [(key, next_key)]
			else:
				self.key.append((key, next_key))
