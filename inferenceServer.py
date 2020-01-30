from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import numpy as np 

import keras
from model import SeqToSeqModel
from generators import BFGenerator

with open('./config/config.json') as json_file:
    config = json.load(json_file)

#LOAD AN EXISTING TRAINED MODEL
model = SeqToSeqModel(config)
model.load()
print("MODEL SUMMARY: ")
print(model.model.summary())


class InferenceServerHandler(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()

  def do_POST(self):
    if(self.path == '/predict'):
      self.do_inference()


  def do_inference(self):
    self._set_headers()

    self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")

    print(self.data_string)

    self.data = np.array(json.loads(self.data_string))
    prediction_input_data, decoder_input_data = BFGenerator.prepare_prediction_data(self.data, config['target_sequence_length'])
    predicted_y=model.predict(prediction_input_data, decoder_input_data)
    print(predicted_y)
    post_processed_predictions = BFGenerator.process_prediction(self.data,[0,2], predicted_y[0])
    print(post_processed_predictions)
    self.wfile.write(json.dumps(post_processed_predictions.tolist()).encode("utf-8"))
    #self.wfile.write(json.dumps(model.model.summary()).encode("utf-8"))



if __name__ == '__main__':
  server = HTTPServer(('',3002), InferenceServerHandler)
  print("listening on port 3002")
  server.serve_forever()

