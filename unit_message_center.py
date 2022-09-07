#!/usr/bin/env python
# coding: utf-8

#Unit Messaging Center version 4

#This application utilizes the pandas library to aggregate and sort soldier data for easy dissemination when needed. It utilizes the Termux Android Application to send messages
# programmatically. In it's current form it can send BA dates to specific squad level elements, squad leaders, and command teams.
#Future renditions will have additional capability to pull upcoming due dates and disseminate reminders to soldiers.

#Note: All the data  presented in these forms was generated using faker.

#Importing libraries to use

import pprint
from datetime import datetime, date, timedelta
import subprocess
import sys
import pandas as pd
import time

#universal variables

pp = pprint.PrettyPrinter(indent=4)
saved_stdout = sys.stdout


# In[4]:


#Function that checks BA dates 30,60,90 days out. 

def datechecker():
    baDate = ()
    try:
        baDate = str(FY22_30.loc[True]['BA22'])
    except KeyError:
        try:
            baDate = str(FY22_60.loc[True]['BA22'])
        except:
            baDate = str(FY22_90.loc[True]['BA22'])
    return baDate

#This Displays the current date at the beginning of the program and defines the BA dates. 

today = pd.to_datetime("today")
print("Today's date is " + str(today.date()))

d = {
    'BA22': ['2022-07-10', '2022-08-21', '2022-10-23', '2022-11-12', '2022-12-11', '2023-01-22', '2023-02-12', '2023'
                                                                                                               '-03-11',
             '2023-04-02', '2023-05-20', '2023-07-15', '2023-08-17']
}


#Creates a dataFrame to compare 30,60,90 dates when requested. 
#Needs to be edited for redundancy. 

df = pd.DataFrame(d)
df = pd.to_datetime(df.stack()).unstack()
today_thirty = today + timedelta(days=30)
today_sixty = today + timedelta(days=60)
today_ninety = today + timedelta(days=90)
today_onetwenty = today + timedelta(days=120)
df['thirty_days_out'] = df['BA22'].between(today, today_thirty)
df['sixty_days_out'] = df['BA22'].between(today_thirty, today_sixty)
df['ninety_days_out'] = df['BA22'].between(today_sixty, today_ninety)
df['onetwenty_days_out'] = df['BA22'].between(today_ninety, today_onetwenty)
FY22_30 = pd.DataFrame(df, columns=['thirty_days_out', 'BA22'])
FY22_30 = FY22_30.set_index('thirty_days_out')
FY22_30['BA22'] = pd.to_datetime(FY22_30['BA22']).dt.date
FY22_60 = pd.DataFrame(df, columns=['sixty_days_out', 'BA22'])
FY22_60 = FY22_60.set_index('sixty_days_out')
FY22_60['BA22'] = pd.to_datetime(FY22_60['BA22']).dt.date
FY22_90 = pd.DataFrame(df, columns=['ninety_days_out', 'BA22'])
FY22_90 = FY22_90.set_index('ninety_days_out')
FY22_90['BA22'] = pd.to_datetime(FY22_90['BA22']).dt.date
FY22_120 = pd.DataFrame(df, columns=['onetwenty_days_out', 'BA22'])
FY22_120 = FY22_120.set_index('onetwenty_days_out')
FY22_120['BA22'] = pd.to_datetime(FY22_120['BA22']).dt.date

#A place holder for a future roster_checking and editing option.

def check_roster():
    print("This piece has not been build yet.")
    print("Sorry.")
    print()
    main()

#A place holder for a future option that will allow the user to pull a list of items coming due, and send a reminder to soldiers. 

def do_outs():
    print("This piece has not been build yet.")
    print("Sorry.")
    print()
    main()

#Takes the option given in (main) and sends it to the proper function.
#Can probably be in main().

def level_two(main_select):
    if main_select == 1:
        message_center()
    if main_select == 2:
        reports()
    if main_select == 3:
        do_outs()
    if main_select == 4:
        check_roster()

#Main menu Function that allows user to select and verify what they would like to do. 

def main():
    print("[1] Message Center")
    print("[2] Reports")
    print("[3] Do-Outs")
    print("[4] Check Roster")
    print("[0] Exit the program.")
    print()
    main_select = int(input("Hey there! Select an option from the list above."))
    print()
    main_confirm = input("You have selected option, " + str(main_select) + " is that correct?")
    if main_confirm == "Yes" or "yes":
        level_two(main_select)
    else:      
        return

#This is the primary Function for the program. It allows the user to send a message using Termux on android. 

def message_center():
    print()
    
    #Calls prompt_display for User to select a prompt. The actual prompt is stored in this function as prompt_selection.
    
    prompt_display()
    print()
    prompt_selection = int(input("Please make a selection."))
    if (prompt_selection > 0) and (prompt_selection <= 3):
        prompt_selection = prompt(prompt_selection)
        print()
        print("You have selected" + prompt_selection+".")
        print()
    
    #If Prompt selection == 4, the User can create their own prompt.
    
    elif prompt_selection == 4:
        prompt_special = input("Please provide your prompt.")
        print()
        print("You have selected: \"", prompt_special, "\"")
        print()
    
    #Below the roster_option Function is called which allows the User to select who to send the message to. This is stored as roster_store. Once the roster is selected,
    #Soldier phone numbers are pulled from test_contact_roster and placed in the list phone_number.
    
    roster_store = roster_options()
    phone_roster = pd.read_excel('test_contact_roster.xlsx', index_col=None,  usecols=['Soldier Name','Cell Phone Number (RLAS)'])
    phone_roster = phone_roster.set_index('Soldier Name')
    phone_number = []
    for i in roster_store:
        phone_number.append((phone_roster.loc[[i]].to_string(header=None, index=None)))
        
    #The send_message Function is called which allows a User to confirm they would like to send the message, and what they would like the program to do after the message is sent.     
        
    message_choice = send_message()
    if message_choice == 3:
        main()
    roster_length = len(roster_store)
    i = 0
    while i > -1 and i <= roster_length-1:
        print("Sending: "+prompt_selection+" to "+ roster_store[i]+"\nat phone number: "+phone_number[i])
        smsmessage = str("Hello ") + roster_store[i] + str(" ") + str(prompt_selection or prompt_special)
        #uncheck below comment to send sms via termux.
        #subprocess.run(["termux-sms-send", "-n", phone_number[i], smsmessage])
        i= i +1
    if message_choice == 1:
        return
    if message_choice == 2:
        main()        

# Displays the prompt options. 

def prompt_display():
    print("[1] [Selected Roster], this is a test message. Please give a thumbs up if this is a good number.")
    print("[2] [Selected Roster], Reminder that next BA is " + datechecker() + '.')
    print("[3][SELECTED ROSTER], do-outs for next B.A. are: [Selected DO-OUTS]")
    print("[4] Provide your own prompt")

# Returns the appropriate prompt when selected by user. 

def prompt(i):
    prompt_store = {1: ", this is a test to confirm accurate phone numbers are on file. If this is a good number, "
                       "give a thumbs up.",
                    2: " , Reminder that next BA starts " + datechecker() + '.',
                    3: ", do-outs for next B.A. are: **[Selected DO-OUTS]**"}
    return prompt_store.get(i)

#This function will display a report based on User Selection of a column value.

def reports():
        final_report = []
        report_roster = pd.read_excel('test_contact_roster.xlsx')
        report_name = report_roster['Soldier Name'].tolist()
        report_request = str(input("Welcome to the Report Generator. Do you need to see a list?"))
        if report_request == "yes":
            pp.pprint(report_roster.columns.values.tolist())
        report_str = str(input("Which report would you like?"))
        report_gen = report_roster[report_str].tolist()
        report_dict = dict(zip(report_name, report_gen))
        contact_roster = pd.read_excel('nineteenoheight.xlsx')
        rosterrequest = str(input("Which Roster would you like? Do you need to see a list?"))
        roster_name = []
        if rosterrequest == "yes":
            pp.pprint(contact_roster.columns.values.tolist())
        soldier_name_select = str(input("Which roster would you like?"))
        for item in contact_roster[soldier_name_select]:
            if item in report_name:
                roster_name.append(item)
        report_dictB = dict(zip(roster_name, roster_name))
        report_compare = pd.DataFrame(columns=["Soldier Name", report_str])
        for k in report_dictB.keys() & report_dict.keys():
            final_report.append({report_str: report_dict[k], 'Soldier Name': report_dictB[k]})
        report_compare_final = report_compare.append(final_report, ignore_index=True ).to_string(index=False)
        print(report_compare_final)
        print()
        print("Report Complete")
        print("---------------")
        print()
        main()

def roster_options():
    nineteenoheight = pd.read_excel('nineteenoheight.xlsx')
    #nineteenoheight = nineteenoheight.dropna()
    print("[1] Full Roster")
    print("[2] Command Group")
    print("[3] Squad Leaders")
    print("[4] 1st Squad")
    print("[5] 2nd Squad")
    print("[6] 3rd Squad")
    print("[7] 4th Squad")
    print()
    roster_choice = int(input("Select an option above"))
    if roster_choice == 1:
        temp_store = nineteenoheight['full_roster'].tolist()
    if roster_choice == 2:
        temp_store = nineteenoheight['command_team'].tolist()
    if roster_choice == 3:
        temp_store = nineteenoheight['squad_leaders'].tolist()
    if roster_choice == 4:
        temp_store = nineteenoheight['first_squad'].tolist()
    if roster_choice == 5:
        temp_store = nineteenoheight['second_squad'].tolist()
    if roster_choice == 6:
        temp_store = nineteenoheight['third_squad'].tolist()
    if roster_choice == 7:
        temp_store = nineteenoheight['fourth_squad'].tolist()
    temp_store = [x for x in temp_store if str(x) != 'nan']
    print("Is the following list correct?")
    for item in temp_store:
        pp.pprint(item)
    roster_response = input("Yes or No?")
    if roster_response == "No":
        return roster_options()
    else:
        return temp_store

def send_message():
    print("Do you wish to send this message?")
    print("[1] Send message and close program.")
    print("[2] Send message and return to main menu.")
    print("[3] Do not send message and return to main menu.")
    print("[0] Exit the Program")
    print()
    selection = int(input("Please select an option above."))
    if selection == 0:
        return
    else:
        return selection

#Launch Application
main()
