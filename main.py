import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import tkintermapview
from datetime import datetime

class CivicEngagementApp:
    """
    A GUI application for a civic engagement platform using tkinter.
    This version uses an interactive map for location reporting, includes timestamps,
    and saves data to a JSON file for persistence.
    """
    def __init__(self, root):
        """
        Initializes the main application window.
        Args:
            root: The root tkinter window.
        """
        self.data_file = "civic_issues.json"
        self.database = self.load_data()  # Load data from file on startup
        
        # --- Main Window Configuration ---
        self.root = root
        self.root.title("Civic Engagement Platform")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f0f0")

        # --- Main Frame ---
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both")

        # --- Title Label ---
        title_label = tk.Label(
            main_frame, 
            text="Welcome to the Civic Engagement Platform",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=(10, 20))

        # --- Main Menu Buttons ---
        button_style = {
            "font": ("Helvetica", 12),
            "bg": "#007BFF",
            "fg": "white",
            "activebackground": "#0056b3",
            "activeforeground": "white",
            "relief": "flat",
            "borderwidth": 0,
            "width": 25,
            "pady": 10
        }

        report_button = tk.Button(
            main_frame, 
            text="Report a New Issue", 
            command=self.open_report_window,
            **button_style
        )
        report_button.pack(pady=10)

        view_button = tk.Button(
            main_frame, 
            text="View All Reported Issues", 
            command=self.open_view_window,
            **button_style
        )
        view_button.pack(pady=10)

        exit_button_style = button_style.copy()
        exit_button_style['bg'] = "#dc3545"
        exit_button_style['activebackground'] = "#c82333"

        exit_button = tk.Button(
            main_frame, 
            text="Exit", 
            command=self.root.quit,
            **exit_button_style
        )
        exit_button.pack(pady=10)

    def load_data(self):
        """
        Loads the issue data from the JSON file.
        """
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self):
        """
        Saves the current list of issues to the JSON file.
        """
        with open(self.data_file, 'w') as f:
            json.dump(self.database, f, indent=4)

    def open_report_window(self):
        """
        Opens a new window with a map for reporting an issue.
        """
        report_win = tk.Toplevel(self.root)
        report_win.title("Report a New Issue")
        report_win.geometry("600x750") # Increased size for map and time entry
        report_win.configure(bg="#f0f0f0")

        # --- Main Frame for the report window ---
        frame = tk.Frame(report_win, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True, fill="both")

        # --- Issue Type and Description ---
        tk.Label(frame, text="Type of Issue:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        issue_types = ["Pothole", "Broken Streetlight", "Trash/Litter", "Graffiti", "Public Transportation", "Other"]
        issue_type_var = tk.StringVar(value=issue_types[0])
        type_dropdown = ttk.Combobox(frame, textvariable=issue_type_var, values=issue_types, state="readonly")
        type_dropdown.pack(fill="x", pady=(5, 10))

        tk.Label(frame, text="Description:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        description_entry = tk.Entry(frame, font=("Helvetica", 11), width=40)
        description_entry.pack(fill="x", pady=(5, 10))

        # --- Timestamp Entry ---
        time_frame = tk.Frame(frame, bg="#f0f0f0")
        time_frame.pack(fill="x", pady=(10, 0), anchor="w")
        
        use_current_time_var = tk.BooleanVar(value=True)

        def toggle_time_entry():
            if use_current_time_var.get():
                time_entry.config(state="disabled")
            else:
                time_entry.config(state="normal")

        tk.Label(time_frame, text="Time of Issue:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        current_time_check = tk.Checkbutton(
            time_frame,
            text="Use current time",
            variable=use_current_time_var,
            command=toggle_time_entry,
            bg="#f0f0f0",
            activebackground="#f0f0f0"
        )
        current_time_check.pack(anchor="w")

        tk.Label(time_frame, text="Or enter manually (e.g., YYYY-MM-DD HH:MM):", font=("Helvetica", 9), bg="#f0f0f0").pack(anchor="w", pady=(5,0))
        time_entry = tk.Entry(time_frame, font=("Helvetica", 11), width=40)
        time_entry.pack(fill="x", pady=(5, 10))
        toggle_time_entry() # Set initial state of the entry box

        # --- Map for Location ---
        tk.Label(frame, text="Location (Right-click on map to set):", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w", pady=(10,5))
        map_widget = tkintermapview.TkinterMapView(frame, width=560, height=300, corner_radius=5)
        map_widget.pack(fill="both", expand=True)

        deepdale_lat, deepdale_lon = 53.765, -2.685
        map_widget.set_position(deepdale_lat, deepdale_lon)
        map_widget.set_zoom(15)
        marker = map_widget.set_marker(deepdale_lat, deepdale_lon, text="Issue Location")

        def set_marker_event(coords):
            marker.set_position(coords[0], coords[1])

        map_widget.add_right_click_menu_command(label="Set Issue Location", command=set_marker_event, pass_coords=True)

        # --- Submit Logic ---
        def submit_issue():
            issue_type = issue_type_var.get()
            description = description_entry.get()
            location_coords = marker.position

            if use_current_time_var.get():
                timestamp = datetime.now().isoformat()
            else:
                timestamp = time_entry.get()

            if not description:
                messagebox.showerror("Error", "Please provide a description.", parent=report_win)
                return

            issue_report = {
                "type": issue_type,
                "description": description,
                "location": location_coords,
                "timestamp": timestamp,
                "status": "Reported"
            }
            self.database.append(issue_report)
            self.save_data()
            
            messagebox.showinfo("Success", "Issue reported successfully!", parent=report_win)
            
            self.refresh_view_window()
            report_win.destroy()

        submit_button = tk.Button(frame, text="Submit Report", command=submit_issue, bg="#28a745", fg="white", font=("Helvetica", 12), relief="flat")
        submit_button.pack(pady=20)

    def open_view_window(self):
        """
        Opens a new window to display all reported issues.
        """
        if hasattr(self, 'view_win') and self.view_win and self.view_win.winfo_exists():
            self.view_win.lift()
        else:
            self.view_win = tk.Toplevel(self.root)
            self.view_win.title("All Reported Issues")
            self.view_win.geometry("600x400")
            self.view_win.configure(bg="#ffffff")
            self.view_win.bind("<Destroy>", lambda e: setattr(self, "view_win", None))
            self.draw_view_widgets()

    def draw_view_widgets(self):
        """
        Draws or redraws the content of the view window.
        """
        for widget in self.view_win.winfo_children():
            widget.destroy()
            
        canvas = tk.Canvas(self.view_win, bg="#ffffff")
        scrollbar = tk.Scrollbar(self.view_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if not self.database:
            tk.Label(scrollable_frame, text="No issues have been reported yet.", font=("Helvetica", 12), bg="white").pack(pady=20)
        else:
            for i, report in enumerate(self.database):
                issue_frame = tk.Frame(scrollable_frame, bd=2, relief="groove", padx=10, pady=10, bg="#f9f9f9")
                issue_frame.pack(fill="x", padx=10, pady=5, anchor="w")
                
                header = f"Issue #{i+1}: {report['type']} ({report['status']})"
                tk.Label(issue_frame, text=header, font=("Helvetica", 12, "bold"), bg="#f9f9f9", anchor="w").pack(fill="x")
                tk.Label(issue_frame, text=f"Description: {report['description']}", bg="#f9f9f9", anchor="w").pack(fill="x")
                
                location = report.get('location', 'N/A')
                if isinstance(location, (list, tuple)):
                    loc_text = f"Location (Lat/Lon): {location[0]:.5f}, {location[1]:.5f}"
                else:
                    loc_text = f"Location: {location}"
                tk.Label(issue_frame, text=loc_text, bg="#f9f9f9", anchor="w").pack(fill="x")

                # Display the timestamp
                timestamp_str = report.get('timestamp', 'N/A')
                try:
                    dt_obj = datetime.fromisoformat(timestamp_str)
                    formatted_time = dt_obj.strftime("%Y-%m-%d %H:%M")
                    time_text = f"Reported on: {formatted_time}"
                except (ValueError, TypeError):
                    time_text = f"Reported on: {timestamp_str}"
                tk.Label(issue_frame, text=time_text, bg="#f9f9f9", anchor="w").pack(fill="x")

    def refresh_view_window(self):
        """
        Refreshes the view window if it is open.
        """
        if hasattr(self, 'view_win') and self.view_win and self.view_win.winfo_exists():
            self.draw_view_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    app = CivicEngagementApp(root)
    root.mainloop()
