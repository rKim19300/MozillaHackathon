from langchain_core.prompts.prompt import PromptTemplate


# Questions
class Questions:
    TYPES_OF_DATA_COLLECTED = "**Types of Data Collected**: What types of data are being collected?"

    PURPOSED_OF_DATA_USAGE = "**Purpose of Data Usage**: How is the data being used?"

    DATA_SHARING = "**Data Sharing**: Who is the data being shared with?"

    DATA_RETENTION_AND_DELETION = "**Data Retention and Deletion**: How long is the data retained and under what conditions is it deleted or anonymized?"

    CONSUMER_RIGHTS_AND_CONTROL = "**Consumer Rights and Control**: What rights or control are given to consumers over their data?"

    DATA_SECURITY_MEASURES = "**Data Security Measures**: What security measures are in place to protect consumer data?"

    RISKS_AND_CONCERNS = "**Risks and Concerns**: Are there any potential risks or concerns related to data privacy or data sharing?"



main_prompt = PromptTemplate.from_template(
"""Please read the following privacy policy or terms of service and summarize the key points 
regarding the question below:

{question}

Provide a concise summary highlighting this key aspects for each category. At most **use 
3 bullet points** and **at most 2 lines** for each point in your summary and keep each point. Use 
numbers for each point.

You **do not need to include** the example below in your response. It is just to show the expected format:

Example format (not to be included in the output):
1. Key point 1
2. Key point 2

Now, please generate the bullet-point summary based on the provided text below:

{relevant_chunks}
"""
    )
