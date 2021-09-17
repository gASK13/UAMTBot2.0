import json
import boto3
import os

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
            "type": RESPONSE_TYPES['DEFERRED_UPDATE_MESSAGE']
        },
        "process": True,
        "name": "MESSAGE_COMPONENT"
    }
}


def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event.get('signature')
    auth_ts = event.get('timestamp')

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig))


def lambda_handler(event, context):
    print(f"event {event}")

    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    # check type
    body = event.get('body-json')
    if body.get("type") not in REQUEST_RESPONSES:
        raise Exception(f"[UNAUTHORIZED] Invalid request type: {body.get('type')}!")

    process = REQUEST_RESPONSES[body.get("type")]

    # process in new lambda (cause timeout)
    if process["process"]:
        boto3.client('lambda').invoke(
            FunctionName=os.environ['PROCESSING_LAMBDA'],
            InvocationType='Event',
            Payload=json.dumps(event)
        )

    return process["response"]
