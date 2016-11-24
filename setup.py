# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements

version = '0.0.1'
requirements = parse_requirements("requirements.txt", session="")

setup(
	name='organizational_management',
	version=version,
	description='Capture the organizational hierarchy in companies and have a view on the Delegation of Authorities when transactions are being performed',
	author='Cloude8',
	author_email='asneha@cloude8.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
