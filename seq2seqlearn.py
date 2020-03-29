import keras
from model import SeqToSeqModel

#replace with import of appropriate generator
from generators import WOMGenerator
import json

with open('./config/config.json') as json_file:
    config = json.load(json_file)


#replace BFGenerator with appropriate data generator

config["train_data_generator"] = WOMGenerator(datafile_path=config["datafile_path"],
                                              source_sequence_length=config["source_sequence_length"],
                                              offset=config["offset"],
                                              input_sequence_length=config["input_sequence_length"],
                                              target_sequence_length=config["target_sequence_length"]).generateTrainingSample(
                                              batch_size=config["batch_size"],
                                              source_sequence_length=config["source_sequence_length"],
                                              offset=config["offset"],
                                              input_attributes=config["input_attributes"],
                                              input_sequence_length=config["input_sequence_length"],
                                              output_attributes=config["output_attributes"],
                                              target_sequence_length=config["target_sequence_length"])

config["kernel_regulariser"]= eval(config["kernel_regulariser"])
config["recurrent_regulariser"]= eval(config["recurrent_regulariser"])
config["bias_regulariser"]=eval(config["bias_regulariser"])
config["optimiser"]= eval(config["optimiser"])


model = SeqToSeqModel(config)
model.build()
print(model.model.summary())

generator=config["train_data_generator"]
print(WOMGenerator.n_sequences)
print(WOMGenerator.within_sequence_iterations)
x_data, y_data=next(generator)


history = model.model.fit(x=x_data, y=y_data, epochs=config["epochs"], verbose=2)
model.save()
print(history.history)