# -*- coding: utf-8 -*-

def get_groups(locations, groups):
    result = []

    for location in locations:
        result.append(
            {
                "name": location["name"],
                "displayName": location["displayName"],
                "enabled": location["enabledAsGroup"]
            }
        )

    for group in groups:
        result.append(
            {
                "name": group["name"],
                "displayName": group["displayName"],
                "enabled": group["enabled"]
            }
        )

    return result


def generate_groups(locations, groups):
    result = []

    for group in get_groups(locations, groups):
        result.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": group["displayName"],
                    "emoji": True
                },
                "value": group["name"]
            }
        )

    return result


def check_group_enabled(group, groups):
    for g in groups:
        if group == g["name"]:
            if g["enabled"]:
                return True
    return False
