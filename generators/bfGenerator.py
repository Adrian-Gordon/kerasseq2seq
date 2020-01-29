import pandas as pd
import numpy as np 
import logging


class BFGenerator:
  def __init__(self, datafile_path,source_sequence_length, offset, input_sequence_length, target_sequence_length):
    BFGenerator.data = pd.read_csv(datafile_path)
    BFGenerator.x_train = BFGenerator.data[['layprice1','laydepth1','layprice2','laydepth2','layprice3','laydepth3','layprice4','laydepth4','layprice5','laydepth5','layprice6','laydepth6','layprice7','laydepth7','layprice8','laydepth8','layprice9','laydepth9','layprice10','laydepth10','backprice1','backdepth1','backprice2','backdepth2','backprice3','backdepth3','backprice4','backdepth4','backprice5','backdepth5','backprice6','backdepth6','backprice7','backdepth7','backprice8','backdepth8','backprice9','backdepth9','backprice10','backdepth10']]
    BFGenerator.y_train = BFGenerator.data[['layprice1']]  

    BFGenerator.within_sequence_iterations = source_sequence_length - offset -input_sequence_length - target_sequence_length + 1

    BFGenerator.n_sequences = len(BFGenerator.x_train) / source_sequence_length  * BFGenerator.within_sequence_iterations
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
    datafile_length = len(BFGenerator.x_train)
    #print(datafile_length)

    while True:
      start_index, within_sequence_offset, input_sequence, output_sequence  = self.getNextSequence(start_index, offset, within_sequence_iterations, within_sequence_offset, input_sequence_length, target_sequence_length, source_sequence_length, datafile_length)

     # input_data = np.array(input_sequence[['layprice1','laydepth1','layprice2','laydepth2','layprice3','laydepth3','layprice4','laydepth4','layprice5','laydepth5','layprice6','laydepth6','layprice7','laydepth7','layprice8','laydepth8','layprice9','laydepth9','layprice10','laydepth10','backprice1','backdepth1','backprice2','backdepth2','backprice3','backdepth3','backprice4','backdepth4','backprice5','backdepth5','backprice6','backdepth6','backprice7','backdepth7','backprice8','backdepth8','backprice9','backdepth9','backprice10','backdepth10']])
      try:

        input_data = self.normalise_to_first_value(np.array(input_sequence[input_attributes])[0],np.array(input_sequence[input_attributes]))
        output_data = self.normalise_to_first_value(np.array(input_sequence[output_attributes])[0],np.array(output_sequence[output_attributes]))
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
    input_sequence = BFGenerator.x_train[input_sequence_start_index:input_sequence_end_index]
    #print(input_sequence["layprice1"])
    output_sequence_start_index = input_sequence_end_index 
    output_sequence_end_index = output_sequence_start_index + target_sequence_length
    output_sequence = BFGenerator.x_train[output_sequence_start_index:output_sequence_end_index]
    #print(output_sequence["layprice1"])
   
    within_sequence_offset = within_sequence_offset + 1
    return start_index, within_sequence_offset, input_sequence, output_sequence

  @classmethod
  def prepare_prediction_data(self, input_data, output_sequence_length ):
    normalised_input_data = self.normalise_to_first_value(input_data[0], input_data)
    decoder_input_data = np.zeros((1, output_sequence_length, 1))
    return np.array([normalised_input_data]), decoder_input_data

  @classmethod
  def process_prediction(self, input_data, indexes, output_data):

    zeroth = input_data[0]
    denormalised_output_data = []
#    print(zeroth)
    for col_i in range(output_data.shape[1]):
      index = indexes[col_i]
#      print(index, zeroth[index])
      denormalised_col = [((float(p) + 1.0) * float(zeroth[index])) for p in output_data[:, col_i]]
#      print(denormalised_col)
      denormalised_output_data.append(denormalised_col)
 #     denormalised_col = [((float(p) / float(zeroth[col_i])) - 1) for p in output_data[:, col_i]]
 #     normalised_output_data.append(denormalised_col)
 #   denormalised = np.array(normalised).T
    denormalised_output_data=np.array(denormalised_output_data).T
    return(denormalised_output_data)
 
  @classmethod
  def normalise_to_first_value(self, start_row_data, input_data):
    #print(input_data)
    #print(start_row_data)
    #print(input_data.shape[1])
    normalised = []
    for col_i in range(input_data.shape[1]):
      normalised_col = [((float(p) / float(start_row_data[col_i])) - 1) for p in input_data[:, col_i]]
      normalised.append(normalised_col)
    normalised = np.array(normalised).T
    return(normalised)

if __name__ == '__main__':
  #bfgenerator = BFGenerator("/home/adrian/Development/bftimeseries/nodejs/data/generate.csv",60, 30, 10,5)

  #data_to_normalise = np.array(bfgenerator.data[['layprice1','laydepth1','backprice1','backdepth1']])[30:40]
  data_to_normalise = np.array([[9.6,16.63,10.4,25.41],[10.5,27.53,10.0,3.54],[11.5,23.0,10.5,45.75],[12.0,10.58,11.5,20.7],[12.5,16.73,11.5,29.91],[12.0,11.62,11.5,31.73],[12.5,23.52,12.0,11.0],[12.5,16.04,12.0,135.51],[12.5,33.58,12.0,83.07],[12.5,5.0,12.0,71.94]])

  prediction_input_data, decoder_input_data = BFGenerator.prepare_prediction_data(data_to_normalise, 5)
  print(prediction_input_data, decoder_input_data)

  #post_processed_output_data = bfgenerator.process_prediction(data_to_normalise, [0,2], np.array([[0.19791667,0.10576923],[0.30208333,0.15384615],[0.25,-0.03846154]]))
  post_processed_output_data = BFGenerator.process_prediction(data_to_normalise, [0,1,2,3], np.array([[ 0.25, -0.36380036,  0.10576923, -0.18536009],[ 0.30208333,  0.00601323,  0.10576923,  0.17709563],[ 0.25      , -0.30126278,  0.10576923,  0.24872098],[ 0.30208333,  0.41431149,  0.15384615, -0.56709957]]))

  print(post_processed_output_data)



#  print(BFGenerator.n_sequences)
#  print(BFGenerator.within_sequence_iterations)

#  the_generator = bfgenerator.generateTrainingSample(1, 60, 30,['layprice1','laydepth1','backprice1','backdepth1'],10,['layprice1','backprice1'],5)#inputs, outputs = next(the_generator)
#  print(inputs[0].shape, inputs[1].shape, outputs.shape)
#  print(inputs)#print(outputs)
  
