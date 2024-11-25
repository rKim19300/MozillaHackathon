from database.database import db, clear_db, vector_store


# the same concept of how many words llamafile will take in during a certain call
# The max safe chunk size is 2700, but we remove 700 because of the prompt
MAX_SAFE_CHUNK_SIZE = 2000
CHUNK_NUM = 3
CHUNK_SIZE = int(MAX_SAFE_CHUNK_SIZE / CHUNK_NUM)


def read_dict(dictionary):
    text_to_return = []
    for header, text in dictionary.items():
        combined = f"{header}: {text}"
        text_to_return.append(combined)
    return "\n".join(text_to_return)


def parse_file_into_chunks(file_text) -> None:
    """
        Parses the file into chunks and puts them into the vector store
    """

    words = file_text.split()

    current_chunk = []
    current_length = 0
    chunk_index = 1

    for word in words:
        word_length = len(word) + 1

        # checking if adding this word will exceed the max chunk size
        if current_length + word_length > CHUNK_SIZE:
            chunk_text = ' '.join(current_chunk)
            # if the chunk doesn't end with a period, we haven't completed a sentence
            # need to keep adding words until we've reached the end of a sentence
            if not chunk_text.endswith('.'):
                while chunk_text and not chunk_text.endswith('.'):
                    current_chunk.pop()
                    chunk_text = ' '.join(current_chunk)

            # Add the chunk to the vector store
            vector_store.add_texts(texts=[chunk_text])

            current_chunk = [word]
            current_length = word_length
            chunk_index += 1
        else:
            current_chunk.append(word)
            current_length += word_length

    # add last chunk if any remaining content
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        if not chunk_text.endswith('.'):
            while chunk_text and not chunk_text.endswith('.'):
                current_chunk.pop()
                chunk_text = ' '.join(current_chunk)
        vector_store.add_texts(texts=[chunk_text])

def vectorize_chunks(parsed_text_dict) -> None:
    """
        Calls parse_file_into_chunks, which put the chunks into a vector store
    """
    text = read_dict(parsed_text_dict)
    chunks_dict = parse_file_into_chunks(text)
    #return chunks_dict


def main_llamafile_call(parsed_text_dict):
    text = read_dict(parsed_text_dict)
    chunks_dict = parse_file_into_chunks(text)
    output = generate_summary(chunks_dict)
    return output

def find_most_similar_chunks(question) -> str:

    # Find the most similar chunks to the question
    chunks = vector_store.similarity_search("Ketanji Brown Jackson", k=CHUNK_NUM)

    # Concatenate the chunks together
    return "".join([chunk.page_content for chunk in chunks])