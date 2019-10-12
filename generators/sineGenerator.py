# This file contains code modified licensed under the MIT License:
# Copyright (c) 2017 Guillaume Chevalier # For more information, visit:
# https://github.com/guillaume-chevalier/seq2seq-signal-prediction
# https://github.com/guillaume-chevalier/seq2seq-signal-prediction/blob/master/LICENSE

"""Contains functions to generate artificial data for predictions as well as 
a function to plot predictions."""

import numpy as np
from matplotlib import pyplot as plt

class SineGenerator:
    
   	def generate(self,batch_size, steps_per_epoch,
                input_sequence_length, target_sequence_length,
                min_frequency=0.1, max_frequency=10,
                min_amplitude=0.1, max_amplitude=1,
                min_offset=-0.5, max_offset=0.5,
                num_signals=3, seed=43):
	    '''Produce a batch of signals.
	    The signals are the sum of randomly generated sine waves.
	    Arguments
	    ---------
	    batch_size: Number of signals to produce.
	    steps_per_epoch: Number of batches of size batch_size produced by the
	        generator.
	    input_sequence_length: Length of the input signals to produce.
	    target_sequence_length: Length of the target signals to produce.
	    min_frequency: Minimum frequency of the base signals that are summed.
	    max_frequency: Maximum frequency of the base signals that are summed.
	    min_amplitude: Minimum amplitude of the base signals that are summed.
	    max_amplitude: Maximum amplitude of the base signals that are summed.
	    min_offset: Minimum offset of the base signals that are summed.
	    max_offset: Maximum offset of the base signals that are summed.
	    num_signals: Number of signals that are summed together.
	    seed: The seed used for generating random numbers
	    
	    Returns
	    -------
	    signals: 2D array of shape (batch_size, sequence_length)
	    '''
	    num_points = input_sequence_length + target_sequence_length
	    x = np.arange(num_points) * 2*np.pi/30

	    while True:
	        # Reset seed to obtain same sequences from epoch to epoch
	        np.random.seed(seed)

	        for _ in range(steps_per_epoch):
	            signals = np.zeros((batch_size, num_points))
	            for _ in range(num_signals):
	                # Generate random amplitude, frequence, offset, phase 
	                amplitude = (np.random.rand(batch_size, 1) * 
	                            (max_amplitude - min_amplitude) +
	                             min_amplitude)
	                frequency = (np.random.rand(batch_size, 1) * 
	                            (max_frequency - min_frequency) + 
	                             min_frequency)
	                offset = (np.random.rand(batch_size, 1) * 
	                         (max_offset - min_offset) + 
	                          min_offset)
	                phase = np.random.rand(batch_size, 1) * 2 * np.pi 
	                         

	                signals += amplitude * np.sin(frequency * x + phase)
	            signals = np.expand_dims(signals, axis=2)
	            
	            encoder_input = signals[:, :input_sequence_length, :]
	            decoder_output = signals[:, input_sequence_length:, :]
	            
	            # The output of the generator must be ([encoder_input, decoder_input], [decoder_output])
	            decoder_input = np.zeros((decoder_output.shape[0], decoder_output.shape[1], 1))
	            yield ([encoder_input, decoder_input], decoder_output)

