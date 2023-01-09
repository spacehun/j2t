from j2t import Converter
import getopt
import json
import sys

HELP = """Usage:  j2t [OPTIONS] INPUT OUTPUT

Converts a JSON array of objects to XLSX format

Options:
  -m   Name of the main table. The default name is "main"
  -k   Fields to use as primary keys for each table
"""

def main():

	# Parse CLI arguments
	options = parse_arguments(sys.argv[1:])
	if options is None:
		exit(1)
	input, output, main, keys = options

	# Read JSON data and convert
	with open(input, 'r') as file:
		converter = Converter(main, keys)
		try:
			data = json.loads(file.read())
		except json.decoder.JSONDecodeError:
			error('Error: invalid JSON')
			exit(1)
		for object in data:
			converter.add(object)
		converter.write(output)

def parse_arguments(arguments: list) -> tuple:
	"""Parses the program options.
	"""

	try:
		flags, remainder = getopt.getopt(arguments, 'm:k:')
	except Exception:
		error(HELP)
		return None
	if len(remainder) != 2:
		error(HELP)
		return None
	input = remainder[0]
	output = remainder[1]
	main = 'main'
	keys = { }
	for flag, value in flags:
		if flag == '-m':
			main = value
		elif flag == '-k':
			try:
				keys = json.loads(value)
			except json.decoder.JSONDecodeError:
				error('Error: keys are invalid JSON')
				return None
	return (input, output, main, keys)

def error(message: str):
	"""Prints an error message to stderr.
	"""

	print(message, file = sys.stderr)
