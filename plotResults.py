import requests
import json
import pandas as pd
import numpy as np 
from generators import WOMGenerator
from utils import plot_price_prediction
from random import seed
from random import randint
# seed random number generator
seed(1)

url = 'http://localhost:3002/predict'

wom_generator = WOMGenerator("/Users/adriangordon/Development/kerasseq2seq/data/womData.csv",15, 0, 10, 5)

print WOMGenerator.n_sequences


# generate some integers
for _ in range(100):
	index = randint(0, WOMGenerator.n_sequences)
	#print(value)
	

	start_index = (index * 15)
	end_index = start_index + 10

	sample_input_pd = wom_generator.data[start_index:end_index]
	sample_input = np.array(sample_input_pd[["layprice1","backprice1","WOM"]])
	sample_output_pd = wom_generator.data[end_index:end_index + 5]
	sample_output = np.array(sample_output_pd[["layprice1","backprice1"]])

	#print sample_input
	#print sample_output


	results_text = requests.post(url, data = json.dumps(sample_input.tolist()), headers = {"content-yype": "application/json"}).text

	#print results_text
	results = np.array(json.loads(results_text))
	#print results.shape
	results_transposed =  np.transpose(results)
	#results = json.loads(results_text)
	#print results_transposed.shape


	plot_price_prediction(sample_input,sample_output,results_transposed)