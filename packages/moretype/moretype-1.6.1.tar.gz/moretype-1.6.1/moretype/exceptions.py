# coding: utf-8
# by Jules
# Time: 2025/1/31 13:54:40

class LinkInfo(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


class RectNotSupport(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message

class KeyValueNotFound(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message