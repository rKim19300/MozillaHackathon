# Mozilla's Next Generation AI Developers Hackathon

## Demo

<video src="./SafeScan-Demo-mp4.mp4" width="320" height="240" controls></video>

## Description

For this Hackathon, we were challenged to build an AI solution using Mozilla's Llamafile to protect users personal activities and information online.

Users are often overwhelmed by long, complex, and legalistic Terms of Service (ToS) and Privacy Policy agreements when interacting with online platforms. Despite being essential for user protection, these agreements are rarely read or understood by the average consumer. This leaves a user vulnerable to misuse of their data and privacy violations.

Our solution leverages Mozilla's Llamafile AI technology to empower users to make informed decisions about the services they use by simplifying the process of understanding complicated ToS and Privacy Policy agreements.

### How It Works:

1. **Parsing and Summarization**: Users can easily upload a PDF file or provide a website URL containing a Terms of Service or Privacy Policy. The text is parsed through and sent to Llamafile for summarization. Llamafile will identify the most important sections.
2. **Highlighting Concerns**: Llamafile doesn’t just summarize the text—it also analyzes the content for potentially concerning or harmful practices. This allows users to quickly identify privacy risks and make informed decisions about their online activities, knowing exactly what they’re agreeing to.
3. **User-Friendly Interface**: Our platform presents the summarized document in a format that’s easy for the user to understand.

### RAG Pipeline

![alt text](diagram/SafeScanRAG.png)

### Technology Stack

- Next.js (Frontend)
- Flask w/ Socket.io (Backend)
- Sqlite-vec (vector database)
- Beautiful Soup (Web Scraping)
- Mozilla's Llamafile (AI Engine)
- Langchain (LLM Orchestration)

## Set Up and Installation Instructions

### Frontend

1. Navigate to the frontend directory

```
cd frontend/mozillafrontend
```

2. Install Necessary Dependencies

```
npm install
```

3. Download Llamafile:

- Run the following command to set up Llamafile in the project:

```
npm run setup
```

4. Start the Project

- To start the project, type the following in the terminal:

```
npm start
```

### Backend

1. Navigate to Backend Directory

```
cd backend
```

2.  Install Dependencies

- Install required Python packages:

```
pip install -r ./requirements.txt
```

3. Run Backend Server

- Start the backend service:

```
python main.py
```
