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
    self.logger = logging.getLogger('bfGenerator')
    self.logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./logging/bfgeneratorlogger.log')
    fh.setLevel(logging.DEBUG)
    self.logger.addHandler(fh)
    #print(BFGenerator.x_train)
    #print(BFGenerator.y_train)  

  def generateTrainingSample(self,batch_size, source_sequence_length, offset, input_sequence_length, target_sequence_length):
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

      input_data = np.array(input_sequence[['layprice1','laydepth1','layprice2','laydepth2','layprice3','laydepth3','layprice4','laydepth4','layprice5','laydepth5','layprice6','laydepth6','layprice7','laydepth7','layprice8','laydepth8','layprice9','laydepth9','layprice10','laydepth10','backprice1','backdepth1','backprice2','backdepth2','backprice3','backdepth3','backprice4','backdepth4','backprice5','backdepth5','backprice6','backdepth6','backprice7','backdepth7','backprice8','backdepth8','backprice9','backdepth9','backprice10','backdepth10']])
      input_batches.append(input_data)
      output_data = np.array(output_sequence[['layprice1']])
      output_batches.append(output_data)
      if len(input_batches) == batch_size:
        #print(input_batches)
        #print(output_batches)
        input_batches_array = np.array(input_batches)
        output_batches_array = np.array(output_batches)
        decoder_input_batches = np.zeros((batch_size, target_sequence_length, 1))
        input_batches = []
        output_batches = []
        self.logger.debug("size=%d start_index=%d within_sequqnce_offset %d", len(input_batches_array), start_index, within_sequence_offset)
        #self.logger.debug('batch input shape')
        yield([input_batches_array, decoder_input_batches], np.array(output_batches_array))

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
    self.loger.debug("getNextSequence start_index: %d dataset_offset: %d within_sequence_offset: %d within_sequqnce_iterations: %d", start_index, dataset_offset, within_sequence_offset, within_sequence_iterations)
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



#test
'''
bfgenerator = BFGenerator("/Users/adriangordon/Development/bftimeseries/nodejs/data/test.csv",60, 30, 10, 5)
print(BFGenerator.n_sequences)
print(BFGenerator.within_sequence_iterations)

the_generator = bfgenerator.generateTrainingSample(10, 60, 30, 10, 5)

for i in range(200):
  inputs, outputs = next(the_generator)
#print(inputs[0].shape, inputs[1].shape, outputs.shape)
  print(i,"Inputs:" ,inputs[0][0][0][0], "Outputs: ", outputs[0][0][0])
'''

#rval = bfgenerator.getNextSequence(540, 30, 16, 16, 10, 5, 60, 600)
#print(rval
