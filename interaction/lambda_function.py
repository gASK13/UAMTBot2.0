import json
import boto3
import os

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = os.environ['PUBLIC_KEY']
PING_PONG = {"type": 1}
RESPONSE_TYPES =  {
                    "PONG": 1,
                    "DEFERRED_UPDATE_MESSAGE": 6,
                    "MESSAGE_WITH_SOURCE": 4,
                    "DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE": 5,
                    "UPDATE_MESSAGE": 7
                  }


def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event.get('signature')
    auth_ts  = event.get('timestamp')

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

def ping_pong(body):
    if body.get("type") == 1:
        return True
    return False


def lambda_handler(event, context):
    print(f"event {event}") # debug print
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")


    # check if message is a ping
    body = event.get('body-json')
    if ping_pong(body):
        return PING_PONG

    client = boto3.client('lambda')

    client.invoke(
        FunctionName = os.environ['PROCESSING_LAMBDA'],
        InvocationType = 'Event',
        Payload = json.dumps(event)
    )

    return {
        "type": RESPONSE_TYPES['DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE'],
        "data": {
            "content": "Will the real UAMTBOT please stand up, please stand up, please stand up.... "
        }
    }
