import json
from http.server import BaseHTTPRequestHandler

# Load the student marks from the JSON file
with open('q-vercel-python.json', 'r') as f:
    STUDENT_MARKS = json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
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
        return
