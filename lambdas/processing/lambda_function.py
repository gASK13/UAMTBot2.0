from uamtbot import UamtBot


def lambda_handler(event, context):
    print(f"event {event}")  # debug print

    # get body
    body = event.get('body-json')
    command = body.get('data').get('name')
    options = body.get('data').get('options')
    user = body.get('member')
    token = body.get('token')

    UamtBot().handle_command(command, options, user, token)
