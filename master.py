#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 17:08:53 2025

@author: nima
"""

import json
from user import user
from utils import load_database , save_database ,load_data_basee,save_dataibasee,load_thesis,save_thesis
from datetime import datetime, timedelta

class master(user):
    def __init__(self,id,name,person,major,password,thesis_request=None,supervision_capacity=None,review_capacity=None,courses=[]):
        super().__init__(id,name,"professor",major,password)
    
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
    
    def view_thesis_req(self, dataa):
        req = load_thesis()
        data = load_data_basee()
        dataa = load_database()
        
        for n in req:
            if n["professor_id"] == self.id:
                print(f" {n['thesis_id']} , {n['student_id']} , {n['title']} , {n['status']}, {n['date']} \n")
        
        print("\nenter 1 to manage them (press any key to return)")
        chosse = input()
        if chosse == "1":
            reqid = input("enter request id number for managing:")
            if reqid.isdigit():
                reqid = int(reqid)
                bol = True
                for n in req:
                    if n["thesis_id"] == reqid:
                        bol = False
                        print("choose an item: \n1. accept\n2. reject ")
                        chose = input()
                        if chose == "1":
                            n["status"] = "approve"
                            n["approval_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            for i in data["course"]:
                                if i["professor_id"] == self.id and i["title"] == n["title"]:
                                    i["capacity"] = i["capacity"] - 1
                                    save_dataibasee(data)
                            save_thesis(req)
                            for n in dataa["user"]:
                                if n["id"] == self.id:
                                    n["supervision_capacity"] = n["supervision_capacity"] - 1
                                    save_database(dataa)
                        elif chose == "2":
                            n["status"] = "reject"
                            save_thesis(req)
                        else:
                            print("invalid input")
                            return
                if bol:
                    print("invalid input")
                    return
        elif chosse == "2":
            self.manage_defense_requests()
        else:
            return
    
    def manage_defense_requests(self,data):
        req = load_thesis()
        dataa = load_database()
        
        defense_requests = []
        for n in req:
            if n["professor_id"] == self.id and n["defense_requested"] == 1 and n["defense_approved"] == 0:
                defense_requests.append(n)
        
        if not defense_requests:
            print("no defense requests found!")
            return
        
        for dr in defense_requests:
            print(f"Thesis ID: {dr['thesis_id']}, Student: {dr['student_id']}, Title: {dr['title']}")
            print(f"Proposed Date: {dr['defense_date_proposed']}")
            print("Abstract:", dr['abstract'][:50] + "..." if dr['abstract'] else "no abstract")
            print("---")
        
        thesis_id = input("enter thesis id to manage: ")
        if thesis_id.isdigit():
            thesis_id = int(thesis_id)
            for n in req:
                if n["thesis_id"] == thesis_id and n["professor_id"] == self.id:
                    print("1. Auto-add internal reviewer and select external\n2. Reject defense")
                    choice = input("choose: ")
                    
                    if choice == "1":
                        student_major = ""
                        for user in dataa["user"]:
                            if user["id"] == n["student_id"]:
                                student_major = user["major"]                            
                                break
                        
                        
                        supervisor_reviewer = None
                        for user in dataa["user"]:
                            if (user["person"] == "professor" and 
                                user["id"] == self.id and 
                                user["review_capacity"] > 0 and
                                user["major"] == student_major):
                                supervisor_reviewer = user
                                break
                        
                        if not supervisor_reviewer:
                            print("your supervisor capacity is full!")
                            return
                        
                        n["reviewers"].append({
                            "id": supervisor_reviewer["id"],
                            "type": "supervisor",
                            "grade": None
                        })
                        
                        for user in dataa["user"]:
                            if user["id"] == supervisor_reviewer["id"]:
                                user["review_capacity"] -= 1
                        
                        print(f"{supervisor_reviewer['name']} you added to list for giving mark!")
                        
                        internal_reviewer = None
                        for user in dataa["user"]:
                            if (user["person"] == "professor" and 
                                user["id"] != self.id and 
                                user["review_capacity"] > 0 and
                                user["major"] == student_major):
                                internal_reviewer = user
                                break
                        
                        if not internal_reviewer:
                            print("no available internal reviewer found!")
                            return
                        
                        n["reviewers"].append({
                            "id": internal_reviewer["id"],
                            "type": "internal",
                            "grade": None
                        })
                        
                        for user in dataa["user"]:
                            if user["id"] == internal_reviewer["id"]:
                                user["review_capacity"] -= 1
                        
                        print(f"internal reviewer {internal_reviewer['name']} added automatically!")
                        
                        available_external = []
                        for user in dataa["user"]:
                            if (user["person"] == "professor" and 
                                user["id"] != self.id and 
                                user["id"] != internal_reviewer["id"] and
                                user["review_capacity"] > 0 and
                                user["major"] != student_major):
                                available_external.append(user)
                        
                        if not available_external:
                            print("no available external reviewers found!")
                            for user in dataa["user"]:
                                if user["id"] == internal_reviewer["id"]:
                                    user["review_capacity"] += 1
                            n["reviewers"] = []
                            save_database(dataa)
                            save_thesis(req)
                            return
                        
                        print("select external reviewer (different major):")
                        for idx, rev in enumerate(available_external, 1):
                            print(f"{idx}. {rev['name']} ({rev['major']}) - Capacity: {rev['review_capacity']}")
                        
                        rev_choice = input("select reviewer number: ")
                        if rev_choice.isdigit() and 1 <= int(rev_choice) <= len(available_external):
                            selected_rev = available_external[int(rev_choice)-1]
                            n["reviewers"].append({
                                "id": selected_rev["id"],
                                "type": "external", 
                                "grade": None
                            })
                            
                            for user in dataa["user"]:
                                if user["id"] == selected_rev["id"]:
                                    user["review_capacity"] -= 1
                            
                            print(f"external reviewer {selected_rev['name']} added!")
                            
                            n["defense_approved"] = 1
                            n["defense_date"] = n["defense_date_proposed"]
                            
                            save_database(dataa)
                            save_thesis(req)
                            print("defense approved with both reviewers!")
                        else:
                            print("invalid selection!")
                            for user in dataa["user"]:
                                if user["id"] == internal_reviewer["id"]:
                                    user["review_capacity"] += 1
                            n["reviewers"] = []
                            save_database(dataa)
                            save_thesis(req)
                    
                    elif choice == "2":
                        n["defense_requested"] = 0
                        for reviewer in n["reviewers"]:
                            for user in dataa["user"]:
                                if user["id"] == reviewer["id"]:
                                    user["review_capacity"] += 1
                        n["reviewers"] = []
                        save_database(dataa)
                        save_thesis(req)
                        print("defense rejected!")
                    
                    else:
                        print("invalid choice!")
                    
                    return
            print("thesis not found!")
        else:
            print("invalid input!")
    
    
    
    def submit_grade(self, data):
        req = load_thesis()
        dataa = load_database()
        dat=load_data_basee()
        
        my_reviews = []
        for n in req:
            for reviewer in n["reviewers"]:
                
                if (reviewer["id"] == self.id and reviewer["grade"] is None and 
                    n["defense_approved"] == 1 and n["status"] == "approve"):
                    my_reviews.append(n)
                    break
        
        if not my_reviews:
            print("no theses to grade!")
            return
        
        for thesis in my_reviews:
            print(f"Thesis ID: {thesis['thesis_id']}, Title: {thesis['title']}, Student: {thesis['student_id']}")
        
        thesis_id = input("enter thesis id to grade: ")
        if thesis_id.isdigit():
            thesis_id = int(thesis_id)
            for n in req:
                if n["thesis_id"] == thesis_id:
                    for reviewer in n["reviewers"]:
                        if reviewer["id"] == self.id and reviewer["grade"] is None:
                            grade=int(30)
                            while (grade >int(20)  or grade<int(0)):                   
                                grade = int(input("enter grade (0-20): "))
                                if (grade>int(20) or grade<int(0)):
                                    print("your input is out of range")
                            grade=str(grade)
                            if grade.replace('.', '').isdigit() and 0 <= float(grade) <= 20:
                                reviewer["grade"] = float(grade)
                                
                               
                                all_graded = True
                                grades = []
                                for rev in n["reviewers"]:
                                    if rev["grade"] is None:
                                        all_graded = False
                                        break
                                    grades.append(rev["grade"])
                                
                                if all_graded:
                                    
                                    tgrade = sum(grades) / 3
                                    n["finalgrade"] = tgrade
                                    if 17 <=tgrade <= 20:
                                        n["finalresult"]="الف"
                                    elif 13 <= tgrade < 17:
                                        n["finalresult"]="ب"
                                        
                                    elif 10 <= tgrade < 13:
                                        n["finalresult"]="ج"
                                    else:
                                        n["finalresult"]="د"
                                    
                                    
                                    if n["finalgrade"] >= 10:
                                        n["status"] = "pass"
                                    else:
                                        n["status"] = "fail"
                                    
                                    
                                    for rev in n["reviewers"]:
                                        for user in dataa["user"]:
                                            if user["id"] == rev["id"]:
                                                user["review_capacity"] += 1
                                    for m in dat["course"]:
                                        if m["professor_id"]==self.id and m["title"]==n["title"]:
                                            m["capacity"]+=1
                                
                                save_thesis(req)
                                save_database(dataa)
                                save_dataibasee(dat)
                                print("grade submitted!")
                                return
            print("thesis not found or not authorized!")
        else:
            print("invalid input!")
    
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
        