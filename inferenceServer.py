from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from generators import BFGenerator


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

    self.data = json.loads(self.data_string)



if __name__ == '__main__':
  server = HTTPServer(('',3002), InferenceServerHandler)
  print("listening on port 3002")
  server.serve_forever()