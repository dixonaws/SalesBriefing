from __future__ import print_function

import time
import boto3

# SalesBriefing, v1.0

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest,  etc.)
    The JSON body of the request is provided in the event parameter.
    """

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    #Uncomment this if statement and populate with your skill's application ID to
    #prevent someone else from configuring a skill that sends requests to this
    #function.

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.372ed24f-828d-4d1d-99e1-0718051ceca0"):
        raise ValueError("Invalid Application ID")

    # print("event[session][user][userId]=" + str(event['session']['user']['userId']))

    if event['session']['new']:
        print("Starting new session...")
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        print("Launch requested...")
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        print("SessionEnd requested...")
        return on_session_ended(event['request'], event['session'])


# ------------------------- on_session_started()

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    # print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


# ------------------------- on_launch()

def on_launch(launch_request, session):
    # Called when the user launches the skill without specifying what they want

    # print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])

    # Dispatch to your skill's launch

    return get_welcome_response()


def on_session_ended(session_ended_request, session):
    # Called when the user ends the session.

    # Is not called when the skill returns should_end_session=true

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    # If we wanted to initialize the session to have some attributes we could add those here

    print("*** in get_welcome_response()")

    session_attributes = {}

    # instantiate an S3 client named 's3'
    bucket = "salesbriefing-data"
    walmart_salesFigures_key = "walmart_salesFigures.txt"
    message_key = "message.txt"
    s3 = boto3.resource('s3')

    # read a string amount from a file called 'key' in S3 'bucket'
    obj = s3.Object(bucket, walmart_salesFigures_key)
    sales = obj.get()['Body'].read().decode('utf-8')

    obj = s3.Object(bucket, message_key)
    message = obj.get()['Body'].read().decode('utf-8')

    walmartSales = sales
    targetSales = 590000
    rubbermaiddotcomSales = 98000
    homedepotSales = 48000
    publixSales = 10000

    usEastSales = 2987675
    usCentralSales = 3435676
    usWestSales = 3454652

    card_title = "AcmeCo Sales Briefing"
    card_content = "Retail sales for December 7, 2016:" + "\n"
    card_content += "1. Walmart: " + (str(walmartSales)).format('n') + "\n"
    card_content += "2. Target: " + str(targetSales) + "\n"
    card_content += "3. acmeco.com: " + str(rubbermaiddotcomSales) + "\n"
    card_content += "4. Home Depot: " + str(homedepotSales) + "\n"
    card_content += "5. Publix: " + str(publixSales) + "\n"
    card_content += "\n"
    card_content += "US East: " + str(usEastSales) + "\n"
    card_content += "US Central: " + str(usCentralSales) + "\n"
    card_content += "US West: " + str(usWestSales)

    # results in "Thursday, December 8" or whatever today is
    strToday = time.strftime("%a") + ", " + time.strftime("%B") + " " + time.strftime("%d")

    speech_output = "<speak>"
    speech_output += "<s>Here's your Ack mee Co sales briefing for today, " + strToday + ".<break time=\"1s\"/></s>"
    speech_output += "<s>Top three retail sales yesterday: </s>"
    speech_output += "<s>Walmart: " + str(walmartSales) + " dollars.</s>"
    speech_output += "<s>Target: " + str(targetSales) + " dollars.</s>"
    speech_output += "<s>ack mee co.com: " + str(rubbermaiddotcomSales) + " dollars.</s>"
    speech_output += "<s>" + message + "</s>"
    speech_output += "</speak>"

    should_end_session = True

    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


# ------------------------- handle_session_end_request()

def handle_session_end_request():
    card_title = "Session Ended"
    card_content = "Session Ended"
    speech_output = "Thank you for being an Acme Co customer." \
                    "Have a nice day! "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, card_content, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(card_title, card_content, output, reprompt_text, should_end_session):
    return {
        #        'outputSpeech': {
        #            'type': 'PlainText',
        #            'text': output
        #        },
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
