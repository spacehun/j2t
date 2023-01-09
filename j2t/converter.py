from j2t.table import Table
from j2t.writer import XLSXWriter
import json

class Converter:
	"""Converts JSON objects to table format.
	"""

	def __init__(self, main: str, keys: dict):
		"""Creates a converter.
		- main: name of the main table
		- keys: primary keys of each table
		"""

		# Tables. The keys are the name of the tables, the values are the tables themselves
		self.tables = {}

		self.keys = keys

		self.main = main

	def add(self, data: dict, name: str = None, key: tuple = None):
		"""Converts a JSON object and adds it to the set of tables.
		- data: content of the JSON object
		- name: name of the table the object belongs to
		- key: foreign key for this table
		"""

		# If no table name is provided, this is the main table
		if name is None:
			name = self.main

		# Find the table or create a new one if it doesn't exist yet
		try:
			table = self.tables[name]
			table.create_row(len(table.header))
		except KeyError:
			table = Table()
			self.tables[name] = table

		# Add foreign key
		if key is not None:
			for level in key:
				column, value = level
				table.add(column, value)

		# Add object fields
		for field, value in data.items():

			if isinstance(value, list):

				for object in value:

					# Build foreign key for the next table
					try:
						level = (self.keys[name], len(table.rows))
						next_key = (level,) if key is None else (*key, level)
					except KeyError:
						next_key = None

					self.add(object, field, next_key)

			else:
				table.add(field, value)

	def write(self, name: str = None):
		"""Writes the set of tables to a XLSX file.
		- name: file name
		"""

		writer = XLSXWriter(name)
		for name, table in self.tables.items():
			try:
				key = self.keys[name]
			except KeyError:
				key = None
			writer.write(name, table, key)
