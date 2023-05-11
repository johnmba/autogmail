
from datetime import datetime, timedelta
import webbrowser
import time

from customtkinter import (
    CTkFrame, CTkTabview, CTkLabel, CTkEntry, CTkButton, IntVar, CTkRadioButton, StringVar
)

from reg_view_frame import Regdata, Generator
from datasheet import Datasheet


class Dataframe(CTkTabview):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.duration = 48
        self.hours = True
        self.yr = int(time.strftime("%Y"))
        self.mont = int(time.strftime("%m"))
        self.day = int(time.strftime("%d"))
        self.hr = int(time.strftime("%H"))
        self.min = int(time.strftime("%M"))
        self.sec = int(time.strftime("%S"))
        self.today = datetime(
            year=self.yr, month=self.mont, day=self.day, hour=self.hr, minute=self.min, second=self.sec
        )
        self.stop = self.today + timedelta(hours=self.duration)
        if not self.hours:
            self.stop = self.today + timedelta(minutes=self.duration)
        self.stored_data_set = 0
        self._command = self.fetch_more_data
        
        self.add(name="Live Data Generation")
        self.tab("Live Data Generation").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        
        self.timer = CTkFrame(master=self.tab(name="Live Data Generation"))
        self.timer.grid(row=0, column=0, padx=(10, 10), pady=(5,0), sticky="nsew")
        self.desc = CTkLabel(master=self.timer, text="This generator will stop generating after two days")
        self.desc.grid(row=0, column=0, padx=(10, 10), pady=(20,10), sticky="nsew")
        
        self.start_stop = CTkLabel(
            master=self.timer, text=f"Starts :  {self.today.ctime()} \n\nStops :  {self.stop.ctime()}"
        )
        self.start_stop.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew") 
        self.display_clock = CTkLabel(master=self.timer)
        self.display_clock.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        #set up timer for display
        self.elapsed = CTkLabel(master=self.timer, text="Time elapsed:")
        self.elapsed.grid(row=2, column=0, padx=(20, 5), pady=(20, 0))
         
        self.timing = CTkFrame(master=self.timer)
        self.timing.grid(row=2, column=1, padx=(20, 5), pady=(20, 0))
        self.hr_data = IntVar()
        self.hr_entry = CTkEntry(master=self.timing, textvariable=self.hr_data, width=30)
        self.hr_entry.grid(row=2, column=1, padx=(2, 2), sticky="w")
        self.min_data = IntVar()
        self.min_entry = CTkEntry(master=self.timing, textvariable=self.min_data, width=30)
        self.min_entry.grid(row=2, column=2, padx=(2, 2), sticky="w")
        self.secs_data = IntVar()
        self.sec_entry = CTkEntry(master=self.timing, textvariable=self.secs_data, width=30)
        self.sec_entry.grid(row=2, column=3, padx=(2, 2), sticky="w")
        
        #display user registeration detail in datasheet
        self.live_sheet = Datasheet(master=self.tab("Live Data Generation"))
        self.live_sheet.grid(row=1, column=0, sticky="nsew")
        
        self.live_data_contro = CTkFrame(master=self.tab("Live Data Generation"))
        self.live_data_contro.grid(row=2, column=0, padx=(20, 20), pady=(2, 0))
        self.duration_var = IntVar()
        self.live_durarion = CTkEntry(
            master=self.live_data_contro, textvariable=self.duration_var
        )
        self.live_durarion.grid(row=1, column=1)
        self.radio_var = IntVar()
        self.label_radio_group = CTkLabel(master=self.live_data_contro, text="Operation period type:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = CTkRadioButton(master=self.live_data_contro, text="Hour", variable=self.radio_var, value=1)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20)
        self.radio_button_2 = CTkRadioButton(master=self.live_data_contro, text="Minute", variable=self.radio_var, value=0)
        self.radio_button_2.grid(row=1, column=3, pady=10, padx=20)

        self.controls = CTkFrame(master=self.tab("Live Data Generation"))
        self.controls.grid(row=3, column=0, padx=20, pady=10)
        self.stop_live = CTkButton(master=self.controls, text="Stop")
        self.stop_live.grid(row=0, column=0, padx=20, pady=10)
        self.start_live = CTkButton(master=self.controls, text="Start", command=self.start_gen)
        self.start_live.grid(row=0, column=1, padx=20, pady=10)

        # frame for opening browser window for registeration   text="Data Registeration"
        self.reg_page_frame = Regdata(master=self.tab("Live Data Generation"))
        self.reg_page_frame.grid(row=0, column=1, sticky="nsew")

        # set up for user stored generated data
        description="Stored Data of an Email User.  Database stored data is viewed here"
        self.add(name="View Generated Data")
        self.tab("View Generated Data").grid_columnconfigure(0, weight=1)
        self.header = CTkLabel(self.tab("View Generated Data"), text=description)
        self.header.grid(row=0, column=0, padx=(20, 20), pady=(20,20), sticky="nsew")
        
        self.view_sheet = Datasheet(master=self.tab("View Generated Data"))
        self.live_sheet.grid(row=1, column=0, sticky="nsew")
        #self.tab("View Generated Data").bind(sequence="FocusIn", command=self.fetch_more_data)
        #self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        #Initialize time and call caroutine
        self.hr_data.set(00)
        self.min_data.set(00)
        self.secs_data.set(00)
        self.radio_var.set(1)
        self.duration_var.set(0)
        self.stop = False
        self.gen_started = False
        
        #self.elapsed = int(self.hr_data.get())*3600 + int(self.min_data.get())*60 + int(self.secs_data.get())
        
        self.display_clock.after(ms=1000, func=self.clock)
        
                
    def clock(self):
        """start a clock"""
        
        today = time.strftime("%A %B")
        am_pm = time.strftime("%p")
        hr = int(time.strftime("%H"))
        min = int(time.strftime("%M"))
        sec = int(time.strftime("%S"))
        clock_text = f"{today} \n\n {hr} : {min} : {sec} {am_pm}"
        self.display_clock.configure(text=clock_text)
        self.display_clock.after(ms=1000, func=self.clock)
                
    def gen_time(self):
        
        hr = self.hr_data.get()
        minu = self.min_data.get()
        sec = self.secs_data.get()
        
        stop_time = hr
        if self.hours:
            stop_time = minu
            
        if self.duration > stop_time and not self.stop:
            if sec == 60:
                minu =+ 1
                self.secs_data.set(value=00)
                self.min_data.set(value=minu)
            elif minu == 60:
                hr =+ 1
                self.min_data.set(value=00)
                self.hr_data.set(value=hr)
            else:
                sec = int(self.secs_data.get()) + 1
                self.secs_data.set(value=sec)
        self.timing.after(ms=1000, func=self.gen_time)

    def start_bot(self):
        """
        start the bot registeration operation
        call back after every specified time
        """
        gen_data = Generator()
        data = gen_data.generate_user_data()
        if reg := self.reg_page_frame.bot_reg(data=data):
            gen_data.data["username"] = reg
            gen_data.data["registered"] = True
            gen_data.data["active"] = True
            gen_data._recorddata()
            self.view_sheet.add(data=data)
        self.reg_page_frame.after(ms=1000, func=self.start_bot)
        
    def start_gen(self):
        """
        Start Generator manually with a time duration
        Stop generator manually 
        """
        global gen_started
        gen_started = True
        self.reg_page_frame.bot()
        duratn = self.duration_var.get()
        typ = self.radio_var.get()
        
        if duratn > 0:
            self.duration = duratn
            self.hours = bool(typ)
        self.gen_time()
        self.start_bot()
        
    def stop_gen(self):
        """
        Start Generator manually with a time duration
        Stop generator manually 
        """
        global gen_started
        gen_started = True
        self.stop = True
        

    def fetch_more_data(self):
        """
        Hide live frame and toggle generated frame
        re-run this function on fetch more with parameter of last data id
        """
        if self.get() == "View Generated Data":
            if fetched_data := Generator()._fetchdata():
                for data in fetched_data:
                    self.view_sheet.add(data=data)
                    print("sidebar_button click")
                self.view_sheet.update()
                self.stored_data_set = fetched_data[-1][0]

    