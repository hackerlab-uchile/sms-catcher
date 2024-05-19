from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    
    # POST handler
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Assuming the data is in JSON format
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            print("Received JSON data:")
            print(json_data)
            self.send_response(200)
            self.end_headers()
            response = json.dumps({"message": "Data received successfully"})
            self.wfile.write(response.encode('utf-8'))
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            self.send_response(400)
            self.end_headers()
            response = json.dumps({"error": "Invalid JSON data"})
            self.wfile.write(response.encode('utf-8'))

# Server settings
port = 8002
server_address = ('', port)

# Create an HTTP server
httpd = HTTPServer(server_address, RequestHandler)

# Start the server
print('Starting the server on port', port)
httpd.serve_forever()
