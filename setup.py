from setuptools import setup

setup(
	name = 'j2t',
	version = '0.0.1',
	description = 'Convert JSON to XLSX',
	author = 'spacehun <spacesus@proton.me>',
	packages = ['j2t'],
	install_requires = [
		'openpyxl',
	],
	extras_require = {
		'test': [
			'pandas',
			'pytest',
		]
	},
	scripts = ['bin/j2t'],
	python_requires = '>3.6',
)
