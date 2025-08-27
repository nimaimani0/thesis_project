#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 12:54:30 2025

@author: nima
"""

class thesis:
    def __init__(self,thesis_id,s_id,c_id,req_date,status="pending"):
        self.thesis_id=thesis_id
        self.s_id=s_id
        self.c_id=c_id
        self.req_date=req_date
        self.status=status
        
        
        self.approval_date=None
        self.defense_date=None
        self.title=None
        self.abstract=None
        self.keywords=None
        self.pdf_path=None
        self.firstpage_path=None
        self.lastpage_path=None
        self.examiner={}
        self.grades={}
        self.finalgrade=None
        self.finalresult=None
        self.session_number=None
