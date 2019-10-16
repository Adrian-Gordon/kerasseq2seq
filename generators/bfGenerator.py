import pandas as pd
import numpy as np 

class BFGenerator:
  def __init__(self, datafile_path):
    BFGenerator.data = pd.read_csv(datafile_path)
    BFGenerator.x_train = BFGenerator.data[['layprice1','laydepth1','layprice2','laydepth2','layprice3','laydepth3','layprice4','laydepth4','layprice5','laydepth5','layprice6','laydepth6','layprice7','laydepth7','layprice8','laydepth8','layprice9','laydepth9','layprice10','laydepth10','backprice1','backdepth1','backprice2','backdepth2','backprice3','backdepth3','backprice4','backdepth4','backprice5','backdepth5','backprice6','backdepth6','backprice7','backdepth7','backprice8','backdepth8','backprice9','backdepth9','backprice10','backdepth10']]
    BFGenerator.y_train = BFGenerator.data[['layprice1']]  

    #print(BFGenerator.x_train)
    #print(BFGenerator.y_train)  

  def generateTrainingSample(self,batch_size, source_sequence_length, offset, input_sequence_length, target_sequence_length):

    start_index = 0


    within_sequence_iterations = source_sequence_length - offset -input_sequence_length - target_sequence_length + 1

    print(within_sequence_iterations)

    for i in range(within_sequence_iterations):
      input_sequence_start_index = start_index + offset + i 
      input_sequence_end_index = input_sequence_start_index + input_sequence_length
      #print(input_sequence_start_index )
      #print(input_sequence_end_index)
      input_sequence = BFGenerator.x_train[input_sequence_start_index:input_sequence_end_index]
      print(input_sequence)
      output_sequence_start_index = input_sequence_end_index 
      output_sequence_end_index = output_sequence_start_index + target_sequence_length
      output_sequence = BFGenerator.x_train[output_sequence_start_index:output_sequence_end_index]
      print(output_sequence)


#test

bfgenerator = BFGenerator("/home/adrian/Development/bftimeseries/nodejs/data/testdata.csv")

bfgenerator.generateTrainingSample(1, 60, 30, 10, 5)