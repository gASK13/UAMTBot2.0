from uamtbot import UamtBot
import traceback


def lambda_handler(event, context):
    print(f"event {event}")  # debug print

    # get body
    body = event.get('body-json')
    try:
        UamtBot().handle(body)
    except Exception:
        print(traceback.format_exc())
