# -*- coding: utf-8 -*-


LOCATIONS = [
    {
        "text": {
            "type": "plain_text",
            "text": "Remote",
            "emoji": True
        },
        "value": "remote"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "US",
            "emoji": True
        },
        "value": "us"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Saratov",
            "emoji": True
        },
        "value": "saratov"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Saint Petersburg",
            "emoji": True
        },
        "value": "spb"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Kharkiv",
            "emoji": True
        },
        "value": "kharkiv"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Lviv",
            "emoji": True
        },
        "value": "lviv"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Kyiv",
            "emoji": True
        },
        "value": "kyiv"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Krakow",
            "emoji": True
        },
        "value": "krakow"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Belgrade",
            "emoji": True
        },
        "value": "belgrade"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "London",
            "emoji": True
        },
        "value": "london"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Chisinau",
            "emoji": True
        },
        "value": "chisinau"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Dnipro",
            "emoji": True
        },
        "value": "dnipro"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Guadalajara",
            "emoji": True
        },
        "value": "guadalajara"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Kazan",
            "emoji": True
        },
        "value": "kazan"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Moscow",
            "emoji": True
        },
        "value": "moscow"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Wroclaw",
            "emoji": True
        },
        "value": "wroclaw"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Gdansk",
            "emoji": True
        },
        "value": "gdansk"
    },
    {
        "text": {
            "type": "plain_text",
            "text": "Ljubljana",
            "emoji": True
        },
        "value": "ljubljana"
    }
]

EXTRA_GROUPS = [
    {
        "text": {
            "type": "plain_text",
            "text": "eng_data_analytics",
            "emoji": True
        },
        "value": "eng_data_analytics"
    }
]

DONUT = {
    "type": "image",
    "image_url": "https://files.slack.com/files-pri/T1H4XT8DV-F02FKRZ2QK0/1000x1000_color.png?pub_secret=43aa14cb10",
    "alt_text": "cute donut"
}

MEET_REMINDER = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "We've already had a meeting"
                },
                "style": "primary",
                "action_id": "flow_meet_was"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Still waiting for a meeting"
                },
                "style": "primary",
                "action_id": "flow_meet_was_not_yet"
            }
        ]
    }
]

MEET_FEEDBACK = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Yes"
                },
                "style": "primary",
                "action_id": "flow_meet_was"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "No"
                },
                "style": "danger",
                "action_id": "flow_meet_was_not"
            }
        ]
    }
]

MEET_NEXT = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Sure!"
                },
                "style": "primary",
                "action_id": "flow_next_week_yes"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "One-week pause"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1w"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "One-month pause"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1m"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Stop bot permanently"
                },
                "style": "danger",
                "action_id": "stop"
            }
        ]
    }
]

MEET_NEXT_AFTER_PAUSE = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Sure!"
                },
                "style": "primary",
                "action_id": "flow_next_week_yes"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Additional week of rest"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1w"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Additional month of rest"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1m"
            }
        ]
    }
]

MEET_WAS = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Awesome!"
                },
                "style": "primary",
                "action_id": "flow_meet_p3"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Good"
                },
                "action_id": "flow_meet_p2"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Normal"
                },
                "action_id": "flow_meet_p1"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Could be better"
                },
                "action_id": "flow_meet_n1"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Unsatisfactory"
                },
                "style": "danger",
                "action_id": "flow_meet_n2"
            }
        ]
    }
]

FLOW_PART_0 = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Join"
                },
                "style": "primary",
                "action_id": "flow_participate_1"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Help"
                },
                "action_id": "help"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Cancel"
                },
                "style": "danger",
                "action_id": "stop"
            }
        ]
    }
]

FLOW_STOP = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "One-week pause"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1w"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "One-month pause"
                },
                "style": "danger",
                "action_id": "flow_next_week_pause_1m"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Stop bot permanently"
                },
                "style": "danger",
                "action_id": "stop"
            }
        ]
    }
]
