from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import numpy as np 

from generators import BFGenerator

config= {
    "num_input_features": 4,
    "num_output_features":2,
    "input_sequence_length":10,
    "target_sequence_length": 5,
    "model_save_path":"./data/kerasmodel.h5"
    
}


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
    print(prediction_input_data)
    print(decoder_input_data)



if __name__ == '__main__':
  server = HTTPServer(('',3002), InferenceServerHandler)
  print("listening on port 3002")
  server.serve_forever()