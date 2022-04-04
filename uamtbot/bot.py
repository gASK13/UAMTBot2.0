from uamtbot.utils import Poster, DynaStore
from uamtbot.commands import *


def register_commands(cls=command.Command, command_map={1: {}, 2: {}, 3: {}}):
    for cmd in cls.__subclasses__():
        register_commands(cmd, command_map)
        if cmd.name() is not None:
            command_map[cmd.type()][cmd.name().lower()] = cmd
    return command_map


class UamtBot:
    def __init__(self):
        # init all commands
        self.command_map = register_commands()

    def response_ephemeral(self, body):
        # do a quick check - is ephemeral or not?
        cmd = self.get_command_handler_class(body)
        if cmd is not None:
            return cmd.ephemeral()
        return True

    def get_command_handler_class(self, body):
        cmd_name = self.get_command_name(body)
        cmd_type = self.get_command_type(body)
        if cmd_name in self.command_map[cmd_type]:
            return self.command_map[cmd_type][cmd_name]
        return None

    @staticmethod
    def get_command_name(body):
        return body['data']['name'].lower()

    @staticmethod
    def get_command_type(body):
        return body['data']['type'] if 'type' in body['data'] else 1

    def handle(self, body):
        type = body.get('type')
        options = body.get('data')
        user = body.get('member')
        token = body.get('token')
        if type == 2:
            cmd = self.get_command_handler_class(body)
            if cmd is not None:
                Poster.patch_message(token, cmd.handle(body))
            else:
                msg = 'Sorry, no handler for this command.'

            # to be removed
            if options.get('name').lower() == 'notes':
                Poster.patch_message(token, {
                    "content": msg,
                    "allowed_mentions": {
                        "parse": []
                    },
                    "components": [{
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
            else:
                Poster.patch_message(token, {
                    "content": msg,
                    "allowed_mentions": {
                        "parse": []
                    }
                })
        elif type == 3:
            Poster.post_message(token, UamtBot.set_ephemeral({
                "content": "Got your interaction. Wink wink.",
                "allowed_mentions": {
                    "parse": []
                }
            }))

        # do type switch - message VS interaction
        # find handler
        # HANDLE (including param parsing / checking)
        # have some SERVICES (user service etc?)
        pass

    @staticmethod
    def set_ephemeral(response):
        response["flags"] = (1 << 6)
        return response

    @staticmethod
    def is_interaction(body):
        return body['type'] == 3

    @staticmethod
    def is_interaction_user(body):
        user_id = body['member']['user']['id']
        author_id = body['message']['interaction']['user']['id']
        return author_id == user_id

    @staticmethod
    def get_components(body):
        return body['message']['components']

    @staticmethod
    def disable_components(components):
        for c in components:
            if c['type'] == 1:
                UamtBot.disable_components(c['components'])
            else:
                c['disabled'] = True
        return components

#
# class OldBot:
#     def handle_message(self, command, options):
#         if command == 'Age':
#             self.handle_age(options.get('resolved'))
#         elif command == 'Length':
#             self.handle_length(options.get('resolved'))
#         elif command == 'notes':
#             self.process_notes(options.get('options'), options.get('resolved'))
#         elif command == 'slap':
#             time.sleep(5)
#             self.post_response("Sorry, " + self.get_user(self.user) + ", can't slap **" + options.get('options')[0].get(
#                 'value') + "** yet. Ask <@412352063125717002> to fix this!")
#             return
#         elif command == 'post':
#             if self.user.get('user').get('id') == '412352063125717002':
#                 self.post_response("Bots dispatched...")
#                 time.sleep(10)
#                 self.post_response("Bots have delivered their payload.")
#             else:
#                 self.post_response("Sorry, Dave, I cannot do that.")
#         elif command == 'sleep':
#             dur = options.get('options')[0].get('value')
#             if dur > 20 or dur < 0:
#                 self.post_response("Sorry. Can't sleep that long, maximum 20 seconds....")
#                 return
#             for i in range(0, dur):
#                 self.post_response("Sleeping for " + str(i) + " seconds...")
#                 time.sleep(1)
#             self.post_response("I'm done now, " + self.get_user(self.user) + ", are you happy?")
#             return
#         else:
#             self.post_response("BORK BORK boooooork .... ")
#             return
#
#     def handle_command(self, type, options, user, token):
#         try:
#             self.user = user
#             self.token = token
#             self.handle_message(options.get('name'), options)
#
#         except Exception:
#             self.post_response("Something went wrong. I can feel it...")
#             print(traceback.format_exc())
#             raise
#
#     def process_notes(self, options, resolved):
#         self.store = DynaStore(table_name='notes')
#         subcommand = options[0]['name']
#         suboptions = options[0]['options'] if 'options' in options[0] else {}
#         if subcommand == 'list':
#             self.list_notes(suboptions, resolved)
#         elif subcommand == 'add':
#             self.add_note(suboptions)
#         elif subcommand == 'remove':
#             self.remove_note(suboptions)
#         elif subcommand == 'clear':
#             self.clear_notes()
#
#     def add_note(self, options):
#         note_text = options[0]['value']
#         notes = self.store.get(key=self.user['user']['id'])
#         if not notes:
#             notes = {'notes': []}
#         notes['notes'].append(note_text)
#         self.store.store(key=self.user['user']['id'], value=notes)
#         self.post_response("Note `" + note_text[:15] + "...` saved...")
#
#     def remove_note(self, options):
#         user_id = self.user['user']['id']
#         notes = self.store.get(key=user_id)
#         if len(options) != 1:
#             self.post_response("Please use exactly one of `index` or `note text` as an option.")
#             return
#         if not notes:
#             self.post_response("Nice try, but you got no notes...")
#             return
#         if options[0]['name'] == 'index':
#             idx = int(options[0]['value']) - 1
#             if (idx < 0) | (idx >= len(notes['notes'])):
#                 self.post_response("Sorry, you only have " + str(len(notes['notes'])) + " ideas")
#                 return
#         elif options[0]['name'] == 'note':
#             val = options[0]['value'].lower()
#             idx = None
#             for i in range(len(notes['notes'])):
#                 if val in notes['notes'][i].lower():
#                     if idx:
#                         self.post_response("You need to be more clear, there are multiple such notes")
#                         return
#                     idx = i
#             if not idx:
#                 self.post_response("Sorry, no such note was found.")
#                 return
#         removed = notes['notes'].pop(idx)
#         self.store.store(key=user_id, value=notes)
#         self.post_response('`' + removed + '` was not a good one anyway....')
#
#     def clear_notes(self):
#         components = [
#             {
#                 "type": 1,
#                 "components": [
#                     {
#                         "type": 2,
#                         "label": "Delete",
#                         "style": 4,
#                         "custom_id": "delete",
#                         "emoji": {
#                             "name": "rip",
#                             "id": "512360112820584448"
#                         }
#                     },
#                     {
#                         "type": 2,
#                         "label": "I changed my mind",
#                         "style": 2,
#                         "custom_id": "keep"
#                     }
#                 ]
#
#             }
#         ]
#         self.post_response("Do you really want to clear all your notes?", components=components)
#
#     def list_notes(self, options, resolved):
#         if len(options) == 1:
#             user_id = options[0]['value']
#             user_name = resolved["members"][user_id]['nick'] if resolved["members"][user_id]['nick'] is not None else resolved["users"][user_id]['username']
#             user_avatar = resolved["users"][user_id]['avatar']
#         else:
#             user_id = self.user['user']['id']
#             user_name = self.get_user(self.user)
#             user_avatar = self.user['user']['avatar']
#         notes = self.store.get(key=user_id)
#         notes = (notes['notes'] if 'notes' in notes else []) if notes else []
#         if len(notes) == 0:
#             if user_id == self.user['user']['id']:
#                 self.post_response("You have no notes. Did you forget already?")
#             else:
#                 self.post_response("<@" + user_id + "> has no notes. Ask him to add some maybe?")
#         else:
#             embed = discord.Embed(title=user_name + "'s notes:", color=0x00ff00)
#             embed.set_author(name=user_name,icon_url='https://cdn.discordapp.com/avatars/' + str(user_id) + '/' + user_avatar + '.png?size=64')
#             for i in range(len(notes)):
#                 embed.add_field(name="#" + str(i+1), value=notes[i], inline=False)
#             self.post_response(embeds=[embed.to_dict()])
#
#     def handle_length(self, resolved):
#         for message in resolved['messages'].keys():
#             msg = resolved['messages'][message]
#             self.post_response_ephemereal("The message has " + str(len(msg['content'])) + "characters.")
#             return
#         self.post_response("..... I'm not sure what I am supposed to do?", True)
#
#     def handle_age(self, resolved):
#         for user_id in resolved['users'].keys():
#             if 'members' in resolved:
#                 if user_id in resolved['members']:
#                     join = datetime.fromisoformat(resolved['members'][user_id]['joined_at'])
#                     delta = datetime.now(join.tzinfo) - join
#                     self.post_response(
#                         "<@" + user_id + "> has been a member of this server for " + str(delta.days) + " days.")
#                     return
#             self.post_response(resolved["users"][user_id]["username"] + " is no longer with us....")
#             return
#         self.post_response("..... I'm not sure what I am supposed to do?")
#
#     def get_user(self, user):
#         if user is not None:
#             if user.get('nick') is not None:
#                 return user.get('nick')
#             elif user.get('user') is not None:
#                 return user.get('user').get('username')
#         return '?$#@'
#
#     def post_response(self, content=None, msgid="@original", components=None, embeds=None):
#         # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
#         json = {}
#         if content:
#             json["content"] = content
#             json["allowed_mentions"] = {"parse": []}
#         if components:
#             json['components'] = components
#         if embeds:
#             json['embeds'] = embeds
#         Poster.patch_message(self.token, json, message_id=msgid)
#
#     def handle_interaction(self, options, message, user, token):
#         try:
#             self.user = user
#             self.token = token
#             self.handle_interaction_inner(options, message)
#
#         except Exception:
#             self.post_response("Something went wrong. I can feel it...")
#             print(traceback.format_exc())
#             raise
#
#     def disable_components(self, components):
#         for c in components:
#             if c['type'] == 1:
#                 self.disable_components(c['components'])
#             else:
#                 c['disabled'] = True
#         return components
#
#     def handle_interaction_inner(self, options, message):
#         self.store = DynaStore(table_name='notes')
#         user_id = self.user['user']['id']
#         author_id = message.get('interaction').get('user').get('id')
#         if author_id != user_id:
#             return
#         custom_id = options.get('custom_id')
#         if custom_id == 'delete':
#             self.store.delete(key=user_id)
#             self.post_response(msgid=message.get('id'),
#                                components=self.disable_components(message['components']))
#         elif custom_id == 'keep':
#             self.post_response(msgid=message.get('id'),
#                                components=self.disable_components(message['components']))
