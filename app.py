from atexit import register
from tracemalloc import start
from bot.register_pref import RegisterPreference
from tkinter import BooleanVar, Checkbutton, StringVar, Tk, Label, Button, Entry, END

import re
import time

LOGIN = "" # Put your WhenToWork username
PASSWD = "" # Put your WhenToWork password
DAYS = {'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6}

class wtwbot(Tk):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
    
        # WIDGETS
        self.title("Preference Automate Bot - @hvcuong")
        self.instruction = Label(self, text="Format: [hour]:[00/15/30/45][AM/PM]. E.g: 12:30PM")
        self.start_label = Label(self, text = "Start Time")
        self.end_label = Label(self, text = "End Time")
        self.days_layout = []
        for day in DAYS:
            day = Label(self, text = day)
            self.days_layout.append(day)
        self.add_inquiry = Label(self, text = "Add hour for") 
        self.is_this_week = BooleanVar(value=True)
        self.is_next_week = BooleanVar(value=False)
        
        day_to_hour = self.populate_form()
        
        # LAYOUT
        self.instruction.grid(row=0,column=0,columnspan=3, padx=10, pady=10)
        self.start_label.grid(row = 1, column = 1)
        self.end_label.grid(row = 1, column = 2)
        for row in range(2,7):
            self.days_layout[row-2].grid(row = row, column = 0)
        self.add_inquiry.grid(row=7,column=0, padx=10, pady=10) 
        Checkbutton(self, text='this week', variable=self.is_this_week).grid(row=7,column=1)
        Checkbutton(self, text='next week', variable=self.is_next_week).grid(row=7,column=2)
        
        self.add_btn = Button(
            self, text='Add', command=(lambda : self.fetch_schedule(day_to_hour))
        )
        self.add_btn.grid(row=8,column=3,columnspan=3, padx=10, pady=10)   
        
        # CREATE ANOTHER FUNCTION TO POPULATE LOGIN SCREEN
        self.bot.land_homepage()
        self.bot.login(LOGIN, PASSWD)             
    
    def fetch_schedule(self, day_to_hour):
        processed_input_data = dict()
        for entry in day_to_hour:
            # Only take input from nonempty time entry boxes
            if (entry[1][0].get() != '' and entry[1][1].get() != ''):
                start_time = self.convert_AM_to_am(
                    time.strftime("%I%p%M", time.strptime(entry[1][0].get(), "%H:%M"))
                )
                end_time = self.convert_AM_to_am(
                    time.strftime("%I%p%M", time.strptime(entry[1][1].get(), "%H:%M"))
                )
                processed_register_time = [start_time.lstrip('0'), end_time.lstrip('0')]
                processed_input_data[DAYS[entry[0]]] = processed_register_time
        print(processed_input_data) 
        print(self.is_this_week.get())
        print(self.is_next_week.get())
        self.input_handler(processed_input_data)
    
    # Convert AM to am because of WhenToWork's poor frontend design. smh
    def convert_AM_to_am(self, time):
        if (time[2] == 'A'):
            return time.lower()
        return time
    
    def populate_form(self):
        # USER INPUT. 
        day_to_hour = []
        row = 2
        # Register the callback function to validate the input in the Entry widget
        reg = (self.register(self.onValidate), '%d', '%s', '%S')
        for day in DAYS:
            start_time = StringVar()
            e_start = Entry(self, textvariable=start_time, validate="key", validatecommand=reg)
            e_start.bind("<KeyRelease>", self.hour_24)
            e_start.grid(row = row, column = 1)
            
            end_time = StringVar()
            e_end = Entry(self, textvariable=end_time, validate="key", validatecommand=reg)
            e_end.bind("<KeyRelease>", self.hour_24)
            e_end.grid(row = row, column = 2)
            
            hour = [start_time, end_time]
            day_to_hour.append((day,hour))
            row += 1
        return day_to_hour
    
    def onValidate(self, d, s, S):
        # if it's deleting return True
        if d == "0":
            return True
        # Allow only digit, ":" and check the length of the string
        if ((S == ":" and len(s) != 2) or (not S.isdigit() and
                S != ":") or (len(s) == 3 and int(S) > 5) or len(s) > 4):
            self.bell()
            return False
         
        return True

    def hour_24(self, event):
        """
        Check and build the correct format hour: hh:mm in 24 format
        it keep in mind the 0x, 1x and 2x hours and the max minutes can be 59
        """
 
        # get the object that triggered the event
        s = event.widget
        # if delete a char do return ok or delete the char ":" and the previous number
        if len(s.get()) == 2 and event.keysym=="BackSpace":
            s.delete(len(s.get())-1, END)
        if event.keysym=="BackSpace":
            return
         
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 2:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) < 24:
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.bell()
            s.delete(1, END)
    
    def input_handler(self, process_input_data):
        if (self.is_this_week.get()):
            self.register_hour_per_day(process_input_data)
        if (self.is_next_week.get()):
            self.bot.navigate_forward_a_week()
            self.register_hour_per_day(process_input_data)

    def register_hour_per_day(self, processed_input_data):
        # Format the input data into 'HHam/PM - (0,15,30,45)' wtw format 
        for day in processed_input_data:            
            user_sh = processed_input_data[day][0][:-2]
            user_sm = processed_input_data[day][0][-2:]
            user_eh = processed_input_data[day][1][:-2]
            user_em = processed_input_data[day][1][-2:]
            self.bot.register_hour_per_day(day, user_sh, user_sm, user_eh, user_em)
    
if __name__ == '__main__':
    bot = RegisterPreference()
    app = wtwbot(bot)
    app.mainloop()

# bot = RegisterPreference()
# bot.land_homepage()
# bot.login(LOGIN,PASSWD)
# bot.register_hour_per_day(2, "12PM", "30", "3PM", "00")
# bot.register_hour_per_day(4, "12PM", "30", "3PM", "00") 
# bot.register_hour_per_day(6, "10am", "00", "3PM", "00")   
