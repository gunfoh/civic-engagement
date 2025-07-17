import tkinter as tk
from tkinter import messagebox, ttk
import tkintermapview
from datetime import datetime
import data_manager
import math

class CivicEngagementApp:
    #gui class
    def __init__(self, root):
        #init
        self.database = data_manager.load_data()

        self.root = root
        self.root.title("Civic Engagement Platform")
        self.root.geometry("500x400")
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
            "font": ("Helvetica", 12), "fg": "white",
            "activeforeground": "white", "relief": "flat", 
            "borderwidth": 0, "width": 25, "pady": 10
        }
        
        
        blue_normal = "#007BFF"
        blue_hover = "#3395FF"
        teal_normal = "#17a2b8"
        teal_hover = "#20c9e0"
        red_normal = "#dc3545"
        red_hover = "#e45765"

        # report
        report_button = tk.Button(main_frame, text="Report a New Issue", command=self.open_report_window, 
                                   bg=blue_normal, activebackground=blue_normal, **button_style)
        report_button.pack(pady=8)
        report_button.bind("<Enter>", lambda e: self.animate_color(report_button, blue_normal, blue_hover))
        report_button.bind("<Leave>", lambda e: self.animate_color(report_button, blue_hover, blue_normal))

        #view
        view_button = tk.Button(main_frame, text="View All Reported Issues", command=self.open_view_window, 
                                 bg=blue_normal, activebackground=blue_normal, **button_style)
        view_button.pack(pady=8)
        view_button.bind("<Enter>", lambda e: self.animate_color(view_button, blue_normal, blue_hover))
        view_button.bind("<Leave>", lambda e: self.animate_color(view_button, blue_hover, blue_normal))
        
        #heatmap start
        heatmap_button = tk.Button(main_frame, text="View Issue Heatmap", command=self.open_heatmap_window, 
                                   bg=teal_normal, activebackground=teal_normal, **button_style)
        heatmap_button.pack(pady=8)
        heatmap_button.bind("<Enter>", lambda e: self.animate_color(heatmap_button, teal_normal, teal_hover))
        heatmap_button.bind("<Leave>", lambda e: self.animate_color(heatmap_button, teal_hover, teal_normal))

        
        exit_button = tk.Button(main_frame, text="Exit", command=self.root.quit, 
                                bg=red_normal, activebackground=red_normal, **button_style)
        exit_button.pack(pady=8)
        exit_button.bind("<Enter>", lambda e: self.animate_color(exit_button, red_normal, red_hover))
        exit_button.bind("<Leave>", lambda e: self.animate_color(exit_button, red_hover, red_normal))

    def animate_color(self, widget, from_hex, to_hex, steps=15):
        
        from_rgb = tuple(int(from_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        to_rgb = tuple(int(to_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        def update_step(step):
            if step > steps:
                widget.config(bg=to_hex, activebackground=to_hex)
                return

            new_rgb = [int(from_rgb[i] + (to_rgb[i] - from_rgb[i]) * (step / steps)) for i in range(3)]
            new_hex = f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
            
            try:
                widget.config(bg=new_hex, activebackground=new_hex)
                self.root.after(10, lambda: update_step(step + 1))
            except tk.TclError:
                
                pass
            
        update_step(1)

    def open_report_window(self):
        
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
        
        if hasattr(self, 'view_win') and self.view_win and self.view_win.winfo_exists():
            self.draw_view_widgets()

    def open_heatmap_window(self):
        
        heatmap_win = tk.Toplevel(self.root)
        heatmap_win.title("Issue Heatmap - Deepdale")
        heatmap_win.geometry("800x600")

        map_widget = tkintermapview.TkinterMapView(heatmap_win, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(53.765, -2.685) # deepdale
        map_widget.set_zoom(15)

        self.draw_heatmap_clusters(map_widget)

    def draw_heatmap_clusters(self, map_widget):
        
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
            
            map_widget.set_marker(
                center_coords[0], 
                center_coords[1], 
                text=marker_text,
                command=lambda _, reports=cluster['reports']: self.show_cluster_details(reports)
            )

    def show_cluster_details(self, reports):
        
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
        
        text_widget.config(state="disabled") #vulnerability fix, makes read only
