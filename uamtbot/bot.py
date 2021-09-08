import traceback
import time
import os
import discord
from .poster.poster import Poster
from .dynastore.dynastore import DynaStore


class UamtBot:
    def __init__(self):
        self.poster = Poster()

    def app_id(self):
        return os.environ['APP_ID'] if 'APP_ID' in os.environ else 'N/A'

    def handle_command(self, command, options, user, token):
        try:
            self.user = user
            self.token = token
            if command == 'notes':
                self.process_notes(options)
            elif command == 'slap':
                self.post_response("Sorry, " + self.get_user(user) + ", can't slap **" + options[0].get(
                    'value') + "** yet. Ask <@412352063125717002> to fix this!")
                return
            elif command == 'post':
                if user.get('user').get('id') == '412352063125717002':
                    self.post_response("Bots dispatched...")
                    time.sleep(10)
                    self.post_to_channel(options)
                    self.post_response("Bots have delivered their payload.")
                else:
                    self.post_response("Sorry, Dave, I cannot do that.")
            elif command == 'sleep':
                dur = options[0].get('value')
                if dur > 20 or dur < 0:
                    self.post_response("Sorry. Can't sleep that long, maximum 20 seconds....")
                    return
                for i in range(0, dur):
                    self.post_response("Sleeping for " + str(i) + " seconds...")
                    time.sleep(1)
                self.post_response("I'm done now, " + self.get_user(user) + ", are you happy?")
                return
            else:
                self.post_response("BORK BORK boooooork .... ")
                return
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
        self.post_response("Not implemented yet. Sorry.")

    def list_notes(self, options):
        if len(options) == 1:
            user_id = options[0]['value']
        else:
            user_id = self.user['user']['id']
        notes = self.store.get(key=user_id)
        if not notes:
            if user_id == self.user['user']['id']:
                self.post_response("You have no notes. Did you forget already?")
            else:
                self.post_response("<@" + user_id + "> has no notes. Ask him to add some maybe?")
        else:
            if user_id == self.user['user']['id']:
                text = 'Your notes:\r\n'
            else:
                text = '<@' + user_id + ">'s notes:\r\n"
            for i in range(len(notes['notes'])):
                text += '#' + str(i + 1) + ' => `' + notes['notes'][i] + '`\r\n'
            self.post_response(text)

    def get_user(self, user):
        if user is not None:
            if user.get('nick') is not None:
                return user.get('nick')
            elif user.get('user') is not None:
                return user.get('user').get('username')
        return '?$#@'

    def post_response(self, content):
        # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
        self.poster.patch(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + self.token + "/messages/@original",
            json={
                "content": content,
                "allowed_mentions": {
                    "parse": []
                }
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
