import json
import boto3
import os
from uamtbot import UamtBot
import copy

from nacl.signing import VerifyKey

PUBLIC_KEY = os.environ['PUBLIC_KEY']

RESPONSE_TYPES = {
    "PONG": 1,
    "DEFERRED_UPDATE_MESSAGE": 6,
    "MESSAGE_WITH_SOURCE": 4,
    "DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE": 5,
    "UPDATE_MESSAGE": 7
}

REQUEST_RESPONSES = {
    1: {
        "response": {
            "type": RESPONSE_TYPES["PONG"]
        },
        "process": False,
        "name": "PING"
    },
    2: {
        "response": {
            "type": RESPONSE_TYPES['DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE'],
            "data": {
                "allowed_mentions": {
                    "parse": []
                }
            }
        },
        "process": True,
        "name": "APPLICATION_COMMAND"
    },
    3: {
        "response": {
            "type": RESPONSE_TYPES['DEFERRED_UPDATE_MESSAGE'],
            "data": {}
        },
        "process": False,
        "name": "MESSAGE_COMPONENT"
    }
}


def is_dummy_event(event):
    return 'dummy_event' in event


def verify_signature(event):
    try:
        raw_body = event.get("rawBody")
        auth_sig = event.get('signature')
        auth_ts = event.get('timestamp')

        message = auth_ts.encode() + raw_body.encode()
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(message, bytes.fromhex(auth_sig))
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")


def lambda_handler(event, context):
    # debug print
    print(f"event {event}")

    if is_dummy_event(event):
        return 'STILL WARM'

    verify_signature(event)

    # check type
    body = event.get('body-json')
    response = get_response(body)

    # check ephemeral
    check_ephemeral(body, response)

    # update buttons (disable on click if correct user)
    modify_interaction_response(body, response)

    # process in new lambda (cause timeout)
    run_processing(event, response)

    print(f"reponse {response['response']}")
    return response["response"]


def check_ephemeral(body, response):
    if response["process"]:
        if UamtBot().response_ephemeral(body):
            UamtBot.set_ephemeral(response['response']['data'])


def run_processing(event, response):
    if response["process"]:
        boto3.client('lambda').invoke(
            FunctionName=os.environ['PROCESSING_LAMBDA'],
            InvocationType='Event',
            Payload=json.dumps(event)
        )


def modify_interaction_response(body, response):
    if UamtBot.is_interaction(body):
        if UamtBot.is_interaction_user(body):
            response['response']['data']['components'] = UamtBot.disable_components(UamtBot.get_components(body))
            response['response']['type'] = RESPONSE_TYPES['UPDATE_MESSAGE']
            response['process'] = True


def get_response(body):
    if body.get("type") not in REQUEST_RESPONSES:
        raise Exception(f"[UNAUTHORIZED] Invalid request type: {body.get('type')}!")
    process = REQUEST_RESPONSES[body.get("type")]
    return copy.deepcopy(process)
