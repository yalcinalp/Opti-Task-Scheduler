# algorithmicacrobats
This repo is the final project which managed to get 1st place in the Goldman Sachs Warsaw 24-Hour Hackathon. 
Our teams consists of:  
    Alp Eren Yalçın - [yalcinalp](https://github.com/yalcinalp)  
    Doğancem Duran - [dogancemd](https://github.com/dogancemd)  
    Emre Geçit - [gecitemre](https://github.com/gecitemre)  
    Yusufhan Ali Üstün - [yusufhanali](https://github.com/yusufhanali)  

This web extension is connected to your Jira, Google Calendar and Gmail accounts. It has three main functionality:  
-To fetch tasks from Jira, sort them according to their dependency and priority, then create events and add them to your Google Calendar.  
-To display mails from preadded accounts in the extension.  
-To give you a chance to rate your daily productivity and work-life balance.  



To run the project:
1. Get Google Gmail and Calendar API JSON
2. Get Jira API keys
3. Add browser extension to a web browser placed in the extension
4. Fill the API key field in the Server/jira.py
5. Change the credentials.json and mail_credentials.json with your credentials(Google API Keys)
6. Run the Server/rest.py on local.
7. You can now fully utilize the extension.
