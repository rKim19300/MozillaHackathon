# TO-DO List

- To run the backend first step into the backend dir then type <code>pip install -r ./requirments.txt</code> and then <code>python main.py</code>

- Most of the parts below can be done synchonously, then wired together.

1. We are going to accept both pdf files and urls.
    - Make the Upload button accept a pdf <span style="color: green;">***(JW)***</span>
    - Add the textbox for the url <span style="color: green;">***(JW)***</span>
        - Make the functions to send either the pdf or the url to the backend <span style="color: blue;">***(RK)***</span>

2. Finish the two endpoints, one for PDFs and another for url web pages <span style="color: blue;">***(RK)***</span> 
    - Both of them will 
        - scrape the page and create a dict<section, content>
        - Feed the dict into the LLM, which will process the contents (this will be done in part 3 and 4)
        - Send two values using two differnt sockets
            - The output from the LLM
            - Whether it is sending a paragraph or a title 

3. Update the prompt so that it only its summary only outputs a limited number of words per section <span style="color: red;">***(MJ)***</span>

4. (Edit: try using what you have in llamafileConnection.py, then try this) Try using the ***AnalyzeDocumentChain*** from langchain.chain when querying the LLM.  This will map reduce the input and enhance the output. We can apply it to one section of the TOS at a time <span style="color: red;">***(MJ)***</span>
    - Make a function similar to stream_chunks() in main.py, which will be fed the dictionary from part 2.
    - Feed it one section of the TOS at a time (from the dictionary).
    - If this is too slow, perhaps scrap it

5. Format the output in the frontend <span style="color: green;">***(JW)***</span>
    - The stream that is returned has \n characters, convert them into the equivalent React/HTML versions
    - Make the headers look different from the output text

6. Have the .llamafile start automatically on boot up

7. Finish the docs

8. (optional) Enhancing the prompt further
    - Slip the 7 points into 7 different prompts and iterate over each section with 7 queries. Tell the LLM to not output anything if it is of no interest with regards to the question
