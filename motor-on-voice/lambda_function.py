from flask import Flask, render_template, json
from flask_ask import Ask, statement, question, session
import json
import requests

app = Flask(__name__)
ask = Ask(app, '/')
motor_status = 0

def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)

# will run on invocation
@ask.launch
def launched():
   return question('Hello, How can I help you today')

# when something goes wrong
@ask.default_intent
def default_message():
    speech = "Oh-aw! I couldn't understand you. Please try again"
    return question(speech)

# start motor if not running
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

# stop motor if running
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

# return whether motor runnning or not
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

# start or stop motor as a confirmation
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

# don't start or stop motor now
@ask.intent('NoIntent')
def motor_do_nothing():
    response = render_template('motor_do_nothing')
    return statement(response)

# HTTP GET req for motor status
@app.route('/motor/status')
def get_data():
    global motor_status
    response = ''
    if(motor_status == 1):
        response = app.response_class(
            response="running",
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response="stopped",
            status=200,
            mimetype='application/json'
        )
    return response

if __name__ == '__main__':
    app.run(debug=True)
