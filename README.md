# Expense-Tracker-Chatbot
![Capture](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/9a6671de-7622-43d0-be17-496f81a6da7a)
![Capture2](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/bbe85bda-a312-4d14-988f-91725aa5bd00)
![Capture3](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/446590cf-5462-43a6-a0a5-19c2243490eb)
![Capture4](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/b5ef0e60-c170-40b9-bbce-b863fca13849)
![Capture5](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/9fe7b1d2-1d70-4e39-8d7a-eaaf54d49244)
![Capture6](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/4659157f-57ce-48f5-8ad3-392a89ee2a04)
![Capture7](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/a69772ef-5883-4007-80ba-5da5ebd3ec33)
![Capture8](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/58605294-19bf-4147-b02d-2888b82606f6)
![Capture9](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/acccf488-6104-42a2-97fb-dba226b05fc3)
![Capture10](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/f524d176-7b18-4c2f-abf4-92d61b710419)
![Capture11](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/028a15fe-cadc-49bb-8251-66e9acf6b99c)
![Capture12](https://github.com/ImaneMdn/Expense-Tracker-Chatbot/assets/115882702/64ece61f-8102-40fb-8fee-3a38d36f1ab5)

## Problem Statement:

Managing personal finances and tracking expenses can be a cumbersome task, often leading to disorganized records and overspending. The need for a streamlined solution to simplify expense tracking, budget management, and financial reporting is evident. Existing tools may lack user-friendly interfaces and real-time insights, contributing to the persistent challenge of maintaining a comprehensive view of one's financial landscape.

## Objective:

To address the identified financial management challenges, I embarked on the creation of an Expense Tracker Chatbot. The objectives are:

1. Define Seamless User Interactions: Utilize Dialogflow to create intuitive intents, entities, and ongoing contexts, ensuring a user-friendly chatbot experience for efficient expense tracking.

2. Enable Database Integration: Develop SQL queries and implement mysql.connector to interact with a MySQL database. This facilitates tasks such as adding expenses, setting budgets, and querying spending summaries in a structured and organized manner.

3. Build a Robust Web Service: Implement a powerful web service using FastAPI, structuring API endpoints to seamlessly handle various chatbot functionalities, ensuring reliability and responsiveness.

4. Facilitate Data Extraction for Reporting: Extract relevant data from the MySQL database to create comprehensive reports using Power BI. These reports cover a spectrum of financial insights, including expenses, budgets, and spending summaries.

## Directory structure:
===================
1. main.py: Contains Python FastAPI backend code.
2. db: contains the dump of the database. you need to import this into your MySQL db by using MySQL workbench tool.
3. frontend: website code.

## Install these modules
======================

1. pip install mysql-connector..
2. pip install fastapi.

## To start fastapi backend server
================================
1. Run this command: uvicorn main:app --reload.

## ngrok for https tunneling
================================
1. To install ngrok, go to https://ngrok.com/download and install ngrok version that is suitable for your OS.
2. Extract the zip file and place ngrok.exe in a folder.
3. Open windows command prompt, go to that folder and run this command: ngrok http 80000.

NOTE: ngrok can timeout. you need to restart the session if you see session expired message.
