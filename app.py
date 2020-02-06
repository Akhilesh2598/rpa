# app.py
from flask import Flask, request, jsonify
import os
import dialogflow
import pandas as pd
import psycopg2
import requests
from flask_cors import CORS
import json

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\AkhileshKumarSingh\\Documents\\DialogFlowChatBot\\uipathchatbot-igsqnq-9e0b8710dc64.json"

app = Flask(__name__)
CORS(app)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


# check DF server connection
@app.route('/api/v1/ask-nero', methods=['GET'])
def askNero():
    # Retrieve the name from url parameter
    query = request.args.get("query", None)
    firstname = request.args.get("firstname", None)
    lastname = request.args.get("lastname", None)
    return detect_intent_texts("uipathchatbot-igsqnq", "123", query, firstname, lastname, "en-US")

@app.route('/rpa_post', methods=['POST'])
def rpa_post():
    # Retrieve the name from url parameter
    data = request.json
    print(data)
    data_type = type (data)
    return (data)
    #return jsonify(data)
    #return rpa_api()

# check DF server connection
@app.route('/rpa', methods=['GET'])
def rpa():
    # Retrieve the name from url parameter
    query = request.args.get("query", None)
    return rpa_api()

# check DF server connection
@app.route('/df', methods=['GET'])
def df():
    # Retrieve the name from url parameter
    query = request.args.get("query", None)
    # rpa_api()
    return detect_intent_texts("uipathchatbot-igsqnq", "123", query, "Akhilesh", "Singh", "en-US")

def rpa_api():
    access_url = "https://platform.uipath.com/Akhilesh2/Akhilesh2/api/Account/Authenticate"

    access_payload = "{\r\n  \"tenancyName\": \"Akhilesh2\",\r\n  \"usernameOrEmailAddress\": \"akhilesh.tech17@gmail.com\",\r\n  \"password\": \"Education01\"\r\n}"
    access_headers = {
            'Content-Type': 'application/json'}

    access_response = requests.request("POST", access_url, headers=access_headers, data=access_payload)


    access_token = json.loads(access_response.text)['result']

    print(access_token)

    queue_url = "https://platform.uipath.com/Akhilesh2/Akhilesh2/odata/Queues/UiPathODataSvc.AddQueueItem"

    queue_payload = "{\r\n  \"itemData\": {\r\n    \"Name\": \"pendingTasks\",\r\n    \"Priority\": \"High\",\r\n    \"SpecificContent\": {\"Issue\": \"PaymentFailure\"},\r\n    \"DeferDate\": \"2020-02-05T12:17:52.650Z\",\r\n    \"DueDate\": \"2020-02-05T12:17:52.650Z\",\r\n    \"RiskSlaDate\": \"2020-02-05T12:17:52.650Z\",\r\n    \"Reference\": \"string\",\r\n    \"Progress\": \"string\"\r\n  }\r\n}"
    queue_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    queue_response = requests.request("POST", queue_url, headers=queue_headers, data=queue_payload)

    queue_id = json.loads(queue_response.text)['QueueDefinitionId']

    print(queue_id)

    return str(queue_id)

def detect_intent_texts(project_id, session_id, texts, firstname, lastname, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    res = decision.response_parser(response, firstname, lastname)

    # print('=' * 20)
    # # print('Query text: {}'.format(response.query_result.query_text))
    # print('Query text: {}'.format(response.query_result.query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(
    #     response.query_result.intent.display_name,
    #     response.query_result.intent_detection_confidence))
    # print('Fulfillment text: {}\n'.format(
    #     response.query_result.fulfillment_text))
    # print('Fulfillment query_result: {}\n'.format(
    #     response.query_result))
    print(json.dumps(response, indent=2))
    return res


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, port=5000)
