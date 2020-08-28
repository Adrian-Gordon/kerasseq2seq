from generators import BFWOMGenerator
import json

with open('./config/config.json') as json_file:
    config = json.load(json_file)


#replace BFGenerator with appropriate data generator

generator = BFWOMGenerator(datafile_path=config["datafile_path"],
                                              source_sequence_length=config["source_sequence_length"],
                                              offset=config["offset"],
                                              input_sequence_length=config["input_sequence_length"],
                                              target_sequence_length=config["target_sequence_length"])

tsGen = generator.generateTrainingSample(batch_size=config["batch_size"],
                                source_sequence_length=config["source_sequence_length"],
                                offset=config["offset"],
                                input_attributes=config["input_attributes"],
                                input_sequence_length=config["input_sequence_length"],
                                output_attributes=config["output_attributes"],
                                target_sequence_length=config["target_sequence_length"])

inputs, outputs = next(tsGen)