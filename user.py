#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 17:46:32 2025

@author: nima
"""

class user:
    def __init__(self, id, name, person, major, password,thesis_request=None):
        self.id = id
        self.name = name
        self.person = person
        self.major = major
        self.password = password
        self.thesis_request=thesis_request