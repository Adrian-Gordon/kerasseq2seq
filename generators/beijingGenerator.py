import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler


class BeijingGenerator:
    data=[]
    scaler = StandardScaler()
    X_train=[]
    X_test=[]
    y_train=[]
    y_test=[]
    def __init__(self, datafile_path):
        BeijingGenerator.data = pd.read_csv(datafile_path)  

        BeijingGenerator.data.fillna(0, inplace = True)
        #   print(BeijingGenerator.data.head())
        ## One-hot encode 'cbwd'
        temp = pd.get_dummies(BeijingGenerator.data['cbwd'], prefix='cbwd')
        BeijingGenerator.data = pd.concat([BeijingGenerator.data, temp], axis = 1)
        del BeijingGenerator.data['cbwd'], temp

        #standardize 


        BeijingGenerator.data[['pm2.5', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']] = BeijingGenerator.scaler.fit_transform(BeijingGenerator.data[['pm2.5', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir']])

        #print(BeijingGenerator.data.head())

        ## Split into train and test - I used the last 1 month data as test, but it's up to you to decide the ratio
        df_train = BeijingGenerator.data.iloc[:(-31*24), :].copy()
        df_test = BeijingGenerator.data.iloc[-31*24:, :].copy()

        ## take out the useful columns for modeling - you may also keep 'hour', 'day' or 'month' and to see if that will improve your accuracy
        BeijingGenerator.X_train = df_train.loc[:, ['pm2.5', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']]#.values.copy()
        BeijingGenerator.X_test = df_test.loc[:, ['pm2.5', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']]#.values.copy()
        BeijingGenerator.y_train = df_train['pm2.5'].values.copy().reshape(-1, 1)
        BeijingGenerator.y_test = df_test['pm2.5'].values.copy().reshape(-1, 1)

    def generateTrainingSample(self,batch_size, steps_per_epoch, input_sequence_length, target_sequence_length):
        start_index = 0
        x_data = BeijingGenerator.X_train
        y_data = BeijingGenerator.y_train

        while True:
            if (start_index + input_sequence_length + target_sequence_length) > 800:
              start_index = 0

            for _ in range(steps_per_epoch):
              input_batches = []
              output_batches = []

              for x in range(batch_size):   #build a batch
                  an_input_sequence = x_data[start_index : start_index + input_sequence_length]
                  input_data = np.array(an_input_sequence[['pm2.5','DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']])
                  input_batches.append(input_data)

                  an_output_sequence = x_data[start_index + input_sequence_length  : start_index + input_sequence_length + target_sequence_length]
                  output_data = np.array(an_output_sequence[['pm2.5']])
                  output_batches.append(output_data)

                  if (start_index + input_sequence_length + target_sequence_length) > x_data.shape[0]:
                    start_index = 0
                  else:
                    start_index += (input_sequence_length + target_sequence_length)
              decoder_input_batches = np.zeros((batch_size, target_sequence_length, 1))
              yield([np.array(input_batches), decoder_input_batches], np.array(output_batches))


    def generateTestSample(self,batch_size, steps_per_epoch, input_sequence_length, target_sequence_length):
        start_index = 0
        x_data = BeijingGenerator.X_test
        y_data = BeijingGenerator.y_test

        while True:
#            if (start_index + input_sequence_length + target_sequence_length) > 500:
#              start_index = 0

            for _ in range(steps_per_epoch):
              input_batches = []
              output_batches = []

              for x in range(batch_size):   #build a batch
                  an_input_sequence = x_data[start_index : start_index + input_sequence_length]
                  input_data = np.array(an_input_sequence[['pm2.5','DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir', 'cbwd_NE', 'cbwd_NW', 'cbwd_SE', 'cbwd_cv']])
                  input_batches.append(input_data)

                  an_output_sequence = x_data[start_index + input_sequence_length  : start_index + input_sequence_length + target_sequence_length]
                  output_data = np.array(an_output_sequence[['pm2.5']])
                  output_batches.append(output_data)

                  if (start_index + input_sequence_length + target_sequence_length) > x_data.shape[0]:
                    start_index = 0
                  else:
                    start_index += (input_sequence_length + target_sequence_length)
              decoder_input_batches = np.zeros((batch_size, target_sequence_length, 1))
              yield([np.array(input_batches), decoder_input_batches], np.array(output_batches))




#test

#gd = BeijingGenerator('../data/PRSA_data_2010.1.1-2014.12.31.csv')
#gd.generateTrainingSample(2,1,10,5)

'''
beijing_generator = BeijingGenerator('../data/PRSA_data_2010.1.1-2014.12.31.csv').generateTrainingSample(batch_size=50, steps_per_epoch=5, input_sequence_length=20, target_sequence_length=20)

i = 0
while True:
  inputs, decoder_outputs = next(beijing_generator)
  if inputs[0].shape[0] != 50:
    print(i)
    print(inputs[0].shape)
    print(inputs[1].shape)
    print(decoder_outputs.shape)
  i = i + 1

'''

'''
#print(inputs[0])
  #print(inputs[1])
#print(decoder_outputs)


'''

'''inputs, decoder_outputs = next(beijing_generator)

print(inputs[0])
print(inputs[1])
print(decoder_outputs)
'''


#print(BeijingGenerator.X_train[0:30])
#test_inputs, test_outputs = gd.getTestSample(30,5,0)
#print(test_inputs)
#print(test_outputs)

#input_batches, output_batches = gd.getTrainingSample(1,30,5)
#print(input_batches)
#print(output_batches)
#gd.plot()


