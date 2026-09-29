Welcome to TidBit, your own personal weekly planner!

TidBit lets you input your tasks for the week by name, date, time, and with a description. 
It will then further break down your schedule using AI to help organize steps for you to follow using the Task Breakdown.
Additionally, TidBit provides a chatbot aimed at giving you advice on how to fix your schedule and improve your study habits.
To keep you motivated, we have the Bit Breakdown, where each task you complete is a new "bit" that gets to party!

TidBit is a fun atmosphere designed to improve quality of life by helping organize and plan schedules;
that way, users have more time to do the things they love without worrying about pending tasks!

To run the program, you must run the following commnds in your terminal:
in TidBit\TidBit, run npm install 

In TidBit\TidBit\Gemini_Files, run pip install. You must also run python -m venv venv, then .\venv\Scripts\Activate.ps1
  - if pip install gives you trouble, run the following:
  - pip install --upgrade google-generativeai fastapi uvicorn python-dotenv
  - pip install Flask

From there, open two terminals: one for React and one for Python
1) In TidBit\TidBit\Gemini_Files on one terminal, run python main.py to start up the Flask backend
2) In the other terminal, in TidBit\TidBit, do npm run dev to begin the website
