import json
from http.server import BaseHTTPRequestHandler
import os

# Dummy data for student marks
STUDENT_MARKS = {
    "Alice": 90,
    "Bob": 80,
    "Charlie": 70,
    "David": 85,
    "Eve": 95
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        query = self.path.split('?')[1] if '?' in self.path else ''
        query_params = dict(param.split('=') for param in query.split('&')) if query else {}
        
        # Get names from query parameters
        names = query_params.get('name', '').split(',')
        
        # Retrieve the marks for each name
        marks = [STUDENT_MARKS.get(name.strip(), None) for name in names]
        
        # Prepare the JSON response
        response = {
            "marks": marks
        }

        # Send JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
