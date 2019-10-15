import numpy as np
import keras

class SeqToSeqModel:
  def __init__(self, config):
    self.config = config

  def build(self):
    #Build the encoder
    # Define an input sequence.
    self.encoder_inputs = keras.layers.Input(shape=(None, self.config["num_input_features"]))
    self.encoder_states = keras.layers.GRU(self.config["gru_neurons"], return_sequences=True, return_state=True,
                                          kernel_regularizer=self.config["kernel_regulariser"],
                                          recurrent_regularizer=self.config["recurrent_regulariser"],
                                          bias_regularizer=self.config["bias_regulariser"])(self.encoder_inputs)
    #define the decoder

    self.decoder_inputs = keras.layers.Input(shape=(None, 1))

    self.decoder_outputs = keras.layers.GRU(self.config["gru_neurons"], return_sequences=True, return_state=True,
                                          kernel_regularizer=self.config["kernel_regulariser"],
                                          recurrent_regularizer=self.config["recurrent_regulariser"],
                                          bias_regularizer=self.config["bias_regulariser"])(self.decoder_inputs, initial_state = self.encoder_states[1])

    #define the output layer

    self.outputs = keras.layers.Dense(self.config["num_output_features"],
                                       activation='linear',
                                       kernel_regularizer=self.config["kernel_regulariser"],
                                       bias_regularizer=self.config["bias_regulariser"])(decoder_outputs[0]) #first element of the returned array is the hidden state for each time step

    self.model = keras.models.Model(inputs=[self.encoder_inputs, self.decoder_inputs], outputs=self.outputs)
    self.model.compile(optimizer=self.config["optimiser"], loss=self.config["loss"])

  def build_old(self):

    #Build the encoder
    # Define an input sequence.
    self.encoder_inputs = keras.layers.Input(shape=(None, self.config["num_input_features"]))


    # Create a list of RNN Cells, these are then concatenated into a single layer
    # with the RNN layer.
    self.encoder_cells = []
    for hidden_neurons in self.config["layers"]:
      self.encoder_cells.append(keras.layers.GRUCell(hidden_neurons,
                                                  kernel_regularizer=self.config["kernel_regulariser"],
                                                  recurrent_regularizer=self.config["recurrent_regulariser"],
                                                  bias_regularizer=self.config["bias_regulariser"]))

    self.encoder = keras.layers.RNN(self.encoder_cells, return_state=True)

    self.encoder_outputs_and_states = self.encoder(self.encoder_inputs)

    # Discard encoder outputs and only keep the states.
    # The outputs are of no interest to us, the encoder's
    # job is to create a state describing the input sequence.
    self.encoder_states = self.encoder_outputs_and_states[1] #1:

#a dense layer to  resize the output states from the encoder to match the required shape of the input states to the decoder 
    self.encoder_dense = keras.layers.Dense(self.config["target_sequence_length"],
                                       activation='linear',
                                       kernel_regularizer=self.config["kernel_regulariser"],
                                       bias_regularizer=self.config["bias_regulariser"])

    self.resized_encoder_states = self.encoder_dense(self.encoder_states)


    # The decoder input will be set to zero (see random_sine function of the utils module).
    # Do not worry about the input size being 1, I will explain that in the next cell.
    self.decoder_inputs = keras.layers.Input(shape=(None, 1))

    self.decoder_cells = []
    for hidden_neurons in self.config["layers"]:
        self.decoder_cells.append(keras.layers.GRUCell(hidden_neurons,
                                                  kernel_regularizer=self.config["kernel_regulariser"],
                                                  recurrent_regularizer=self.config["recurrent_regulariser"],
                                                  bias_regularizer=self.config["bias_regulariser"]))

    self.decoder = keras.layers.RNN(self.decoder_cells, return_sequences=True, return_state=True)

    # Set the initial state of the decoder to be the ouput state of the encoder.
    # This is the fundamental part of the encoder-decoder.
    self.decoder_outputs_and_states = self.decoder(self.encoder_inputs, initial_state=self.resized_encoder_states)

    # Only select the output of the decoder (not the states)
    self.decoder_outputs = self.decoder_outputs_and_states[0]

    # Apply a dense layer with linear activation to set output to correct dimension
    # and scale (tanh is default activation for GRU in Keras, our output sine function can be larger then 1)
    self.decoder_dense = keras.layers.Dense(self.config["num_output_features"],
                                       activation='linear',
                                       kernel_regularizer=self.config["kernel_regulariser"],
                                       bias_regularizer=self.config["bias_regulariser"])

    self.decoder_outputs = self.decoder_dense(self.decoder_outputs)

    # Create a model using the functional API provided by Keras.
    # The functional API is great, it gives an amazing amount of freedom in architecture of your NN.
    # A read worth your time: https://keras.io/getting-started/functional-api-guide/ 
    self.model = keras.models.Model(inputs=[self.encoder_inputs, self.decoder_inputs], outputs=self.decoder_outputs)
    self.model.compile(optimizer=self.config["optimiser"], loss=self.config["loss"])

  def train(self):
    self.model.fit_generator(self.config["train_data_generator"], steps_per_epoch=self.config["steps_per_epoch"], epochs=self.config["epochs"])

  def predict(self, x_encoder, x_decoder):

    return self.model.predict([x_encoder, x_decoder])



