from atexit import register
from bot.register_pref import RegisterPreference
from tkinter import BooleanVar, Checkbutton, StringVar, Tk, Label, Button, Entry

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
    
    def fetch_schedule(self, day_to_hour):
        processed_input_data = dict()
        for entry in day_to_hour:
            if (entry[1][0].get() != '' and entry[1][1].get() != ''):
                processed_register_time = [entry[1][0].get(), entry[1][1].get()]
                processed_input_data[DAYS[entry[0]]] = processed_register_time
        print(processed_input_data) 
        print(self.is_this_week.get())
        print(self.is_next_week.get())
        self.register(processed_input_data)
    
    def populate_form(self):
        # USER INPUT. 
        day_to_hour = []
        row = 2
        for day in DAYS:
            start_time = StringVar()
            Entry(self, textvariable=start_time).grid(row = row, column = 1)
            end_time = StringVar()
            Entry(self, textvariable=end_time).grid(row = row, column = 2)
            hour = [start_time, end_time]
            day_to_hour.append((day,hour))
            row += 1
        return day_to_hour

    def register(self, processed_input_data):
        if (self.is_this_week):
            for day in processed_input_data:
                pass   
        pass
    
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
