from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8887/v1",  # Run your llamafile first, this is the port that it's running on
    api_key="sk-no-key-required"
)

# the same concept of how many words llamafile will take in during a certain call
max_safe_chunk_size = 2700


def read_dict(dictionary):
    text_to_return = []
    for header, text in dictionary.items():
        combined = f"{header}: {text}"
        text_to_return.append(combined)
    return "\n".join(text_to_return)


def parse_file_into_chunks(file_text):
    # dictionary to store the chunks for processing
    chunks = {}

    words = file_text.split()

    current_chunk = []
    current_length = 0
    chunk_index = 1

    for word in words:
        word_length = len(word) + 1

        # checking if adding this word will exceed the max chunk size
        if current_length + word_length > max_safe_chunk_size:
            chunk_text = ' '.join(current_chunk)
            # if the chunk doesn't end with a period, we haven't completed a sentence
            # need to keep adding words until we've reached the end of a sentence
            if not chunk_text.endswith('.'):
                while chunk_text and not chunk_text.endswith('.'):
                    current_chunk.pop()
                    chunk_text = ' '.join(current_chunk)

            chunks[chunk_index] = chunk_text

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
        chunks[chunk_index] = chunk_text

    return chunks


def call_llamafile(prompt):
    # Call llamafile
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system",
             "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via "
                        "helping them with their requests."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    print(completion)
    return completion


def generate_summary(prompt_chunks):
    response_summaries = []
    prev_summary = ""

    # will only iterate through 4*chunk_size for suitable runtime
    for prompt_chunk_text in list(prompt_chunks.items())[:4]:
        prompt = f"""Please read the following privacy policy or terms of service and summarize the key points 
        regarding the collection, use, and sharing of consumer data. Focus on the following categories:

        1. **Types of Data Collected**: What types of data are being collected?
        2. **Purpose of Data Usage**: How is the data being used?
        3. **Data Sharing**: Who is the data being shared with?
        4. **Data Retention and Deletion**: How long is the data retained and under what conditions is it deleted or anonymized?
        5. **Consumer Rights and Control**: What rights or control are given to consumers over their data?
        6. **Data Security Measures**: What security measures are in place to protect consumer data?
        7. **Risks and Concerns**: Are there any potential risks or concerns related to data privacy or data sharing?

        Provide a concise **bullet-point summary** highlighting these key aspects for each category. Be sure to **use 
        bullet points** for each point in your summary.

        You **do not need to include** the example below in your response. It is just to show the expected format:
        
        Example format (not to be included in the output):
        - Key point 1
        - Key point 2

        Now, please generate the bullet-point summary based on the provided text below:

        {prev_summary}

        ----
        {prompt_chunk_text}
        """

        completion = call_llamafile(prompt)

        summary = completion.choices[0].message.content.strip()
        summary = summary.rstrip('</s>')
        prev_summary = summary
        response_summaries.append(summary)

    # prev_summary will also hold our final summary at the end of the loop
    return prev_summary


def get_chunks(parsed_text_dict):
    text = read_dict(parsed_text_dict)
    chunks_dict = parse_file_into_chunks(text)
    return chunks_dict

def process_chunk(chunk):
    prompt = f"""Please read the following privacy policy or terms of service and summarize the key points 
    regarding the collection, use, and sharing of consumer data. Focus on the following categories:

    1. **Types of Data Collected**: What types of data are being collected?
    2. **Purpose of Data Usage**: How is the data being used?
    3. **Data Sharing**: Who is the data being shared with?
    4. **Data Retention and Deletion**: How long is the data retained and under what conditions is it deleted or anonymized?
    5. **Consumer Rights and Control**: What rights or control are given to consumers over their data?
    6. **Data Security Measures**: What security measures are in place to protect consumer data?
    7. **Risks and Concerns**: Are there any potential risks or concerns related to data privacy or data sharing?

    Provide a concise **bullet-point summary** highlighting these key aspects for each category. Be sure to **use 
    bullet points** for each point in your summary.

    You **do not need to include** the example below in your response. It is just to show the expected format:
    
    Example format (not to be included in the output):
    - Key point 1
    - Key point 2

    Now, please generate the bullet-point summary based on the provided text below:
    
    {chunk}
    """

    prompt2 = "Tell me a joke"

    return call_llamafile(prompt2)


def main_llamafile_call(parsed_text_dict):
    text = read_dict(parsed_text_dict)
    chunks_dict = parse_file_into_chunks(text)
    output = generate_summary(chunks_dict)
    return output
