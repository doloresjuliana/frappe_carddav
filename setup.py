from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_carddav/__init__.py
from frappe_carddav import __version__ as version

setup(
	name="frappe_carddav",
	version=version,
	description="Integrate Frappe contacts with some CardDav servers",
	author="Dolores Juliana",
	author_email="https://github.com/doloresjuliana",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
