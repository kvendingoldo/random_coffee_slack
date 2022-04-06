# -*- coding: utf-8 -*-

def get_groups(locations, groups):
    result = []

    for location in locations:
        result.append(
            {
                "name": location,
                "displayName": locations[location]["displayName"],
                "enabled": locations[location]["enabledAsGroup"],
                "additionalUsers": locations[location]["additionalUsers"],
                "admins": locations[location]["admins"]
            }
        )

    for group in groups:
        result.append(
            {
                "name": group,
                "displayName": groups[group]["displayName"],
                "enabled": groups[group]["enabled"],
                "additionalUsers": groups[group]["additionalUsers"],
                "admins": groups[group]["admins"]
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


def check_group_exist(groups, group):
    for g in groups:
        if group == g["name"]:
            return True
    return False


def get_group_additional_users(group, groups):
    for g in groups:
        if group == g["name"]:
            return g["additionalUsers"]
    return []


def is_uid_admin_for_group(groups, group, uid):
    for g in groups:
        if g["name"] == group:
            for admin in g["admins"]:
                if admin == uid:
                    return True

    return False
