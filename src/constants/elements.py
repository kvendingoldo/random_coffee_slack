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
    }
]

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
                "action_id": "flow_meet_had"
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
