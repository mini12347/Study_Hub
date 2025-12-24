import time
import os
import json
from datetime import datetime, timedelta
import threading
import random

class PomodoroTimer:
    def __init__(self):
        self.work_duration = 25
        self.short_break = 5
        self.long_break = 15
        self.sessions_until_long_break = 4
        self.current_session = 0
        self.total_sessions = 0
        self.total_focus_time = 0
        self.is_running = False
        self.session_history = []
        self.break_suggestions = [
            "Stretch your arms and legs",
            "Walk around for a few minutes",
            "Drink a glass of water",
            "Look away from screen (20-20-20 rule)",
            "Do some deep breathing exercises",
            "Quick meditation (2-3 minutes)",
            "Light snack - fruits or nuts",
            "Step outside for fresh air",
            "Do 10 jumping jacks",
            "Close your eyes and relax"
        ]
        self.ambient_sounds = [
            "Rain sounds - gentle rainfall",
            "Coffee shop ambiance",
            "Forest birds chirping",
            "Ocean waves crashing",
            "White noise - steady hum",
            "Fireplace crackling",
            "Thunderstorm distant",
            "Piano instrumental"
        ]
        
    def display_banner(self):
        print("\n" + "="*60)
        print("🍅 POMODORO TIMER + FOCUS MODE 🍅")
        print("="*60)
    
    def select_background_music(self):
        print("\n🎵 SELECT BACKGROUND MUSIC:")
        print("-"*60)
        for i, sound in enumerate(self.ambient_sounds, 1):
            print(f"  {i}. {sound}")
        print(f"  {len(self.ambient_sounds) + 1}. Silent mode")
        print("-"*60)
        
        choice = random.randint(1, len(self.ambient_sounds))
        if choice <= len(self.ambient_sounds):
            selected = self.ambient_sounds[choice - 1]
            print(f"\n▶️  Now playing: {selected}")
            return selected
        else:
            print("\n🔇 Silent mode activated")
            return "Silent"
    
    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def countdown(self, duration_minutes, session_type):
        total_seconds = duration_minutes * 60
        
        print(f"\n⏰ {session_type.upper()} - {duration_minutes} minutes")
        print("="*60)
        
        for remaining in range(total_seconds, 0, -1):
            mins = remaining // 60
            secs = remaining % 60
            
            bar_length = 40
            progress = (total_seconds - remaining) / total_seconds
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"\r  [{bar}] {mins:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        
        print("\n" + "="*60)
        print(f"✅ {session_type.upper()} COMPLETED!")
        
    def get_break_suggestion(self):
        return random.choice(self.break_suggestions)
    
    def run_work_session(self):
        self.current_session += 1
        self.total_sessions += 1
        
        print(f"\n🎯 FOCUS SESSION #{self.current_session}")
        
        start_time = datetime.now()
        self.countdown(self.work_duration, "Focus Session")
        end_time = datetime.now()
        
        self.total_focus_time += self.work_duration
        
        session_log = {
            'session_number': self.total_sessions,
            'type': 'work',
            'duration': self.work_duration,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.session_history.append(session_log)
        
    def run_break_session(self):
        if self.current_session % self.sessions_until_long_break == 0:
            break_duration = self.long_break
            break_type = "Long Break"
        else:
            break_duration = self.short_break
            break_type = "Short Break"
        
        print(f"\n☕ {break_type.upper()} TIME!")
        print("-"*60)
        suggestion = self.get_break_suggestion()
        print(f"💡 Suggestion: {suggestion}")
        print("-"*60)
        
        start_time = datetime.now()
        self.countdown(break_duration, break_type)
        end_time = datetime.now()
        
        session_log = {
            'session_number': self.total_sessions,
            'type': break_type.lower().replace(' ', '_'),
            'duration': break_duration,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'suggestion': suggestion
        }
        self.session_history.append(session_log)
    
    def display_productivity_stats(self):
        print("\n" + "="*60)
        print("📊 PRODUCTIVITY STATISTICS")
        print("="*60)
        
        total_work_sessions = sum(1 for s in self.session_history if s['type'] == 'work')
        total_breaks = len(self.session_history) - total_work_sessions
        
        print(f"\n🍅 Total Focus Sessions: {total_work_sessions}")
        print(f"⏱️  Total Focus Time: {self.total_focus_time} minutes ({self.total_focus_time/60:.1f} hours)")
        print(f"☕ Total Breaks Taken: {total_breaks}")
        
        print(f"\n📈 Average Session Length: {self.work_duration} minutes")
        
        if self.total_focus_time >= 120:
            performance = "🔥 Excellent! You're on fire!"
        elif self.total_focus_time >= 60:
            performance = "👍 Great work! Keep it up!"
        elif self.total_focus_time >= 25:
            performance = "✨ Good start! Building momentum!"
        else:
            performance = "🌱 Just getting started!"
        
        print(f"\n{performance}")
        
        print("\n" + "-"*60)
        print("SESSION HISTORY:")
        print("-"*60)
        
        for i, session in enumerate(self.session_history[-10:], 1):
            session_type = session['type'].replace('_', ' ').title()
            duration = session['duration']
            start = session['start_time'].split()[1][:5]
            
            if session['type'] == 'work':
                icon = "🎯"
            elif 'long' in session['type']:
                icon = "🌙"
            else:
                icon = "☕"
            
            print(f"  {icon} {session_type} - {duration}min @ {start}")
    
    def start_pomodoro_cycle(self, num_cycles=4):
        self.display_banner()
        
        music = self.select_background_music()
        
        print(f"\n⚙️  SETTINGS:")
        print(f"   Work Session: {self.work_duration} minutes")
        print(f"   Short Break: {self.short_break} minutes")
        print(f"   Long Break: {self.long_break} minutes")
        print(f"   Cycles: {num_cycles}")
        
        input("\n📢 Press ENTER to start your focus session...")
        
        for cycle in range(num_cycles):
            print(f"\n{'='*60}")
            print(f"🔄 CYCLE {cycle + 1} of {num_cycles}")
            print(f"{'='*60}")
            
            self.run_work_session()
            
            if cycle < num_cycles - 1:
                self.run_break_session()
            
            if cycle == num_cycles - 1:
                print("\n" + "="*60)
                print("🎉 ALL CYCLES COMPLETED! GREAT JOB!")
                print("="*60)
        
        self.display_productivity_stats()
        
        print("\n" + "="*60)
        print("Thank you for using Pomodoro Timer!")
        print("="*60 + "\n")

