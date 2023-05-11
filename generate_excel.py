
from glob import glob

from tkinter import Listbox
from customtkinter import CTkTabview, CTkOptionMenu, CTkLabel, CTkButton, CTkEntry

from export import Generator


class Genexcel(CTkTabview):
    
    def __init__(self, master, **kwargs):
        
        super().__init__(master, **kwargs)
        
        #self.excel_tabs = customtkinter.CTkTabview(master=self.sidebar_frame, width=250) create excel_tabs
        #self.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.add("Generate Excel")
        self.add("View Excel")
        self.tab("Generate Excel").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tab("View Excel").grid_columnconfigure(0, weight=1)

        self.filter_label = CTkLabel(self.tab("Generate Excel"), text="Filter By date")
        self.filter_label.grid(row=0, column=0, padx=20, pady=10)
        self.filter_menu = CTkOptionMenu(
            self.tab("Generate Excel"), dynamic_resizing=False, values=["value 1", "Value 2", "Value Long Long Long"],
        )
        self.filter_menu.grid(row=1, column=0, padx=20, pady=(20, 10))
        
        #limitvar = StringVar(value=str(500)) textvariable=limitvar,
        self.limit_entry = CTkEntry(self.tab("Generate Excel"), placeholder_text="Specify limit")
        self.limit_entry.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.gen_button = CTkButton(
            self.tab("Generate Excel"), text="Generate Excel", command=self.generated_excel
        )
        self.gen_button.grid(row=3, column=0, padx=20, pady=(10, 10))
        
        # List Generated files
        self.lb = Listbox(master=self.tab("View Excel"))
        self.lb.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.no_file = CTkLabel(master=self.tab("View Excel"), text="There is no file to display")
        self.no_file.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.filter_menu.set("Today")
        self.limit_entry.setvar("500")
    
    def generate_excel(self):
        """
        Generate data according to specification
        save generated data in an excell document
        """
        gen = Generator()
        data = gen.filedata()

    def generated_excel(self):
            """
            List Generate excel documents
            """
            
            if files := glob("*.xlsx"):
                self.no_file.grid_remove()
                for file in files:
                    self.lb.insert(file)
            
        
                
                    