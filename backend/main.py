from flask import Flask, make_response, request, jsonify
from langchain_community.llms.llamafile import Llamafile
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from utils import parse_webpage, extract_pdf_sections
from llamafile_utils import main_llamafile_call
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# Add the LLM as an object
llm = Llamafile()
llm.base_url = f"http://localhost:{8887}"

print("Running llamafile")


"""
    API routes
"""

@app.route("/api/summarize/url", methods=['POST'])
def summarize_url():

    data = request.get_json()    # Parse the JSON body
    url = data.get('url')

    content = parse_webpage(url) # Parse the webpage into a dict <title, section-content>

    llama_output = summarize_with_llama(content)

    # Send the query to the background to be processed
    # TODO Instead of passing in the query, we can pass in the content
    #query = "Write a 3 line Haiku \n" + url
    #socketio.start_background_task(target=stream_chunks, query=query)

    # Send a response back
    #headers = {"Content-Type" : "application/json"}

    #response = make_response("Success", 200)
    #response.headers.update(headers)

    return llama_output


@app.route("/api/summarize/pdf", methods=['POST'])
def summarize_pdf():

    uploaded_file = request.files.get('file')

    content = extract_pdf_sections(uploaded_file) # Pass in the pdf stream to be parsed

    # TODO fix it so the pdf scraper works
    print(content)

    llama_output = summarize_with_llama(content)

    # Send the query to the background to be processed
    # TODO Instead of passing in the query, we can pass in the content
    #query = "Write a 3 line Haiku \n" 
    #socketio.start_background_task(target=stream_chunks, query=query)

    # Send a response back
    #headers = {"Content-Type" : "application/json"}

    #response = make_response("Success", 200)
    #response.headers.update(headers)

    return llama_output


def summarize_with_llama(parsed_dict):
    # Send the query to the background to be processed
    # TODO Instead of passing in the query, we can pass in the content
    output = main_llamafile_call(parsed_dict)
    socketio.start_background_task(target=stream_chunks, query=output)

    # Send a response back
    headers = {"Content-Type" : "application/json"}

    response = make_response("Success", 200)
    response.headers.update(headers)

    return response
    



"""
    Sockets 
"""
# def stream_chunks(query):
    #for chunk in llm.stream(query):
    #    socketio.emit('update-summary', {'chunk': chunk})


def stream_chunks(query):
    sentences = re.split(r'(?<=\.)\s+', query)  # Split on period + space
    for sentence in sentences:
        socketio.emit('update-summary', {'chunk': sentence})



if __name__ == "__main__":
    socketio.run(app)