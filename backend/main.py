from flask import Flask, make_response, request, jsonify
from langchain_community.llms.llamafile import Llamafile
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from utils import parse_webpage, extract_pdf_sections
from llamafile_utils import vectorize_chunks, find_most_similar_chunks
from prompts import Questions, main_prompt
import re
import time
import atexit
from database.database import clear_db, db

# Clear the database when we close the program
def cleanup():
    print("Executing cleanup tasks...")
    clear_db()
    db.close()

atexit.register(cleanup)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# Add the LLM as an object
llm = Llamafile()
llm.base_url = f"http://localhost:{8080}"

"""
    API routes
"""

@app.route("/api/summarize/url", methods=['POST'])
def summarize_url():

    data = request.get_json()    # Parse the JSON body
    url = data.get('url')

    print('\n\nExtracting content from webpage . . .\n')
    content = parse_webpage(url) # Parse the webpage into a dict <title, section-content>

    response = summarize_with_llama(content)     

    return response


@app.route("/api/summarize/pdf", methods=['POST'])
def summarize_pdf():
    
    uploaded_file = request.files.get('file')

    content = extract_pdf_sections(uploaded_file) # Pass in the pdf stream to be parsed

    # Active socket
    response = summarize_with_llama(content)

    return response


def summarize_with_llama(parsed_dict):

    print("\n\nVectorizing the data . . . \n")
    vectorize_chunks(parsed_dict) # Put the scrapped data into the vector store

    print("\n\nExtracting Starting background socket . . . \n")
    socketio.start_background_task(target=stream_chunks)
    
    # Send a response back
    headers = {"Content-Type" : "application/json"}

    response = make_response("Success", 200)
    response.headers.update(headers)

    return response
    


"""
    Sockets 
"""

def stream_chunks():

    print("\n\nAsking Llamafile some questions . . . \n")
    for q_title, question in vars(Questions).items():

        # Skip non-questions
        if q_title.startswith("__") or callable(question):
            continue

        # Send the title to the frontend
        socketio.emit('update-summary', {'token': f"\n\n{q_title.replace("_", " ")}\n\n"})

        # Find the most similar chunks from our vector store
        chunk = find_most_similar_chunks(question)

        # Send the response to the question in pieces
        for t in llm.stream(main_prompt.format(question=question, relevant_chunks=chunk)):
            socketio.emit('update-summary', {'token': t})
    
    clear_db() # Clear the database after we are done
    

if __name__ == "__main__":
    socketio.run(app)