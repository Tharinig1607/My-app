import json
from http.server import BaseHTTPRequestHandler

# Load the student marks from the JSON file
with open('q-vercel-python.json', 'r') as f:
    STUDENT_MARKS = json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the request is for the API or static content
        if self.path.startswith('/api'):
            # Parse the query parameters for 'name'
            query = self.path.split('?')[1] if '?' in self.path else ''
            query_params = dict(param.split('=') for param in query.split('&')) if query else {}

            # Get the 'name' parameter from the query (can have multiple names)
            names = query_params.get('name', '').split(',')
            
            # Retrieve the marks for each student name
            marks = [next((student['marks'] for student in STUDENT_MARKS if student['name'] == name.strip()), None) for name in names]
            
            # Prepare the JSON response
            response = {
                "marks": marks
            }

            # Send JSON response with CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # If not an API request, serve static content
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Check if the request is for the root path ('/') or some other path
            if self.path == '/':
                self.path = '/index.html'  # Serve the index.html if root is requested

            # Open and return the static HTML file
            try:
                with open(f'public{self.path}', 'r') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.wfile.write(b"404 Not Found")
        
        return
