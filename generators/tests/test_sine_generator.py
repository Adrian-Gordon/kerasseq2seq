import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

import mock

from sineGenerator import SineGenerator

def test_generates_sines():
	sine_generator = SineGenerator()

	data = sine_generator.generate()

	print(data)