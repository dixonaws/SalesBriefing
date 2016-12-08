from __future__ import print_function

import urllib2
import json
import time
import boto3

# AlexaCorpStats, v1.0

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest,  etc.)
    The JSON body of the request is provided in the event parameter.
    """

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.372ed24f-828d-4d1d-99e1-0718051ceca0"):
        raise ValueError("Invalid Application ID")

    #print("event[session][user][userId]=" + str(event['session']['user']['userId']))

    if event['session']['new']:
        print("Starting new session...")
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        print("Launch requested...")
        return on_launch(event['request'], event['session'])


    elif event['request']['type'] == "IntentRequest":
        print("Intent requested...")
        return on_intent(event['request'], event['session'])

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


# ------------------------- on_intent()

def on_intent(intent_request, session):
    # Called when the user specifies an intent for this skill

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    # intent_request is a Python dict object
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("*** on_intent: I received intent=" + str(intent));
    print("*** on_intent: I received intent_name=" + str(intent_name));

    # Dispatch to your skill's intent handlers
    if intent_name == "VerifyPIN":
        return verifyPIN(intent, session)
    elif intent_name == "MainMenu":
        return mainMenu(intent, session)
    elif intent_name == "GetAccount":
        return getAccount(intent, session)
    elif intent_name == "AccountCommand":
        return getAccountCommand(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# ------------------------- verifyPIN()

def verifyPIN(intent, session):
    # We hardcode the matching PIN for now
    intCorrectPIN = 9876

    print("*** verifyPIN: I received intent " + str(intent));

    # Grab the PIN out of the intent and cast it to an integer
    PIN = intent['slots']['PIN']['value']
    intReceivedPIN = int(PIN)

    print("*** verifyPIN: I received PIN " + str(PIN))

    card_title = "Welcome"

    # Compare the PIN we received with the correct PIN
    if (intReceivedPIN == intCorrectPIN):
        return mainMenu()

    elif (intReceivedPIN != intCorrectPIN):
        speech_output = "Hmmm. That PIN code doesn't match my records";

    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


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

    client = boto3.client('s3')
    walmartSales=1050930
    targetSales = 589102
    rubbermaiddotcomSales = 98231
    homedepotSales = 48261
    publixSales = 10987

    usEastSales=2987675
    usCentralSales=3435676
    usWestSales=3454652

    card_title = "Rubbermaid Sales Briefing"
    card_content="Retail sales for October 31, 2016:" + "\n"
    card_content+="1. Walmart: " + (str(walmartSales)).format('n') + "\n"
    card_content += "2. Target: " + str(targetSales) + "\n"
    card_content += "3. rubbermaid.com: " + str(rubbermaiddotcomSales) + "\n"
    card_content += "4. Home Depot: " + str(homedepotSales) + "\n"
    card_content += "5. Publix: " + str(publixSales) + "\n"
    card_content += "\n"
    card_content += "US East: " + str(usEastSales) + "\n"
    card_content += "US Central: " + str(usCentralSales) + "\n"
    card_content += "US West: " + str(usWestSales)

    speech_output = "<speak>"
    speech_output+= "<s>Here's your Rubbermaid sales briefing for today, Monday, October 31. <break time=\"1s\"/></s>"
    speech_output+="<s>Top three retail sales yesterday were: </s>"
    speech_output+="<s>Walmart: " + str(walmartSales) + " dollars.</s>"
    speech_output += "<s>Target: " + str(targetSales) + " dollars.</s>"
    speech_output += "<s>Rubbermaid.com: " + str(rubbermaiddotcomSales) + " dollars.</s>"
    speech_output+="</speak>"

    should_end_session = True

    reprompt_text=""

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


# ------------------------- handle_session_end_request()

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for being a Power Company customer." \
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

