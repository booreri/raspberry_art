#!/usr/bin/env python3
"""
Life Countdown Timer Application for Raspberry Pi
A full-screen countdown timer showing life expectancy and themed countdowns
with daily quotes that update at 4 AM.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import threading
import time
import random

class LifeCountdownApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Life Countdown Timer")
        self.root.configure(bg='black')
        
        # Make fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.toggle_fullscreen)
        self.root.bind('<F11>', self.toggle_fullscreen)
        
        # Configuration file
        self.config_file = 'countdown_config.json'
        self.quotes_file = 'daily_quotes.json'
        
        # Load configuration
        self.load_config()
        self.load_quotes()
        
        # Variables for countdown calculations
        self.life_end_date = None
        self.theme_end_date = None
        self.current_quote = ""
        self.last_quote_date = None
        
        # Calculate dates
        self.calculate_dates()
        
        # Setup GUI
        self.setup_gui()
        
        # Start the update loop
        self.update_display()
        
        # Start quote update thread
        self.start_quote_thread()
    
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "birth_date": "1990-01-01",
            "life_expectancy_years": 80,
            "theme_name": "Next Vacation",
            "theme_end_date": "2025-12-31",
            "last_quote_update": "",
            "current_quote": "Anicca|Change, Dukkha|Suffering, Anatta|Non-Self, Sati|Mindfulness, Equanimity|Observation, Sila|Morality, Samadhi|Concentration."
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = default_config
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_quotes(self):
        """Load quotes from JSON file"""
        default_quotes = [
            "Anicca (Impermanence): This is the fundamental teaching that everything is constantly changing, in a perpetual state of flux.",
            "Dukkha (Suffering/Unsatisfactoriness): Often translated as 'suffering,' dukkha encompasses a broader sense of unsatisfactoriness, dis-ease, or inherent instability in conditioned existence.",
            "Anatta (Non-Self): This teaching asserts that there is no permanent, unchanging 'self' or 'soul.'"
        ]
        
        try:
            if os.path.exists(self.quotes_file):
                with open(self.quotes_file, 'r') as f:
                    self.quotes = json.load(f)
            else:
                self.quotes = default_quotes
                with open(self.quotes_file, 'w') as f:
                    json.dump(self.quotes, f, indent=2)
        except Exception as e:
            print(f"Error loading quotes: {e}")
            self.quotes = default_quotes
    
    def calculate_dates(self):
        """Calculate end dates for countdowns"""
        try:
            birth_date = datetime.strptime(self.config['birth_date'], '%Y-%m-%d')
            life_expectancy = self.config['life_expectancy_years']
            self.life_end_date = birth_date + timedelta(days=life_expectancy * 365.25)
            
            self.theme_end_date = datetime.strptime(self.config['theme_end_date'], '%Y-%m-%d')
            
            # Set current quote
            self.current_quote = self.config.get('current_quote', 'Anicca|Change, Dukkha|Suffering, Anatta|Non-Self, Sati|Mindfulness, Equanimity|Observation, Sila|Morality, Samadhi|Concentration.')
            
        except Exception as e:
            print(f"Error calculating dates: {e}")
            # Set default dates if there's an error
            self.life_end_date = datetime.now() + timedelta(days=365 * 30)  # 30 years default
            self.theme_end_date = datetime.now() + timedelta(days=365)  # 1 year default
    
    def setup_gui(self):
        """Setup the GUI elements"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="⏰ LIFE COUNTDOWN ⏰", 
                              font=('Arial', 24, 'bold'), 
                              fg='red', bg='black')
        title_label.pack(pady=(0, 30))
        
        # Life countdown section
        life_frame = tk.Frame(main_frame, bg='black', relief='raised', bd=2)
        life_frame.pack(fill='x', pady=10)
        
        tk.Label(life_frame, text="⚰️ LIFE EXPECTANCY COUNTDOWN ⚰️", 
                font=('Arial', 18, 'bold'), fg='red', bg='black').pack(pady=10)
        
        self.life_countdown_label = tk.Label(life_frame, text="Loading...", 
                                           font=('Courier', 16, 'bold'), 
                                           fg='red', bg='black')
        self.life_countdown_label.pack(pady=10)
        
        # Theme countdown section
        theme_frame = tk.Frame(main_frame, bg='black', relief='raised', bd=2)
        theme_frame.pack(fill='x', pady=10)
        
        self.theme_title_label = tk.Label(theme_frame, text="", 
                                         font=('Arial', 18, 'bold'), 
                                         fg='cyan', bg='black')
        self.theme_title_label.pack(pady=10)
        
        self.theme_countdown_label = tk.Label(theme_frame, text="Loading...", 
                                            font=('Courier', 16, 'bold'), 
                                            fg='cyan', bg='black')
        self.theme_countdown_label.pack(pady=10)
        
        # Quote section
        quote_frame = tk.Frame(main_frame, bg='black', relief='raised', bd=2)
        quote_frame.pack(fill='x', pady=10)
        
        tk.Label(quote_frame, text="💭 DAILY INSPIRATION 💭", 
                font=('Arial', 16, 'bold'), fg='yellow', bg='black').pack(pady=10)
        
        self.quote_label = tk.Label(quote_frame, text="", 
                                   font=('Arial', 14, 'italic'), 
                                   fg='yellow', bg='black', wraplength=800)
        self.quote_label.pack(pady=10)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(side='bottom', pady=20)
        
        # Settings button
        settings_btn = tk.Button(button_frame, text="⚙️ Settings", 
                               command=self.open_settings,
                               font=('Arial', 12), bg='gray', fg='white')
        settings_btn.pack(side='left', padx=10)
        
        # Exit button
        exit_btn = tk.Button(button_frame, text="❌ Exit", 
                           command=self.root.quit,
                           font=('Arial', 12), bg='darkred', fg='white')
        exit_btn.pack(side='right', padx=10)
    
    def format_countdown(self, target_date):
        """Format countdown to show years, days, hours, minutes, seconds"""
        now = datetime.now()
        if target_date <= now:
            return "⚠️ TIME'S UP! ⚠️"
        
        diff = target_date - now
        
        # Calculate years, days, hours, minutes, seconds
        years = diff.days // 365
        remaining_days = diff.days % 365
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60
        
        if years > 0:
            return f"{years}Y {remaining_days}D {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{remaining_days}D {hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update_display(self):
        """Update the countdown displays"""
        if self.life_end_date:
            life_countdown = self.format_countdown(self.life_end_date)
            self.life_countdown_label.config(text=life_countdown)
        
        if self.theme_end_date:
            theme_countdown = self.format_countdown(self.theme_end_date)
            self.theme_countdown_label.config(text=theme_countdown)
            
            # Update theme title
            theme_title = f"🎯 {self.config['theme_name'].upper()} COUNTDOWN 🎯"
            self.theme_title_label.config(text=theme_title)
        
        # Update quote
        self.quote_label.config(text=f'"{self.current_quote}"')
        
        # Schedule next update in 1 second
        self.root.after(1000, self.update_display)
    
    def start_quote_thread(self):
        """Start the thread that checks for quote updates at 4 AM"""
        def quote_updater():
            while True:
                now = datetime.now()
                if now.hour == 4 and now.minute == 0:
                    # Check if we haven't updated today
                    today_str = now.strftime('%Y-%m-%d')
                    if self.config.get('last_quote_update') != today_str:
                        self.update_daily_quote()
                        self.config['last_quote_update'] = today_str
                        self.save_config()
                
                # Sleep for 60 seconds before checking again
                time.sleep(60)
        
        quote_thread = threading.Thread(target=quote_updater, daemon=True)
        quote_thread.start()
    
    def update_daily_quote(self):
        """Update to a new random quote"""
        if self.quotes:
            new_quote = random.choice(self.quotes)
            # Make sure it's different from current quote if possible
            attempts = 0
            while new_quote == self.current_quote and len(self.quotes) > 1 and attempts < 5:
                new_quote = random.choice(self.quotes)
                attempts += 1
            
            self.current_quote = new_quote
            self.config['current_quote'] = new_quote
            self.save_config()
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.configure(bg='black')
        settings_window.grab_set()  # Make modal
        
        # Birth date
        tk.Label(settings_window, text="Birth Date (YYYY-MM-DD):", 
                fg='white', bg='black').pack(pady=5)
        birth_entry = tk.Entry(settings_window)
        birth_entry.insert(0, self.config['birth_date'])
        birth_entry.pack(pady=5)
        
        # Life expectancy
        tk.Label(settings_window, text="Life Expectancy (years):", 
                fg='white', bg='black').pack(pady=5)
        life_exp_entry = tk.Entry(settings_window)
        life_exp_entry.insert(0, str(self.config['life_expectancy_years']))
        life_exp_entry.pack(pady=5)
        
        # Theme name
        tk.Label(settings_window, text="Theme Name:", 
                fg='white', bg='black').pack(pady=5)
        theme_name_entry = tk.Entry(settings_window)
        theme_name_entry.insert(0, self.config['theme_name'])
        theme_name_entry.pack(pady=5)
        
        # Theme end date
        tk.Label(settings_window, text="Theme End Date (YYYY-MM-DD):", 
                fg='white', bg='black').pack(pady=5)
        theme_date_entry = tk.Entry(settings_window)
        theme_date_entry.insert(0, self.config['theme_end_date'])
        theme_date_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(settings_window, bg='black')
        button_frame.pack(pady=20)
        
        def save_settings():
            try:
                self.config['birth_date'] = birth_entry.get()
                self.config['life_expectancy_years'] = int(life_exp_entry.get())
                self.config['theme_name'] = theme_name_entry.get()
                self.config['theme_end_date'] = theme_date_entry.get()
                
                self.save_config()
                self.calculate_dates()
                settings_window.destroy()
                messagebox.showinfo("Success", "Settings saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error saving settings: {e}")
        
        tk.Button(button_frame, text="Save", command=save_settings,
                 bg='green', fg='white').pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=settings_window.destroy,
                 bg='red', fg='white').pack(side='right', padx=10)
        
        # New quote button
        tk.Button(settings_window, text="Get New Quote Now", 
                 command=self.update_daily_quote,
                 bg='blue', fg='white').pack(pady=10)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LifeCountdownApp()
    app.run()