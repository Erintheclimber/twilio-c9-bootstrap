from flask import Flask, request, redirect
import twilio.twiml
import requests
import json
import csv
import datetime
import os
from twilio.rest import TwilioRestClient
from pprint import pprint

MYDIR = os.path.dirname(__file__)

# config_file = open('../config.json', 'r')
# config = json.load(config_file)

# ACCOUNT_SID = config['account_sid']
# AUTH_TOKEN = config['auth_token']

ACCOUNT_SID = os.getenv("ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


app = Flask(__name__)

with open(os.path.join(MYDIR, 'birthday_testing.csv'), 'rb') as f:
    reader = csv.reader(f)
    birthday_list = list(reader)
 
# @app.route("/sms", methods=['GET', 'POST'])
# def hello_monkey():
#     """Respond to incoming calls with a simple text message."""
 
#     resp = twilio.twiml.Response()
#     resp.message("Hello, Mobile Monkey")
#     return str(resp)

numbers = ['+16144775689']
@app.route('/messages', methods=['POST'])
def sms():
    """Respond to incoming calls with a simple text message."""
    print(request.values)
    from_number = request.values.get('From')
    message_response = request.values.get('Body')
    # if number in numbers:
    #     resp = twilio.twiml.Response()
    #     resp.message("Hi, Karthik")
    #     return str(resp)  
    # else:    
    #     resp = twilio.twiml.Response()
    #     resp.message("Hi, everyone")
    #     return str(resp) 
    
    for contact_detail in birthday_list:
        phone_number = contact_detail[4] 
        if from_number == phone_number:
            first_name = contact_detail[0]
            last_name = contact_detail[1]
            message_body = first_name + " " + last_name + " sent " + message_response
            client.messages.create(to="+15108473180", from_="+14158021733",
                                   body=message_body)
            
@app.route('/messages', methods=['GET'])
def send_birthdaywish():
    
    # message = client.messages.create(to="+16144775689", from_="+14158021733",
                                       # body="Hi, Karthik")
    
    
    
    print birthday_list
    today = datetime.date.today()
    print today
    birthday_wishes_sent = "Today's birthday list:\n"
    for contact_detail in birthday_list:
        birthday = contact_detail[2]
        date_object = datetime.datetime.strptime(birthday, "%m-%d-%Y")
        
        # Check if the month and day match the current month and day
        if date_object.month == today.month and date_object.day == today.day:
            birthday_message = contact_detail[3]
            phone_number = contact_detail[4]
            client.messages.create(to=phone_number, from_="+14158021733",
                                       body=birthday_message)
            print birthday_message
            birthday_wishes_sent = birthday_wishes_sent + contact_detail[0] + " " + contact_detail[1] + "\n"
    return birthday_wishes_sent
    
if __name__ == "__main__":
    port = os.getenv("PORT", 8080)
    app.run(debug=True, host='0.0.0.0', port=int(port))
