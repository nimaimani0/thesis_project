#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 22:02:22 2025

@author: nima
"""

from utils import load_database, save_database, load_data_basee
from master import master
from student import student
import sys
def show(title: str):
    print(f"{title.center(40)}")

class Panel:
    def __init__(self, user, data):
        self.user = user
        self.data = data
    
    def run(self):
        while True:
            if isinstance(self.user, student):
                self.student_panel()
            elif isinstance(self.user, master):
                self.professor_panel()
            

    def student_panel(self):
        while True:
            print(f"\nwelcome {self.user.name}!")
            print("------ student menu ------")
            print("please choose an item:")
            print("1. change password")
            print("2. send thesis request")
            print("3. show thesis status")
            print("4. send defense request")
            print("5. watch thesises")
            print("6. your thesis mark")
            print("7. exit")
            
           
            choice = input("choose: ")
            if choice == "1":
                self.user.change_password(self.data)
            elif choice == "2":
                self.user.req_thesis(self.data)
            elif choice == "3":
                self.user.show_status(self.data)
            elif choice == "4":
                self.user.request_defense(self.data)
            elif choice == "5":
                self.user.search_archive(self.data)
            elif choice == "6":
                self.user.get_grade_stu(self.data)
            elif choice == "7":
                sys.exit()
            else:
                print("invalid choice!")

    def professor_panel(self):
        while True:
            print(f"\nwelcome {self.user.name}!")
            print("------ professor Menu ------")
            print("please choose an item:")
            print("1. change password")
            print("2. show and manage thesis requests")
            print("3. manage defense request")
            print("4. submit grade")
            print("5  watch thesises")
            print("6  exit")
            
            choice = input("choose: ")
            if choice == "1":
                self.user.change_password(self.data)
            elif choice == "2":
                self.user.view_thesis_req(self.data)
            elif choice == "3":
                self.user.manage_defense_requests(self.data)
            elif choice == "4":
                self.user.submit_grade(self)
            elif choice =="5":
                self.user.search_archive(self.data)
            elif choice=="6":
                sys.exit()
            else:
                print("invalid choice!")

class Login:
    @staticmethod
    def authentication():
        show("Portal")
        id_input = input("please enter your ID: ")
        password_input = input("Please enter your password: ")
        data = load_database()

        for user_data in data["user"]:
            if user_data["id"] == id_input and user_data["password"] == password_input:
                if user_data["person"] == "student":
                    return student(
                        user_data["id"],
                        user_data["name"],
                        user_data["major"],
                        user_data["password"],
                        user_data.get("thesis_request")
                    )
                elif user_data["person"] == "professor":
                    return master(
                        user_data["id"],
                        user_data["name"],
                        user_data["major"],
                        user_data["password"],
                        user_data.get("supervision_capacity"),
                        user_data.get("review_capacity"),
                        user_data.get("courses", [])
                    )
        
        print("user not found!")
        return None

def main():
    data = load_database()
    user = Login.authentication()
    if not user:
        print("exiting...")
        return
    
    panel = Panel(user, data)
    panel.run()

if __name__ == "__main__":
    main()