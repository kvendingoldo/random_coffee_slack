# -*- coding: utf-8 -*-

USER_NOT_FOUND = "Your ID is not found in the RCB system. " \
                 "Looks like you didn't register via /rcb start command OR executed /rcb quit command"

COMMAND_NOT_FOUND = "Command not found. Use '/rcb help' command to get help"

FLOW_HELP = "Available commands:\n" \
            "/rcb start - participate in Random Coffee meets\n" \
            "/rcb status - get my current status\n" \
            "/rcb stop  - stop participating in Random Coffee\n" \
            "/rcb quit  - quit Random Coffee meets\n" \
            "/rcb change_meet_location - allows to change meeting location; 'worldwide' by default\n" \
            "/rcb help  - help\n"

FLOW_STATUS = "Your current status: {0} weeks of pause; It means that you'll get your pair {1} \n" \
              "Your current meeting location is '{2}'"

FLOW_QUIT = "Sorry about your choice. Hope to see you again soon. " \
            "Just write /rcb start again in this case. Information about your profile was deleted."

FLOW_STOP = "Please, choose a period to stop participating"

ACTION_STOP = "I'm looking forward to seeing you when you come back"

FLOW_PARTNER_LEFT = "It looks like your partner decided to take a break; " \
                    "Don't worry, I'll find a new one and send you an additional notification when ready."

FLOW_PARTICIPATE_0 = "Hi there!👋\n\n" \
                     "I'm a Random Coffee bot here to help you create real connections with GD people worldwide. " \
                     "Weekly I'll randomly pick one exciting person for you to have a meeting with. " \
                     "You both will receive each other's names; " \
                     "slack them, agree on a date and choose a platform to meet: zoom, skype, meet, etc. \n\n" \
                     "So are you up for? \n\n" \
                     "Enter Join to continue."

FLOW_PARTICIPATE_1 = "Tell me a little bit about yourself! \n\n" \
                     "What is your location?"

FLOW_PARTICIPATE_2 = "Wow! Now you’re a Random coffee participant! \n\n" \
                     "What’s next? \n\n" \
                     "1. Every Monday you’ll receive the name of your next coffee partner \n" \
                     "2. Slack them, agree on a date and choose a platform to meet: " \
                     "zoom, skype, meet or even office in your location? \n" \
                     "3. Be interested and punctual. No one wants their coffee break to be ruined."

FLOW_WEEK_YES = "Great! Next Monday I’ll choose one more amazing coffee partner for you!"
FLOW_WEEK_PAUSE_1W = "I see. Let's do this again next week!"
FLOW_WEEK_PAUSE_1M = "I see. I will get back to you in a month!"

FLOW_MEET_WAS = ":eyes: How did it go with <@{0}>?"
FLOW_MEET_WAS_NOT_YET = ":clock1: Hurry up, the week will be over soon"
FLOW_MEET_RATE = "Thank you for your response!"

FLOW_CHANGE_MEET_LOCATION = "Choose a location where you want to have a meeting"

MEET_INFO = "Hey!👋 \n\n" \
            "Your Random Coffee partner is <@{0}>! Lucky you :) \n\n" \
            "Slack them now to set up a meeting."

MEET_LOOKING = "Hey!👋 \n\n" \
               "I'm still looking for a partner for you. \n\n" \
               "You'll be notified immediately when a partner is found."

MEET_INFO_NOT_UNIQUE = "Hey!👋 \n\n" \
                       "You are lucky, this week you have another partner, who is <@{0}>! \n\n" \
                       "Slack them now to set up a meeting."

MEET_REMINDER = "✉️ How are things?\n\n" \
                "Mid-week is the best day to set up a meeting with your coffee partner (<@{0}>)!\n\n" \
                "Slack them now to set up a meeting."

MEET_FEEDBACK = "The week is over! \n\n" \
                "Did you get a chance to meet up with <@{0}> for a coffee break?"

MEET_NEXT = "New week – new opportunities!\n\n" \
            "Are you taking part in Random Coffee meetings next week?"

MEET_NEXT_AFTER_PAUSE = "Hey! Your break is finishing this week! :hourglass: \n\n" \
                        "Are you taking part in Random Coffee meetings next week?"
