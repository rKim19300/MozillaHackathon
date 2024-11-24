#!/usr/bin/env python3
from openai import OpenAI
from langchain_community.llms.llamafile import Llamafile

def main():
    '''
    client = OpenAI(
        base_url="http://localhost:8083",  # Run your llamafile first, this is the port that it's running on
        api_key="sk-no-key-required"
    )

    sampleText = "Hello world"

    prompt = f"""
        Please read the following privacy policy or terms of service and summarize the key points and concerns regarding the collection, use, and sharing of consumer data. Specifically, focus on:
    
        1. What types of data are being collected (e.g., personal information, browsing data, payment details, etc.).
        2. How the data is being used (e.g., for advertising, service improvement, sharing with third parties, etc.).
        3. Who the data is being shared with (e.g., third-party partners, advertisers, government authorities, etc.).
        4. How long the data is retained and under what conditions it is deleted or anonymized.
        5. Any rights or control given to consumers over their data (e.g., opt-out options, data access, correction, or deletion requests).
        6. Security measures in place to protect consumer data.
        7. Any potential risks or concerns related to data privacy or data sharing.
    
        Provide a concise bullet-point summary highlighting these key aspects.
    
        ----
        {sampleText}
        """

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system",
             "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    response = completion.choices[0].message

    print(response.content)
'''

    llm = Llamafile()
    llm.base_url = f"http://localhost:{8083}"

    print("Running llamafile")

    query = "Tell me a joke"

    for chunks in llm.stream(query):
        print(chunks, end="")

    print()

if __name__ == "__main__":
    main()