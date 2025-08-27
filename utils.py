#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 16:58:39 2025

@author: nima
"""

import json
import os

database = "database.json"
def load_database():
    if not os.path.exists(database):
        return {"user": []}
    with open(database, "r", encoding="utf-8") as o:
        return json.load(o)

def save_database(data):
    with open(database, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data_basee = "data_basee.json"
def load_data_basee():
    if not os.path.exists(data_basee):
        return {"course": []}
    with open(data_basee, "r", encoding="utf-8") as e:
        return json.load(e)

def save_dataibasee(dataa):
    with open(data_basee, "w", encoding="utf-8") as g:
        json.dump(dataa, g, ensure_ascii=False, indent=4)

data_thesis = "thesis.json"
def load_thesis():
    if not os.path.exists(data_thesis):
        return []
    with open(data_thesis, "r", encoding="utf-8") as n:
        return json.load(n)

def save_thesis(dat):
    with open(data_thesis, "w", encoding="utf-8") as m:
        json.dump(dat, m, indent=4)

def create_thesis_dir():
    if not os.path.exists("thesis_files"):
        os.makedirs("thesis_files")