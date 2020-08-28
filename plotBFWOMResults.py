import requests
import json
import pandas as pd
import numpy as np 
from generators import BFWOMGenerator
from utils import plot_price_prediction
from random import seed
from random import randint
# seed random number generator
seed(1)

url = 'http://localhost:3002/predict'

wom_generator = BFWOMGenerator("/Users/adriangordon/Development/kerasseq2seq/data/generate.csv",15, 30, 10, 5)

print BFWOMGenerator.n_sequences
print BFWOMGenerator.within_sequence_iterations

#sample_generator = wom_generator.generateTrainingSample(1000, 15, 30, ["layprice1","backprice1","WOM"],10, ["layprice1","backprice1"],5)
#generate a training sample
#the_generator = wom_generator.generateTrainingSample(1, 15, 0,['layprice1','backprice1','WOM'],10,['layprice1','backprice1'],5)
#inputs, outputs = next(the_generator)
#print(inputs[0].shape, inputs[1].shape, outputs.shape)
#print(inputs)
#print(outputs)

# generate some integers
for _ in range(100):
	index1 = randint(0, 5000)
	index2 = randint(0, 14)
	#print(value)
	

	start_index = (index1 * 60) + 30 + index2
	end_index = start_index + 10

	sample_input_pd = BFWOMGenerator.data[start_index:end_index]
	sample_input = np.array(sample_input_pd[["layprice1","backprice1","WOM"]])
	sample_output_pd = BFWOMGenerator.data[end_index:end_index + 5]
	sample_output = np.array(sample_output_pd[["layprice1","backprice1"]])

	print sample_input
	print sample_output


	results_text = requests.post(url, data = json.dumps(sample_input.tolist()), headers = {"content-yype": "application/json"}).text

	#print results_text
	results = np.array(json.loads(results_text))
	#print results.shape
	results_transposed =  np.transpose(results)
	#results = json.loads(results_text)
	#print results_transposed.shape


	plot_price_prediction(sample_input,sample_output,results_transposed)