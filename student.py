#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 16:11:36 2025

@author: nima
"""
import json
from user import user
from utils import load_database , save_database ,load_data_basee ,save_dataibasee ,save_thesis,load_thesis
from datetime import datetime, timedelta
import os
import shutil

class student(user):
    def __init__(self,id,name,person,major,password,thesis_request=None):
        super().__init__(id,name,"student",major,password,thesis_request)
    
    def change_password(self, data):
        new_pass = input("please enter a new password ")
        data = load_database()
        
        for i in data["user"]:
            if i["id"] == self.id:
                i["password"] = new_pass
                self.password = new_pass
                break
        save_database(data)
        print("successfully changed!")
    
    
    
    def req_thesis(self, data):
        dataa = load_data_basee()
        data = load_database()
        req = load_thesis()
        
        thesis_ids = [f["thesis_id"] for f in req]
        a = max(thesis_ids) + 1 if thesis_ids else 1

   
        for m in req:
            if m["student_id"] == self.id:
                if m["status"] in ["pending", "approve", "pass"]:
                    print("you send request before!!!")
                    return
 
        for q in data["user"]:
            if q["id"]==self.id:
                major=str(q["major"])
           
        
        course_by_major = {
            "Computer Engineering": [
                "Natural Language Processing", "Computer Vision", "Cybersecurity", "Algorithms"
            ],
            "Mechanical Engineering": [
                "Rigid Body Kinematics", "Machine Dynamics", "Strength of Materials", "Fluid Mechanics"
            ],
            "Electrical Engineering": [
                "Power Systems", "Electromagnetics", "Math2", "Physics2"
            ]
        }
        
        if major in course_by_major:
            allowed_courses = course_by_major[major]
        else:
            print("Your major is not defined or has no allowed thesis courses!")
            return

       
        for idx, title in enumerate(allowed_courses, 1):
            print(f"{idx}. {title}")

        inpt = input("choose your thesis title: ")

        if inpt.isdigit() and 1 <= int(inpt) <= len(allowed_courses):
            selected_title = allowed_courses[int(inpt)-1]
            
           
            for i in dataa["course"]:
                if i["title"] == selected_title and i["capacity"] > 0:
                    p_id = i["professor_id"]
                    for n in data["user"]:
                        if n["id"] == p_id:
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            new_req = {
                                "thesis_id": a,
                                "student_id": self.id,
                                "professor_id": p_id,
                                "title": selected_title,
                                "status": "pending",
                                "date": current_time,
                                "approval_date": "",
                                "defense_date": "",
                                "abstract": "",
                                "keywords": "",
                                "pdf_path": "",
                                "firstpage_path": "",
                                "lastpage_path": "",
                                "finalgrade": "",
                                "finalresult": "",
                                "defense_requested": 0,
                                "defense_approved": 0,
                                "defense_date_proposed": "",
                                "session_number":3,
                                "reviewers": []
                            }
                            req.append(new_req)
                            save_thesis(req)
                            print(f"request send to {n['name']}")
                            return
            print("course not available")
        else:
            print("invalid input!")
        
    
    
    
    def show_status(self, data):
        req = load_thesis()
        for n in req:
            if n["student_id"] == self.id:
                print(f"your thesis status is {n['status']}")
                if n["status"] == "approve":
                    if n["approval_date"]:
                        approval_date = datetime.strptime(n["approval_date"], "%Y-%m-%d %H:%M:%S")
                        if (datetime.now() - approval_date) >= timedelta(days=90):
                            print("you can request defense now!")
                        else:
                            remaining = 90 - (datetime.now() - approval_date).days
                            print(f"wait {remaining} days for defense request")
                    
                    if n["reviewers"]:
                        print("reviewers assigned:")
                        dataa = load_database()
                        for rev in n["reviewers"]:
                            for user in dataa["user"]:
                                if user["id"] == rev["id"]:
                                    print(f"  - {user['name']} ({rev['type']})")
                                    break
                return
        print("no thesis found!")
    
    def request_defense(self, data):
        req = load_thesis()
        for n in req:
            if n["student_id"] == self.id and n["status"] == "approve":
                if n["approval_date"]:
                    approval_date = datetime.strptime(n["approval_date"], "%Y-%m-%d %H:%M:%S")
                    if (datetime.now() - approval_date) >= timedelta(days=90):
                        if n["defense_requested"] == 0:
                            abstract = input("enter abstract: ")
                            keywords = input("enter keywords (comma separated): ")

                            
                            pdf_path = input("enter pdf file path: ")
                            if os.path.exists(pdf_path) and pdf_path.lower().endswith(".pdf"):
                                pdf_name = os.path.basename(pdf_path)
                                if any(x.get("pdf_path") and os.path.basename(x["pdf_path"]) == pdf_name for x in req):
                                    print("this PDF filename already exists, choose another name!")
                                    return
                                pdf_dir = "/home/nima/Documents/pro/student/pdf"
                                os.makedirs(pdf_dir, exist_ok=True)
                                final_pdf = os.path.join(pdf_dir, pdf_name)
                                shutil.copy(pdf_path, final_pdf)
                                n["pdf_path"] = final_pdf
                            else:
                                print("invalid PDF format! must be .pdf")
                                return

                            
                            firstpage = input("enter first page image path: ")
                            if os.path.exists(firstpage) and firstpage.lower().endswith(".jpg"):
                                first_name = os.path.basename(firstpage)
                                if any(x.get("firstpage_path") and os.path.basename(x["firstpage_path"]) == first_name for x in req):
                                    print("this firstpage image filename already exists, choose another name!")
                                    return
                                img_dir = "/home/nima/Documents/pro/student/image"
                                os.makedirs(img_dir, exist_ok=True)
                                final_first = os.path.join(img_dir, first_name)
                                shutil.copy(firstpage, final_first)
                                n["firstpage_path"] = final_first
                            else:
                                print("invalid first page format! must be .jpg")
                                return
                           
                            lastpage = input("enter last page image path: ")
                            if os.path.exists(lastpage) and lastpage.lower().endswith(".jpg"):
                                last_name = os.path.basename(lastpage)
                                if any(x.get("lastpage_path") and os.path.basename(x["lastpage_path"]) == last_name for x in req):
                                    print("this lastpage image filename already exists, choose another name!")
                                    return
                                img_dir = "/home/nima/Documents/pro/student/image"
                                os.makedirs(img_dir, exist_ok=True)
                                final_last = os.path.join(img_dir, last_name)
                                shutil.copy(lastpage, final_last)
                                n["lastpage_path"] = final_last
                            else:
                                print("invalid last page format! must be .jpg")
                                return

                            
                            n["abstract"] = abstract
                            n["keywords"] = keywords
                            n["defense_requested"] = 1
                            n["defense_date_proposed"] = input("propose defense date (2025-10-10): ")

                            save_thesis(req)
                            print("defense request submitted!")
                            return
                        else:
                            print("defense already requested!")
                            return
                    else:
                        remaining = 90 - (datetime.now() - approval_date).days
                        print(f"wait {remaining} more days for defense request")
                        return
        print("no approved thesis found!")
    
    def search_archive(self, data):
        req = load_thesis()
        keyword = input("enter search keyword: ")

        found = []
        db = load_database()      
        for n in req:
            if n["status"] in ["pass", "fail"]:
                match = False
                if keyword in n.get("title", "").lower():
                    match = True
                elif keyword in n.get("keywords", "").lower():
                    match = True
                else:
                    for stu in db["user"]:
                        if stu["id"] == n["student_id"]:
                            if keyword in stu["name"].lower():
                                match = True
                            break
                if not match and "professor_id" in n:
                    for prof in db["user"]:
                        if prof["id"] == n["professor_id"]:
                            if keyword in prof["name"].lower():
                                match = True
                            break
                if not match and "defense_date_proposed" in n:
                    year = n["defense_date_proposed"].split("-")[0]
                    if keyword in year:
                        match = True
                if not match and "reviewers" in n:
                    for rev in n["reviewers"]:
                        for user in db["user"]:
                            if user["id"] == rev["id"] and keyword in user["name"].lower():
                                match = True
                                break
                if match:
                    found.append(n)
        if found:
            for f in found:
                student_name = ""
                for stu in db["user"]:
                    if stu["id"] == f["student_id"]:
                        student_name = stu["name"]
                        break
                professor_name = ""
                if "professor_id" in f:
                    for prof in db["user"]:
                        if prof["id"] == f["professor_id"]:
                            professor_name = prof["name"]
                            break

                print(f"Title: {f.get('title','')}")
                print(f"Student: {student_name}")
                print(f"Professor: {professor_name}")
                print(f"Abstract: {f.get('abstract','')[:100]}...")
                print(f"Keywords: {f.get('keywords','')}")
                print(f"Grade: {f.get('finalgrade','')}")
                print(f"Status: {f.get('status','')}")
                print(f"Defense Year: {f.get('defense_date_proposed','')[:4]}")
                print(f"PDF: {f.get('pdf_path','')}")

                print("Reviewers:")
                if "reviewers" in f:
                    for rev in f["reviewers"]:
                        rev_name = ""
                        for user in db["user"]:
                            if user["id"] == rev["id"]:
                                rev_name = user["name"]
                                break
                        print(f"  - {rev_name} ({rev['type']}): {rev['grade']}")
                print("---")
        else:
            print("no results found!")
        
            
            
    def get_grade_stu(self, grade):
        req=load_thesis()
        
        for i  in req:
            if i["student_id"]==self.id:
                if i["finalgrade"] !="" and i["finalresult"]!="":
                    fr=i["finalresult"]
                    fg=int(i["finalgrade"])
                    print(f"your final thesis grade is {fg}")
                    print(f"your final thesis result is {fr}")
                    if fg>=10:
                        print("congratulations!!!  you passssed!")
                    elif 0 <= fg <10:
                        print("unfortunately you failed :( ")
                    else:
                        print("invalid grade")

                else:
                    print("there is no grade for you")
                    return
        
        
    

