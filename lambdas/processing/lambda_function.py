from uamtbot import UamtBot


def lambda_handler(event, context):
    print(f"event {event}")  # debug print

    # get body
    body = event.get('body-json')
    command = body.get('data').get('name')
    options = body.get('data').get('options')
    user = body.get('member')
    token = body.get('token')
    try:
        UamtBot().handle_command(command, options, user, token)
    except Exception as inst:
        pass  # this got logged above, so we just need make sure we return correctly
