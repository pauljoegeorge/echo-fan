from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json

app = Flask(__name__)
ask = Ask(app, '/')
motor_status = 0

def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)

@ask.launch
def launched():
   return question('Hello, How can I help you today')

@ask.default_intent
def default_message():
    speech = "Oh-aw! I couldn't understand you. Do you need any assistant?"
    retry_speech = "Please try again later. I couldn't rectify your issue"
    return statement(speech).reprompt(retry_speech)

@ask.intent('MotorOnIntent')
def start_motor():
    global motor_status
    response = ''
    if( motor_status == 1):
        response = render_template('motor_already_on')
    else:
        response = render_template('motor_on')
        motor_status = 1
    return statement(response)

@ask.intent('MotorOffIntent')
def stop_motor():
    global motor_status
    response = ''
    if(motor_status == 0):
        response = render_template('motor_already_off')
    else:
        response = render_template('motor_off')
        motor_status = 0
    return statement(response)

@ask.intent('MotorStatusIntent')
def status_motor():
    global motor_status
    response = ''
    if(motor_status == 1):
        response = render_template('motor_on_status')
        session.attributes['status'] = "stop"
    else:
        response = render_template('motor_off_status')
        session.attributes['status'] = "start"
    return question(response)

@ask.intent('YesIntent')
def restart_motor():
    global motor_status
    response = ''
    if(session.attributes['status'] == "start"):
        response = render_template('motor_on')
        motor_status = 1
    else:
        response = render_template('motor_off')
        motor_status = 0
    return statement(response)

@ask.intent('NoIntent')
def motor_do_nothing():
    response = render_template('motor_do_nothing')
    return statement(response)

if __name__ == '__main__':
    app.run(debug=True)