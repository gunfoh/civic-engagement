import tkinter as tk
from tkinter import messagebox, ttk
import tkintermapview
from datetime import datetime
import data_manager
import math

class CivicEngagementApp:
    """
    The main GUI class for the Civic Engagement Platform.
    Handles all UI elements and user interactions.
    """
    def __init__(self, root):
        """
        Initializes the main application window.
        Args:
            root: The root tkinter window.
        """
        self.database = data_manager.load_data()

        self.root = root
        self.root.title("Civic Engagement Platform")
        self.root.geometry("500x400") # Increased height for new button
        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both")

        title_label = tk.Label(
            main_frame,
            text="Welcome to the Civic Engagement Platform",
            font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333"
        )
        title_label.pack(pady=(10, 20))

        button_style = {
            "font": ("Helvetica", 12), "bg": "#007BFF", "fg": "white",
            "activebackground": "#0056b3", "activeforeground": "white",
            "relief": "flat", "borderwidth": 0, "width": 25, "pady": 10
        }

        tk.Button(main_frame, text="Report a New Issue", command=self.open_report_window, **button_style).pack(pady=8)
        tk.Button(main_frame, text="View All Reported Issues", command=self.open_view_window, **button_style).pack(pady=8)
        
        # --- New Heatmap Button ---
        heatmap_button_style = button_style.copy()
        heatmap_button_style['bg'] = "#17a2b8"
        heatmap_button_style['activebackground'] = "#138496"
        tk.Button(main_frame, text="View Issue Heatmap", command=self.open_heatmap_window, **heatmap_button_style).pack(pady=8)

        exit_button_style = button_style.copy()
        exit_button_style['bg'] = "#dc3545"
        exit_button_style['activebackground'] = "#c82333"
        tk.Button(main_frame, text="Exit", command=self.root.quit, **exit_button_style).pack(pady=8)

    def open_report_window(self):
        """Opens a new window with a map for reporting an issue."""
        report_win = tk.Toplevel(self.root)
        report_win.title("Report a New Issue")
        report_win.geometry("600x750")
        report_win.configure(bg="#f0f0f0")

        frame = tk.Frame(report_win, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Type of Issue:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        issue_types = ["Pothole", "Broken Streetlight", "Trash/Litter", "Graffiti", "Public Transportation", "Other"]
        issue_type_var = tk.StringVar(value=issue_types[0])
        ttk.Combobox(frame, textvariable=issue_type_var, values=issue_types, state="readonly").pack(fill="x", pady=(5, 10))

        tk.Label(frame, text="Description:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        description_entry = tk.Entry(frame, font=("Helvetica", 11), width=40)
        description_entry.pack(fill="x", pady=(5, 10))

        time_frame = tk.Frame(frame, bg="#f0f0f0")
        time_frame.pack(fill="x", pady=(10, 0), anchor="w")
        
        use_current_time_var = tk.BooleanVar(value=True)
        time_entry = tk.Entry(time_frame, font=("Helvetica", 11), width=40)

        def toggle_time_entry():
            time_entry.config(state="disabled" if use_current_time_var.get() else "normal")

        tk.Label(time_frame, text="Time of Issue:", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w")
        tk.Checkbutton(time_frame, text="Use current time", variable=use_current_time_var, command=toggle_time_entry, bg="#f0f0f0", activebackground="#f0f0f0").pack(anchor="w")
        tk.Label(time_frame, text="Or enter manually (e.g., YYYY-MM-DD HH:MM):", font=("Helvetica", 9), bg="#f0f0f0").pack(anchor="w", pady=(5,0))
        time_entry.pack(fill="x", pady=(5, 10))
        toggle_time_entry()

        tk.Label(frame, text="Location (Right-click on map to set):", font=("Helvetica", 11), bg="#f0f0f0").pack(anchor="w", pady=(10,5))
        map_widget = tkintermapview.TkinterMapView(frame, width=560, height=300, corner_radius=5)
        map_widget.pack(fill="both", expand=True)

        deepdale_lat, deepdale_lon = 53.765, -2.685
        map_widget.set_position(deepdale_lat, deepdale_lon)
        map_widget.set_zoom(15)
        marker = map_widget.set_marker(deepdale_lat, deepdale_lon, text="Issue Location")

        map_widget.add_right_click_menu_command(label="Set Issue Location", command=lambda coords: marker.set_position(coords[0], coords[1]), pass_coords=True)

        def submit_issue():
            if not description_entry.get():
                messagebox.showerror("Error", "Please provide a description.", parent=report_win)
                return

            issue_report = {
                "type": issue_type_var.get(),
                "description": description_entry.get(),
                "location": marker.position,
                "timestamp": datetime.now().isoformat() if use_current_time_var.get() else time_entry.get(),
                "status": "Reported"
            }
            self.database.append(issue_report)
            data_manager.save_data(self.database)
            
            messagebox.showinfo("Success", "Issue reported successfully!", parent=report_win)
            self.refresh_view_window()
            report_win.destroy()

        tk.Button(frame, text="Submit Report", command=submit_issue, bg="#28a745", fg="white", font=("Helvetica", 12), relief="flat").pack(pady=20)

    def open_view_window(self):
        """Opens a new window to display all reported issues."""
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
        """Draws or redraws the content of the view window."""
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
                loc_text = f"Location (Lat/Lon): {location[0]:.5f}, {location[1]:.5f}" if isinstance(location, (list, tuple)) else f"Location: {location}"
                tk.Label(issue_frame, text=loc_text, bg="#f9f9f9", anchor="w").pack(fill="x")

                timestamp_str = report.get('timestamp', 'N/A')
                try:
                    time_text = f"Reported on: {datetime.fromisoformat(timestamp_str).strftime('%Y-%m-%d %H:%M')}"
                except (ValueError, TypeError):
                    time_text = f"Reported on: {timestamp_str}"
                tk.Label(issue_frame, text=time_text, bg="#f9f9f9", anchor="w").pack(fill="x")

    def refresh_view_window(self):
        """Refreshes the view window if it is open."""
        if hasattr(self, 'view_win') and self.view_win and self.view_win.winfo_exists():
            self.draw_view_widgets()

    def open_heatmap_window(self):
        """Opens a new window to display a heatmap of issue clusters."""
        heatmap_win = tk.Toplevel(self.root)
        heatmap_win.title("Issue Heatmap - Deepdale")
        heatmap_win.geometry("800x600")

        map_widget = tkintermapview.TkinterMapView(heatmap_win, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(53.765, -2.685) # Deepdale
        map_widget.set_zoom(15)

        self.draw_heatmap_clusters(map_widget)

    def draw_heatmap_clusters(self, map_widget):
        """Calculates and draws issue clusters on the map."""
        reports_with_coords = [r for r in self.database if isinstance(r.get('location'), (list, tuple))]
        
        clusters = []
        CLUSTER_THRESHOLD = 0.0005 

        for report in reports_with_coords:
            placed = False
            for cluster in clusters:
                center_lat, center_lon = cluster['center']
                report_lat, report_lon = report['location']
                distance = math.sqrt((center_lat - report_lat)**2 + (center_lon - report_lon)**2)

                if distance < CLUSTER_THRESHOLD:
                    cluster['reports'].append(report)
                    cluster['center'] = (
                        (center_lat * (len(cluster['reports'])-1) + report_lat) / len(cluster['reports']),
                        (center_lon * (len(cluster['reports'])-1) + report_lon) / len(cluster['reports'])
                    )
                    placed = True
                    break
            if not placed:
                clusters.append({'center': report['location'], 'reports': [report]})

        for cluster in clusters:
            num_reports = len(cluster['reports'])
            center_coords = cluster['center']
            marker_text = f"{num_reports} Report" + ("s" if num_reports > 1 else "")
            
            # --- FIX ---
            # The command function from the library passes the marker object as an argument.
            # We create a lambda that accepts this argument (which we name '_' to show it's ignored)
            # and then calls our function with the 'reports' list that was correctly captured
            # from the loop by setting it as a default argument in the lambda.
            map_widget.set_marker(
                center_coords[0], 
                center_coords[1], 
                text=marker_text,
                command=lambda _, reports=cluster['reports']: self.show_cluster_details(reports)
            )

    def show_cluster_details(self, reports):
        """Shows the details of all reports in a clicked cluster."""
        details_win = tk.Toplevel(self.root)
        details_win.title("Cluster Details")
        details_win.geometry("500x300")

        text_widget = tk.Text(details_win, wrap="word", font=("Helvetica", 10), padx=10, pady=10)
        text_widget.pack(expand=True, fill="both")

        for i, report in enumerate(reports, 1):
            text_widget.insert(tk.END, f"--- Report {i} ---\n")
            text_widget.insert(tk.END, f"Type: {report.get('type', 'N/A')}\n")
            text_widget.insert(tk.END, f"Description: {report.get('description', 'N/A')}\n")
            
            timestamp_str = report.get('timestamp', 'N/A')
            try:
                time_text = f"Time: {datetime.fromisoformat(timestamp_str).strftime('%Y-%m-%d %H:%M')}\n\n"
            except (ValueError, TypeError):
                time_text = f"Time: {timestamp_str}\n\n"
            text_widget.insert(tk.END, time_text)
        
        text_widget.config(state="disabled") # Make it read-only
