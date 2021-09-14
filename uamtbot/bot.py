import traceback
import time
import os
import discord
from .poster.poster import Poster
from .dynastore.dynastore import DynaStore
from datetime import datetime


class UamtBot:
    def __init__(self):
        self.poster = Poster()

    def app_id(self):
        return os.environ['APP_ID'] if 'APP_ID' in os.environ else 'N/A'


    def handle_message(self, command, options):
        if command == 'Age':
            self.handle_age(options.get('resolved'))
        elif command == 'Length':
            self.handle_length(options.get('resolved'))
        elif command == 'notes':
            self.process_notes(options.get('options'))
        elif command == 'slap':
            self.post_response("Sorry, " + self.get_user(self.user) + ", can't slap **" + options.get('options')[0].get(
                'value') + "** yet. Ask <@412352063125717002> to fix this!")
            return
        elif command == 'post':
            if self.user.get('user').get('id') == '412352063125717002':
                self.post_response("Bots dispatched...")
                time.sleep(10)
                self.post_to_channel(options.get('options'))
                self.post_response("Bots have delivered their payload.")
            else:
                self.post_response("Sorry, Dave, I cannot do that.")
        elif command == 'sleep':
            dur = options.get('options')[0].get('value')
            if dur > 20 or dur < 0:
                self.post_response("Sorry. Can't sleep that long, maximum 20 seconds....")
                return
            for i in range(0, dur):
                self.post_response("Sleeping for " + str(i) + " seconds...")
                time.sleep(1)
            self.post_response("I'm done now, " + self.get_user(self.user) + ", are you happy?")
            return
        else:
            self.post_response("BORK BORK boooooork .... ")
            return

    def handle_command(self, type, options, user, token):
        try:
            self.user = user
            self.token = token
            self.handle_message(options.get('name'), options)

        except Exception:
            self.post_response("Something went wrong. I can feel it...")
            print(traceback.format_exc())
            raise

    def process_notes(self, options):
        self.store = DynaStore(tableName='notes')
        subcommand = options[0]['name']
        suboptions = options[0]['options'] if 'options' in options[0] else {}
        if subcommand == 'list':
            self.list_notes(suboptions)
        elif subcommand == 'add':
            self.add_note(suboptions)
        elif subcommand == 'remove':
            self.remove_note(suboptions)
        elif subcommand == 'clear':
            self.clear_notes()

    def add_note(self, options):
        note_text = options[0]['value']
        notes = self.store.get(key=self.user['user']['id'])
        if not notes:
            notes = {'notes': []}
        notes['notes'].append(note_text)
        self.store.store(key=self.user['user']['id'], value=notes)
        self.post_response("Note `" + note_text[:15] + "...` saved...")

    def remove_note(self, options):
        user_id = self.user['user']['id']
        notes = self.store.get(key=user_id)
        if len(options) != 1:
            self.post_response("Please use exactly one of `index` or `note text` as an option.")
            return
        if not notes:
            self.post_response("Nice try, but you got no notes...")
            return
        if options[0]['name'] == 'index':
            idx = int(options[0]['value']) - 1
            if (idx < 0) | (idx >= len(notes['notes'])):
                self.post_response("Sorry, you only have " + str(len(notes['notes'])) + " ideas")
                return
        elif options[0]['name'] == 'note':
            val = options[0]['value'].lower()
            idx = None
            for i in range(len(notes['notes'])):
                if val in notes['notes'][i].lower():
                    if idx:
                        self.post_response("You need to be more clear, there are multiple such notes")
                        return
                    idx = i
            if not idx:
                self.post_response("Sorry, no such note was found.")
                return
        removed = notes['notes'].pop(idx)
        self.store.store(key=user_id, value=notes)
        self.post_response('`' + removed + '` was not a good one anyway....')

    def clear_notes(self):
        self.post_action_response("Do you really want to clear all your notes?")

    def list_notes(self, options):
        if len(options) == 1:
            user_id = options[0]['value']
        else:
            user_id = self.user['user']['id']
        notes = self.store.get(key=user_id)
        notes = (notes['notes'] if 'notes' in notes else []) if notes else []
        if len(notes) == 0:
            if user_id == self.user['user']['id']:
                self.post_response("You have no notes. Did you forget already?")
            else:
                self.post_response("<@" + user_id + "> has no notes. Ask him to add some maybe?")
        else:
            if user_id == self.user['user']['id']:
                text = 'Your notes:\r\n'
            else:
                text = '<@' + user_id + ">'s notes:\r\n"
            for i in range(len(notes)):
                text += '#' + str(i + 1) + ' => `' + notes[i] + '`\r\n'
            self.post_response(text)

    def handle_length(self, resolved):
        for message in resolved['messages'].keys():
            msg = resolved['messages'][message]
            self.post_response_ephemereal("The message has " + str(len(msg['content'])) + "characters.")
            return
        self.post_response("..... I'm not sure what I am supposed to do?", True)

    def handle_age(self, resolved):
        for user_id in resolved['users'].keys():
            if 'members' in resolved:
                if user_id in resolved['members']:
                    join = datetime.fromisoformat(resolved['members'][user_id]['joined_at'])
                    delta = datetime.now(join.tzinfo) - join
                    self.post_response(
                        "<@" + user_id + "> has been a member of this server for " + str(delta.days) + " days.")
                    return
            self.post_response(resolved["users"][user_id]["username"] + " is no longer with us....")
            return
        self.post_response("..... I'm not sure what I am supposed to do?")

    def get_user(self, user):
        if user is not None:
            if user.get('nick') is not None:
                return user.get('nick')
            elif user.get('user') is not None:
                return user.get('user').get('username')
        return '?$#@'

    def post_response(self, content, msgid="@original"):
        # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
        self.poster.patch(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + self.token + "/messages/" + msgid,
            json={
                "content": content,
                "allowed_mentions": {
                    "parse": []
                }
            })

    def post_action_response(self, content):
        # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
        self.poster.patch(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + self.token + "/messages/@original",
            json={
                "content": content,
                "allowed_mentions": {
                    "parse": []
                },
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Delete",
                                "style": 4,
                                "custom_id": "delete",
                                "emoji": {
                                    "name": "rip",
                                    "id": "512360112820584448"
                                }
                            },
                            {
                                "type": 2,
                                "label": "I changed my mind",
                                "style": 2,
                                "custom_id": "keep"
                            }
                        ]

                    }
                ]
            })

    def post_response_ephemereal(self, content):
        # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
        self.poster.delete(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + self.token + "/messages/@original")
        self.poster.post(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + self.token + "",
            json={
                "content": content,
                "allowed_mentions": {
                    "parse": []
                },
                "flags": (1 << 6)
            })

    def post_to_channel(self, options):
        r = self.poster.post(
            url='https://discord.com/api/v8/channels/' + options[0].get('value') + '/messages',
            json={
                "content": options[1].get('value'),
                "allowed_mentions": {
                    "users": [options[2].get('value')]
                }
            })
        print(r)
        print(r.json())

    def handle_interaction(self, options, message):
        self.store = DynaStore(tableName='notes')
        user_id = self.user['user']['id']
        author_id = message.get('interaction').get('user').get('id')
        if author_id != user_id:
            self.post_response("Sorry, only <@" + author_id + "> can click on my buttons.")
            return
        custom_id = options.get('custom_id')
        if custom_id == 'delete':
            self.post_response("Deleted! Hope you did not make a mistake...")
            self.store.delete(key=user_id)
            self.post_response("XXX", msgid=message.get('id'))
        elif custom_id == 'keep':
            self.post_response("Ok, that's good decision.")
            self.post_response("XXX", msgid=message.get('id'))
        else:
            self.post_response("....huh?")
