#!/usr/bin/env python

from setuptools import setup

setup(
		name = "find-duplicate-images",
		version = "0.0.1",
		author = "Bach Phan",
		author_email = "bachp2@uw.edu",
		description = ("this Python script finds all duplicate images and deletes them using a simple GUI interface."),
		license = "MIT",
		install_requires = [
			'imagehash'
			'Pillow'
			'PyQt4'
		]
	)