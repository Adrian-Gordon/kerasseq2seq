import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

import mock

from sineGenerator import SineGenerator

def test_generates_sines():
	sine_generator = SineGenerator().generate(5, 1, 10, 8)

	inputs, outputs = next(sine_generator)

	assert len(inputs) == 2 	#encoder input and (zero)  decoder input, decoder output
	assert len(inputs[0]) == 5	#batch size
	assert len(inputs[0][0]) == 10 #input sequence length
	assert len(inputs[0][0][0]) == 1 #input attributes 

	assert len(outputs) == 5 #batch size
	assert len(outputs[0]) == 8 #output sequence length
	assert len(outputs[0][0]) == 1 #output attributes