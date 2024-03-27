from flask import Flask, jsonify, request 
import time
from utils import get_current_event,core_function
import json
import gmailAPI.mailAPI as gmail
import event_scheduler

last_mails = dict()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/get_current', methods=['GET'])
def return_current_event() -> dict:
    current_event = get_current_event()
    current_time = time.strptime(current_event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z")
    result = {
        "event_name": current_event["summary"],
        "event_time": f"{current_time.tm_hour}:{current_time.tm_min}",
        "event_description": ""
    }
    return jsonify(result), 200

@app.route('/api/schedule', methods=['GET','POST'])
def schedule():
    event_scheduler.make_schedule()
    return jsonify({'message': 'success'}), 200
 
@app.route('/api/delete_calendar', methods=['GET'])
def deleteCalendar():
    event_scheduler.delete_calendar()
    return jsonify({'message': 'success'}), 200 

@app.route('/gmail/add_user', methods=['POST'])
def add_email():
    with open('user_email_list.json','r',encoding='utf-8') as f:
        email_users = json.load(f)
    request_data = request.get_json()
    user,email = request_data["user"].strip(),request_data["email"].strip()
    if(user not in email_users) and email != "":
        email_users[user] = [email]
    elif email not in email_users[user] and email != "":
        email_users[user].append(email)
    with open('user_email_list.json','w',encoding='utf-8') as f:
        json.dump(email_users,f,ensure_ascii=False)
    return jsonify({'message': 'success'}), 200

@app.route('/gmail/get_accounts', methods=['GET'])
def get_accounts():
    user = request.args.get('user')
    with open('user_email_list.json','r',encoding='utf-8') as f:
        email_users = json.load(f)
    if user in email_users:
        result = jsonify({"accounts":email_users[user]}), 200
    else:
        result =  jsonify({"accounts":[]}), 200
    print(result[0].json)
    return result


@app.route('/gmail/get_mails', methods=['GET'])
def get_mails():
    user = request.args.get('user')
    messages = gmail.get_priority_mails("user_email_list.json",user,10)
    snippets = list()
    for messsage in messages:
        tmp = gmail.get_mail_content(messsage["id"],user)
        if tmp != "":
            snippets.append(tmp)
    last_mails[user] = snippets
    return jsonify({"length":len(snippets)}), 200

@app.route('/gmail/get_mail_no', methods=['GET'])
def get_mail_no():
    try:
        user = request.args.get('user')
        i = request.args.get('i')
        return jsonify({"msg":last_mails[user][int(i)]}), 200
    except:
        return jsonify({"msg":""}), 200

if __name__ == '__main__':
    app.run()
