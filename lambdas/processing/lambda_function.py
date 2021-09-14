from uamtbot import UamtBot
import traceback


def lambda_handler(event, context):
    print(f"event {event}")  # debug print

    # get body
    body = event.get('body-json')
    type = body.get('type')
    options = body.get('data')
    user = body.get('member')
    token = body.get('token')
    try:
        if type == 2:
            UamtBot().handle_command(type, options, user, token)
        elif type == 3:
            UamtBot().handle_interaction(options, body.get('message'), user, token)
    except Exception:
        print(traceback.format_exc())
