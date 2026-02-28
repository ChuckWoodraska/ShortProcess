import customtkinter as ctk
import threading
import time
from .process_monitor import ProcessMonitor

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ProcessApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Docker & Python Process Viewer")
        self.geometry("1300x700") # Increased width further for Image column

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row 2 is the scrollable content

        # 1. Header Frame (Title & Refresh)
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Active Processes", font=("Roboto", 24))
        self.title_label.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(self.header_frame, text="Refresh Now", command=self.refresh_data)
        self.refresh_button.pack(side="right", padx=10)

        # 2. Table Header Frame (Fixed)
        self.table_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.table_header_frame.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="ew")
        
        # Configure columns (TOTAL: 6 columns now)
        # 0: PID
        # 1: Name (Container Name / Process Name)
        # 2: Image (Image Name / Empty)
        # 3: Arguments
        # 4: Status
        # 5: Ports
        self.table_header_frame.grid_columnconfigure(0, weight=1) 
        self.table_header_frame.grid_columnconfigure(1, weight=2) 
        self.table_header_frame.grid_columnconfigure(2, weight=2) # New Image col
        self.table_header_frame.grid_columnconfigure(3, weight=4) 
        self.table_header_frame.grid_columnconfigure(4, weight=1) 
        self.table_header_frame.grid_columnconfigure(5, weight=1) 

        headers = ["PID", "Name", "Image", "Arguments", "Status", "Ports"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_header_frame, text=header, font=("Roboto", 16, "bold"), anchor="w")
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        # 3. Content Frame (Scrollable)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=2)
        self.scrollable_frame.grid_columnconfigure(2, weight=2) # New Image col
        self.scrollable_frame.grid_columnconfigure(3, weight=4)
        self.scrollable_frame.grid_columnconfigure(4, weight=1)
        self.scrollable_frame.grid_columnconfigure(5, weight=1)

        # Data Storage
        self.process_widgets = []
        
        # Initial Load
        self.refresh_data()

    def refresh_data(self):
        # Clear existing widgets
        for widget in self.process_widgets:
            widget.destroy()
        self.process_widgets.clear()

        # Fetch new data
        processes = ProcessMonitor.get_processes()

        # Populate table
        for i, proc in enumerate(processes, start=0):
            # PID
            pid_label = ctk.CTkLabel(self.scrollable_frame, text=str(proc['pid']), anchor="w")
            pid_label.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            
            # Name
            name_label = ctk.CTkLabel(self.scrollable_frame, text=proc['name'], anchor="w")
            name_label.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            
            # Image
            image_text = proc.get('image', "")
            image_label = ctk.CTkLabel(self.scrollable_frame, text=image_text, anchor="w")
            image_label.grid(row=i, column=2, padx=5, pady=2, sticky="ew")
            
            # Arguments (Scrollable Box)
            args_text = proc.get('arguments', "")
            args_box = ctk.CTkTextbox(self.scrollable_frame, height=40, wrap="word") 
            args_box.insert("0.0", args_text)
            args_box.configure(state="disabled") # Read-only
            args_box.grid(row=i, column=3, padx=5, pady=2, sticky="ew")
            
            # Status
            status_label = ctk.CTkLabel(self.scrollable_frame, text=proc['status'], anchor="w")
            status_label.grid(row=i, column=4, padx=5, pady=2, sticky="ew")
            
            # Ports
            ports_text = ", ".join(map(str, proc['ports'])) if proc['ports'] else "-"
            ports_label = ctk.CTkLabel(self.scrollable_frame, text=ports_text, anchor="w")
            ports_label.grid(row=i, column=5, padx=5, pady=2, sticky="ew")

            self.process_widgets.extend([pid_label, name_label, image_label, args_box, status_label, ports_label])
