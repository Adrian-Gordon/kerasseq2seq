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
                                       bias_regularizer=self.config["bias_regulariser"])(self.decoder_outputs[0]) #first element of the returned array is the hidden state for each time step

    self.model = keras.models.Model(inputs=[self.encoder_inputs, self.decoder_inputs], outputs=self.outputs)
    self.model.compile(optimizer=self.config["optimiser"], loss=self.config["loss"])

  def train(self):
    self.model.fit_generator(self.config["train_data_generator"], steps_per_epoch=self.config["steps_per_epoch"], epochs=self.config["epochs"])

  def predict(self, x_encoder, x_decoder):

    return self.model.predict([x_encoder, x_decoder])

  def save(self):
    self.model.save(self.config['model_save_path'])

  def load(self):
    self.model.load(self.config['model_save_path'])
    print(model.summary)



