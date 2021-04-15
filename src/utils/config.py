# -*- coding: utf-8 -*-

import yaml


def load(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
