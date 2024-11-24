from flask import Flask, make_response, request, jsonify
from langchain_community.llms.llamafile import Llamafile
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from utils import parse_webpage, extract_pdf_sections

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# Add the LLM as an object
llm = Llamafile()
llm.base_url = f"http://localhost:{8080}"

print("Running llamafile")


"""
    API routes
"""

@app.route("/api/summarize", methods=['POST'])
def summarize():

    data = request.get_json()  # Parse the JSON body
    terms = data.get('terms') 

    # Send the query to the background to be processed
    # TODO replace this query with the one we intend
    query = "Write a 3 line Haiku \n" + terms
    socketio.start_background_task(target=stream_chunks, query=query)

    # Send a response back
    headers = {"Content-Type" : "application/json"}

    response = make_response("Success", 200)
    response.headers.update(headers)

    return response

"""
    Sockets 
"""
def stream_chunks(query):
    for chunk in llm.stream(query):
        socketio.emit('update-summary', {'chunk': chunk})


if __name__ == "__main__":
    socketio.run(app)