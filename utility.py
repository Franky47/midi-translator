# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------

class Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
