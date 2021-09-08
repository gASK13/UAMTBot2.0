from uamtbot import UamtBot
import traceback


def lambda_handler(event, context):
    print(f"event {event}")  # debug print

    # get body
    body = event.get('body-json')
    command = body.get('data').get('name')
    options = body.get('data')
    user = body.get('member')
    token = body.get('token')
    try:
        UamtBot().handle_command(command, options, user, token)
    except Exception:
        print(traceback.format_exc())
