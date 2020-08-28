import pandas as pd
import numpy as np 
import logging


class BFWOMGenerator:
  def __init__(self, datafile_path,source_sequence_length, offset, input_sequence_length, target_sequence_length):
    BFWOMGenerator.data = pd.read_csv(datafile_path)
    BFWOMGenerator.data['WOM']= (BFWOMGenerator.data['laydepth1'] + BFWOMGenerator.data['laydepth2'] + BFWOMGenerator.data['laydepth3'] + BFWOMGenerator.data['laydepth4'] + BFWOMGenerator.data['laydepth5'] + BFWOMGenerator.data['laydepth6'] + BFWOMGenerator.data['laydepth7'] + BFWOMGenerator.data['laydepth8'] + BFWOMGenerator.data['laydepth9'] + BFWOMGenerator.data['laydepth10']) / (BFWOMGenerator.data['backdepth1'] + BFWOMGenerator.data['backdepth2'] + BFWOMGenerator.data['backdepth3'] + BFWOMGenerator.data['backdepth4'] + BFWOMGenerator.data['backdepth5'] + BFWOMGenerator.data['backdepth6'] + BFWOMGenerator.data['backdepth7'] + BFWOMGenerator.data['backdepth8'] + BFWOMGenerator.data['backdepth9'] + BFWOMGenerator.data['backdepth10']) 
    BFWOMGenerator.x_train = BFWOMGenerator.data[['layprice1','backprice1','WOM']]
    BFWOMGenerator.y_train = BFWOMGenerator.data[['layprice1']]  

    BFWOMGenerator.within_sequence_iterations = source_sequence_length - offset -input_sequence_length - target_sequence_length + 1

    BFWOMGenerator.n_sequences = len(BFWOMGenerator.x_train) / source_sequence_length  * BFWOMGenerator.within_sequence_iterations
    #self.logger = logging.getLogger('bfGenerator')
    #self.logger.setLevel(logging.DEBUG)
    #fh = logging.FileHandler('./logging/bfgeneratorlogger.log')
    #fh.setLevel(logging.DEBUG)
    #self.logger.addHandler(fh)
    #print(BFGenerator.x_train)
    #print(BFGenerator.y_train)  

  def generateTrainingSample(self,batch_size, source_sequence_length, offset, input_attributes,input_sequence_length, output_attributes,target_sequence_length):
    start_index = 0
    within_sequence_offset = 0
    input_batches =[]
    output_batches=[]

    within_sequence_iterations = source_sequence_length - offset -input_sequence_length - target_sequence_length + 1
    #print(within_sequence_iterations)
    datafile_length = len(BFWOMGenerator.x_train)
    #print(datafile_length)

    while True:
      start_index, within_sequence_offset, input_sequence, output_sequence  = self.getNextSequence(start_index, offset, within_sequence_iterations, within_sequence_offset, input_sequence_length, target_sequence_length, source_sequence_length, datafile_length)

     # input_data = np.array(input_sequence[['layprice1','laydepth1','layprice2','laydepth2','layprice3','laydepth3','layprice4','laydepth4','layprice5','laydepth5','layprice6','laydepth6','layprice7','laydepth7','layprice8','laydepth8','layprice9','laydepth9','layprice10','laydepth10','backprice1','backdepth1','backprice2','backdepth2','backprice3','backdepth3','backprice4','backdepth4','backprice5','backdepth5','backprice6','backdepth6','backprice7','backdepth7','backprice8','backdepth8','backprice9','backdepth9','backprice10','backdepth10']])
      with np.errstate(divide='raise'):
        try:

          input_data = self.normalise_input_to_difference(np.array(input_sequence[input_attributes]))
          output_data = self.normalise_output_to_difference(np.array(input_sequence[output_attributes]),np.array(output_sequence[output_attributes]))
        except:
          pass
        else:
          input_batches.append(input_data)
          output_batches.append(output_data)
          #print(len(input_batches))
          if len(input_batches) == batch_size:
            #print(input_batches)
            #print(output_batches)
            input_batches_array = np.array(input_batches)
            output_batches_array = np.array(output_batches)
            decoder_input_batches = np.zeros((batch_size, target_sequence_length, 1))
            input_batches = []
            output_batches = []
            #print("size=%d start_index=%d within_sequqnce_offset %d", len(input_batches_array), start_index, within_sequence_offset)
            #print('batch input shape: ', input_batches_array.shape)
            yield([input_batches_array, decoder_input_batches], np.array(output_batches_array))
        #except:
          #print("An exception")
          #print(i, start_index, within_sequence_offset)

  def getNextSequence(self, start_index, dataset_offset, within_sequence_iterations, within_sequence_offset, input_sequence_length, target_sequence_length, source_sequence_length, datafile_length):
    '''
    parameters: start_index                 - start index into the data set 
                dataset_offset              - offset into the source sequence to start (e.g. start from the 30th minute of a 60 minute sequence)
                within_sequence_iterations  - no of possible iterations within a sequence
                within_sequence_offset      - offset into a source sequence at which to start (e.g. start at the 2nd minute of the 30 minute sequence starting from the dataset_offset)
                input_sequence_length       - length of the input sequence
                target_sequence-length      - length of the target sequence
                datafile_length             - total numer of rows in the datafile
    returns: new index to start into the data set,
              new within sequence offset 
              input sequence
              output sequence

    '''
#    self.logger.debug("getNextSequence start_index: %d dataset_offset: %d within_sequence_offset: %d within_sequqnce_iterations: %d", start_index, dataset_offset, within_sequence_offset, within_sequence_iterations)
    if within_sequence_offset == within_sequence_iterations :
      #print("end of within sequence iterations")
      start_index = start_index + source_sequence_length
      within_sequence_offset = 0

    if(start_index >= datafile_length):#datafile_length): #go back to the start
        #print("Reached the end, go back to the start")
        start_index = 0
        within_sequence_offset = 0
       
    
    input_sequence_start_index = start_index + dataset_offset + within_sequence_offset
    input_sequence_end_index = input_sequence_start_index + input_sequence_length 
    #print(input_sequence_start_index )
    #print(input_sequence_end_index)
    input_sequence = BFWOMGenerator.x_train[input_sequence_start_index:input_sequence_end_index]
    #print(input_sequence["layprice1"])
    output_sequence_start_index = input_sequence_end_index 
    output_sequence_end_index = output_sequence_start_index + target_sequence_length
    output_sequence = BFWOMGenerator.x_train[output_sequence_start_index:output_sequence_end_index]
    #print(output_sequence["layprice1"])
   
    within_sequence_offset = within_sequence_offset + 1
    return start_index, within_sequence_offset, input_sequence, output_sequence

  @classmethod
  def prepare_prediction_data(self, input_sequence, output_sequence_length ):
    normalised_input_data = self.normalise_input_to_difference(np.array(input_sequence))
    decoder_input_data = np.zeros((1, output_sequence_length, 1))
    return np.array([normalised_input_data]), decoder_input_data

  @classmethod
  def process_prediction(self, input_data, indexes, output_data):
    start_values = np.reciprocal(input_data[-1]) # last observed elements (probability)
   # print(start_values)
    all_predicted_vals = np.array([])
    for index in range(indexes.shape[0]):
      #print("index: ",index)
      predicted_diffs = output_data[...,index]
      #print('predicted_diffs: ', predicted_diffs)
      next_predicted_val = start_values[index]
      #print("start predicted_val: ", next_predicted_val)
      predicted_vals = []
      for pd in predicted_diffs:
        #print('pd:', pd)
        next_predicted_val = next_predicted_val + pd
        #print('npv: ', next_predicted_val)
        predicted_vals.append(next_predicted_val)
      predicted_vals = np.reciprocal(np.array(predicted_vals))
      #print('predicted_vals', predicted_vals)
      all_predicted_vals = np.append(all_predicted_vals, predicted_vals, axis = 0)
    #print("all: ", all_predicted_vals)
    return(np.reshape(all_predicted_vals,(indexes.shape[0], output_data.shape[0])))


  #change data to be difference between data and previous value, as probabilities
  # this currently just works for 2 input columns
  @classmethod
  def normalise_input_to_difference(self, input_data):

    normalised = []

    normalised_col1 = np.diff(np.reciprocal(input_data[:, 0]))
    normalised_col1 = np.insert(normalised_col1,0,0.0, axis=0)
    #print(normalised_col1)

    normalised.append(normalised_col1)

    normalised_col2 = np.diff(np.reciprocal(input_data[:, 1]))
    normalised_col2 = np.insert(normalised_col2,0,0.0, axis=0)
    #print(normalised_col2)

    normalised.append(normalised_col2)

    col3 = input_data[:, 2]
    normalised.append(col3)

    normalised = np.array(normalised).T
    return normalised

  @classmethod
  def normalise_output_to_difference(self, input_data, output_data):
    lastElement0 = input_data[-1,0]
    lastElement1 = input_data[-1,1]
    #print(lastElement0)
    #print(lastElement1)

    normalised = []

    normalised_col1 = np.diff(np.reciprocal(np.insert(output_data[:, 0],0,lastElement0)))
    #normalised_col1 = np.insert(normalised_col1,0,0.0, axis=0)
    #print(normalised_col1)

    normalised.append(normalised_col1)

    normalised_col2 = np.diff(np.reciprocal(np.insert(output_data[:, 1],0,lastElement1)))
    #normalised_col2 = np.insert(normalised_col2,0,0.0, axis=0)
    #print(normalised_col2)

    normalised.append(normalised_col2)
    normalised = np.array(normalised).T
    return normalised

if __name__ == '__main__':
  wom_generator = BFWOMGenerator("/Users/adriangordon/Development/kerasseq2seq/data/generate.csv",60, 30, 10, 5)
 
  #generate a training sample
  the_generator = wom_generator.generateTrainingSample(1, 15, 0,['layprice1','backprice1','WOM'],10,['layprice1','backprice1'],5)
  inputs, outputs = next(the_generator)
  print(BFWOMGenerator.n_sequences);
  #print(inputs[0].shape, inputs[1].shape, outputs.shape)
  print(inputs)
  print(outputs)

  #normalise input data for prediction
#  n, d = wom_generator.prepare_prediction_data([[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.69,2.64,-0.48],[2.73,2.68,-0.48]], 5)
#  print(n)
 # print(d)

 #process a returned prediction
 # d = wom_generator.process_prediction(
 # np.array([[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.66,2.62,0],[2.69,2.64,-0.48],[2.73,2.68,-0.48]]),
 # np.array([0,1]), 
#  np.array([[-0.0041, -0.0051],[-0.0042, -0.0052],[-0.0043, -0.0053],[-0.0044, -0.0054],[-0.0045, -0.0055]]))

#  print(d)
