import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, List
import os
from tkinter import messagebox
from datetime import datetime, timezone
from progress_tracker import TaskStatus, ChestCreationTracker
from chest_api import ChestAPIClient

class ChestCreationWizard:
    def __init__(self, icons_dir: str, app_config: dict, api_template: dict, logging_config: dict):
        self.icons_dir = icons_dir
        self.app_config = app_config
        self.api_template = api_template
        self.logging_config = logging_config
        
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title(app_config['ui']['title'])
        self.root.geometry(app_config['ui']['window_size'])
        
        # Initialize variables
        self.bonus_var = tk.BooleanVar(value=False)
        
        # Initialize progress tracker
        self.progress_tracker = ChestCreationTracker(
            icons_dir=icons_dir,
            logging_config=logging_config
        )
        
        self.current_screen = None
        self.data = {}  # Store user inputs
        
        # Initialize tracker
        self.tracker = None  # We'll initialize this when we know if bonus chest is needed
        
        # Create logs directory if it doesn't exist
        os.makedirs(self.logging_config.get('log_directory', 'logs'), exist_ok=True)
        
        # Show first screen
        self.show_screen1()

    def show_screen1(self):
        """Initial screen with basic inputs"""
        if self.current_screen:
            self.current_screen.destroy()
            
        self.current_screen = ttk.Frame(self.root, padding="10")
        self.current_screen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Chest Name Input
        ttk.Label(self.current_screen, text="Treasure Chest Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        chest_name = ttk.Entry(self.current_screen, width=40)
        chest_name.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # File Selection
        ttk.Label(self.current_screen, text="Item List File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        file_path_var = tk.StringVar()
        file_path_label = ttk.Label(self.current_screen, textvariable=file_path_var, wraplength=300)
        file_path_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        def select_file():
            filename = filedialog.askopenfilename(
                title="Select Item List File",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                file_path_var.set(filename)
                self.data['item_list_file'] = filename  # Store in self.data
        
        ttk.Button(self.current_screen, text="Browse", command=select_file).grid(row=1, column=2, pady=5)
        
        # Validate button
        ttk.Button(
            self.current_screen,
            text="Validate Item List",
            command=self.validate_item_list
        ).grid(row=2, column=0, columnspan=3, pady=5)
        
        # Bonus Chest Checkbox
        ttk.Checkbutton(
            self.current_screen,
            text="Bonus Chest Needed",
            variable=self.bonus_var,
            command=lambda: self.handle_bonus_checkbox()
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Bonus Chest Fields (initially hidden)
        self.bonus_frame = ttk.LabelFrame(self.current_screen, text="0 Percent Item Information", padding="5")
        self.bonus_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.bonus_frame.grid_remove()
        
        ttk.Label(self.bonus_frame, text="Item Id GUID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        zero_item_id = ttk.Entry(self.bonus_frame, width=40)
        zero_item_id.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.bonus_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity = ttk.Entry(self.bonus_frame, width=10)
        quantity.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Bottom Buttons
        button_frame = ttk.Frame(self.current_screen)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            button_frame,
            text="Start Chest Creation",
            command=lambda: self.validate_and_proceed_to_screen2(
                chest_name.get(),
                file_path_var.get(),
                self.bonus_var.get(),
                zero_item_id.get() if self.bonus_var.get() else None,
                quantity.get() if self.bonus_var.get() else None
            )
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        ).grid(row=0, column=1, padx=5)

    def handle_bonus_checkbox(self):
        """Handle the bonus checkbox state change"""
        has_bonus = self.bonus_var.get()
        print(f"Bonus checkbox state changed to: {has_bonus}")  # Debug print
        
        # Update the progress tracker with the new bonus state
        self.progress_tracker = ChestCreationTracker(
            icons_dir=self.icons_dir,
            logging_config=self.logging_config,
            has_bonus_chest=has_bonus
        )
        
        # If we have any UI elements that should show/hide based on bonus status,
        # update them here
        if hasattr(self, 'bonus_frame'):
            if has_bonus:
                self.bonus_frame.grid()
            else:
                self.bonus_frame.grid_remove()

    def validate_and_proceed_to_screen2(self, chest_name: str, file_path: str,
                                      bonus_needed: bool, zero_item_id: str = None,
                                      quantity: str = None):
        """Validate inputs and proceed to screen 2"""
        # Basic validation
        if not chest_name:
            self.show_error("Please enter a chest name")
            return
            
        if not file_path or not os.path.exists(file_path):
            self.show_error("Please select a valid item list file")
            return
            
        if bonus_needed:
            if not zero_item_id:
                self.show_error("Please enter the 0 percent item ID")
                return
            if not quantity or not quantity.isdigit():
                self.show_error("Please enter a valid quantity")
                return
        
        # Store the data
        self.data.update({
            'chest_name': chest_name,
            'item_list_file': file_path,
            'bonus_needed': bonus_needed,
            'zero_item_id': zero_item_id if bonus_needed else None,
            'quantity': int(quantity) if bonus_needed else None
        })
        
        # Proceed to screen 2
        self.show_screen2()

    def show_screen2(self):
        """Auth token input screen"""
        if self.current_screen:
            self.current_screen.destroy()
            
        self.current_screen = ttk.Frame(self.root, padding="10")
        self.current_screen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(
            self.current_screen,
            text="Paste Current Auth Token",
            font=('Arial', 12, 'bold')
        ).grid(row=0, column=0, pady=10)
        
        ttk.Label(
            self.current_screen,
            text="This will not be saved and will be properly encoded",
            font=('Arial', 10, 'italic')
        ).grid(row=1, column=0, pady=5)
        
        token_entry = ttk.Entry(self.current_screen, width=60)
        token_entry.grid(row=2, column=0, pady=20)
        
        continue_button = ttk.Button(
            self.current_screen,
            text="Continue",
            command=lambda: self.validate_and_proceed_to_screen3(token_entry.get()),
            state='disabled'
        )
        continue_button.grid(row=3, column=0, pady=10)
        
        # Enable continue button when token is entered
        def on_token_change(*args):
            continue_button['state'] = 'normal' if token_entry.get() else 'disabled'
            
        token_entry.bind('<KeyRelease>', on_token_change)

    def validate_and_proceed_to_screen3(self, token: str):
        """Validate token, get user info, then proceed to screen 3"""
        self.data['auth_token'] = token
        
        # Create API client
        client = ChestAPIClient(token, self.app_config['api'], self.api_template)
        
        try:
            # Get user account info
            response = client.get_user_account()
            if not response.success:
                self.show_error("Failed to get user account info")
                return
            
            # Store account info
            self.data['account_id'] = response.data['account_id']
            self.data['org_id'] = response.data['org_id']
            
            # Initialize tracker for God Rotation (simple, no bonus distinction needed)
            self.tracker = ChestCreationTracker(
                icons_dir=self.icons_dir,
                logging_config=self.logging_config,
                has_bonus_chest=False # Always false for God Rotation
            )
            
            # Proceed to screen 3
            self.show_screen3()
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def show_screen3(self):
        """Show the progress screen"""
        if self.current_screen:
            self.current_screen.destroy()

        # Resize window for better visibility
        self.root.geometry("600x800")  # Increased height to show all tasks and buttons

        # Initialize dictionaries to store status labels and icons
        self.status_labels = {}
        self.status_icons = {}

        # Create new frame with padding
        self.current_screen = ttk.Frame(self.root, padding="20")  # Increased padding
        self.current_screen.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights to allow proper expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Add progress display
        progress_frame = ttk.Frame(self.current_screen)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create progress display using tracker
        for idx, (task_name, status) in enumerate(self.tracker.tasks.items()):
            # Task name label
            ttk.Label(progress_frame, text=task_name).grid(row=idx, column=0, sticky=tk.W, padx=5)
            
            # Status icon - initialize with PENDING status
            icon_label = ttk.Label(progress_frame)
            icon_path = TaskStatus.PENDING.get_icon_path(self.icons_dir)
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                icon_label.configure(image=icon)
                icon_label.image = icon  # Keep a reference!
            icon_label.grid(row=idx, column=1, padx=5)
            self.status_icons[task_name] = icon_label
            
            # Status text - initialize with PENDING status
            status_label = ttk.Label(progress_frame, text=TaskStatus.PENDING.value)
            status_label.grid(row=idx, column=2, padx=5)
            self.status_labels[task_name] = status_label
        
        # Add buttons
        button_frame = ttk.Frame(self.current_screen)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Initialize all buttons as instance variables
        self.start_button = ttk.Button(button_frame, text="Start Creation", command=self.start_creation)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.back_button = ttk.Button(button_frame, text="Back", command=self.show_screen2)
        self.back_button.grid(row=0, column=1, padx=5)
        
        self.log_button = ttk.Button(button_frame, text="View Log", command=self.show_log, state='disabled')
        self.log_button.grid(row=0, column=2, padx=5)
        
        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit, state='disabled')
        self.exit_button.grid(row=0, column=3, padx=5)

    def update_task_display(self, task_name: str, status: TaskStatus):
        """Update the display for a single task"""
        if task_name in self.status_labels:
            # Update icon
            icon_path = status.get_icon_path(self.icons_dir)
            if os.path.exists(icon_path):
                new_icon = tk.PhotoImage(file=icon_path)
                self.status_icons[task_name].configure(image=new_icon)
                self.status_icons[task_name].image = new_icon
            
            # Update status text
            self.status_labels[task_name].configure(text=status.value)
            
            # Enable buttons if all tasks are complete
            if self.tracker.all_tasks_completed():
                if hasattr(self, 'log_button'):
                    self.log_button['state'] = 'normal'
                if hasattr(self, 'exit_button'):
                    self.exit_button['state'] = 'normal'

    def show_log(self):
        """Show the log file in a new window"""
        log_dir = self.logging_config.get('log_directory', 'logs')
        log_prefix = self.logging_config.get('log_file_prefix', 'chest_creation_')
        log_path = os.path.join(log_dir, f"{log_prefix}{self.data['chest_name']}.log")
        
        # Create new window
        log_window = tk.Toplevel(self.root)
        log_window.title(f"Log - {self.data['chest_name']}")
        log_window.geometry("800x600")
        
        # Create main frame with padding
        main_frame = ttk.Frame(log_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        log_window.grid_rowconfigure(0, weight=1)
        log_window.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Add header label
        ttk.Label(
            main_frame,
            text="Chest Creation Log",
            font=('Arial', 12, 'bold')
        ).grid(row=0, column=0, pady=(0, 10))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Courier', 10)
        )
        scrollbar = ttk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=text_widget.yview
        )
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Read and display log file
        try:
            with open(log_path, 'r') as f:
                log_content = f.read()
                text_widget.insert('1.0', log_content)
                text_widget.configure(state='disabled')  # Make read-only
        except Exception as e:
            text_widget.insert('1.0', f"Error reading log file: {str(e)}")
            text_widget.configure(state='disabled')
        
        # Add close button at bottom
        ttk.Button(
            main_frame,
            text="Close",
            command=log_window.destroy
        ).grid(row=2, column=0, pady=(10, 0))
        
        # Make window modal
        log_window.transient(self.root)
        log_window.grab_set()
        self.root.wait_window(log_window)

    def reset_to_screen1(self):
        """Reset the application to the initial screen"""
        self.data = {}  # Clear stored data
        self.show_screen1()

    def show_error(self, message: str):
        """Show error popup"""
        messagebox.showerror("Error", message)

    def start_api_process(self):
        """Begin the API call sequence"""
        # Placeholder for God Rotation API process
        # 1. Get selected/deselected gods from Screen 3 data
        # 2. Create task list (e.g., ("Update LTI for God X", self.update_god_lti, god_data))
        # 3. Call self.process_next_task()
        print("Placeholder: start_api_process needs rewrite for God Rotation.")
        # Example: Simulate immediate finish for now
        self.log_button['state'] = 'normal'
        self.exit_button['state'] = 'normal'

    def process_next_task(self):
        """Process the next task in the queue"""
        if not self.task_queue:
            # All tasks completed
            return
        
        task_name, task_func = self.task_queue[0]
        
        # Update status to Processing
        self.tracker.update_task_status(task_name, TaskStatus.PROCESSING)
        self.update_task_display(task_name, TaskStatus.PROCESSING)
        
        try:
            # Execute the task
            result = task_func()
            
            # Store result data if needed
            if result:
                self.data[task_name] = result
            
            # Update status to Success
            self.tracker.update_task_status(task_name, TaskStatus.SUCCESS)
            self.update_task_display(task_name, TaskStatus.SUCCESS)
            
        except Exception as e:
            # Handle error
            self.tracker.update_task_status(
                task_name, 
                TaskStatus.FAILURE, 
                message=str(e)
            )
            self.update_task_display(task_name, TaskStatus.FAILURE)
            self.show_error(f"Error in {task_name}: {str(e)}")
            return
        
        # Remove completed task and schedule next task
        self.task_queue.pop(0)
        if self.task_queue:
            # Schedule next task with a small delay
            self.root.after(100, self.process_next_task)
        else:
            # All tasks completed, write log and enable buttons
            log_path = os.path.join("logs", f"chest_creation_{self.data['chest_name']}.log")
            os.makedirs("logs", exist_ok=True)
            self.tracker.write_log(log_path)
            self.log_button['state'] = 'normal'
            self.exit_button['state'] = 'normal'

    def update_bonus_chest_status(self, has_bonus: bool):
        """Update tracker when bonus chest status changes"""
        self.tracker = ChestCreationTracker(
            icons_dir=self.icons_dir,
            logging_config=self.logging_config,
            has_bonus_chest=has_bonus
        )

    def run(self):
        """Start the application"""
        self.root.mainloop()

    def create_chest_details_screen(self):
        # ... existing code ...

        # Create bonus frame
        self.bonus_frame = ttk.LabelFrame(self.current_screen, text="Bonus Chest Details")
        
        # Add bonus-specific inputs
        tk.Label(self.bonus_frame, text="Bonus Chest Name:").pack(pady=5)
        self.bonus_name_entry = tk.Entry(self.bonus_frame)
        self.bonus_name_entry.pack(pady=5)
        
        tk.Label(self.bonus_frame, text="Bonus Description:").pack(pady=5)
        self.bonus_desc_entry = tk.Entry(self.bonus_frame)
        self.bonus_desc_entry.pack(pady=5)
        
        # Only show bonus frame if checkbox is checked
        if self.bonus_var.get():
            self.bonus_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # ... rest of existing code ...

    def start_creation(self):
        """Start the chest creation process"""
        try:
            # Disable all control buttons during creation
            self.start_button['state'] = 'disabled'
            self.back_button['state'] = 'disabled'
            self.exit_button['state'] = 'disabled'
            
            # Initialize API client and start process
            client = ChestAPIClient(
                self.data['auth_token'],
                self.app_config['api'],
                self.api_template
            )
            
            self.start_api_process()
            
        except Exception as e:
            self.show_error(f"Failed to start creation process: {str(e)}")
            # Re-enable control buttons
            self.start_button['state'] = 'normal'
            self.back_button['state'] = 'normal'
            self.exit_button['state'] = 'normal'

    def validate_item_list(self):
        """Validate the selected item list file"""
        # Placeholder - Validation not needed for God Rotation
        messagebox.showinfo("Info", "Item List Validation is not applicable for God Rotation.")
