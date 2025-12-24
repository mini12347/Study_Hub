from datetime import datetime, timedelta

class StudyPlanGenerator:
    def __init__(self):
        self.subjects = []
        self.exam_date = None
        self.study_hours_per_day = 3
        self.completed_goals = set()
        self.progress = {}
        
    def add_subject(self, name, priority, hours_needed):
        subject = {
            'id': len(self.subjects) + 1,
            'name': name,
            'priority': priority,
            'hours_needed': hours_needed,
            'hours_completed': 0
        }
        self.subjects.append(subject)
        self.progress[name] = 0
        
    def set_exam_date(self, exam_date_str):
        self.exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d')
        
    def days_until_exam(self):
        if not self.exam_date:
            return None
        today = datetime.now()
        delta = self.exam_date - today
        return max(0, delta.days)
    
    def get_priority_weight(self, priority):
        weights = {'high': 3, 'medium': 2, 'low': 1}
        return weights.get(priority, 2)
    
    def calculate_daily_hours(self, subject):
        days_left = self.days_until_exam()
        if not days_left or days_left == 0:
            return 0
        
        hours_remaining = subject['hours_needed'] - subject['hours_completed']
        weight = self.get_priority_weight(subject['priority'])
        total_weight = sum(self.get_priority_weight(s['priority']) for s in self.subjects)
        
        allocated_hours = (self.study_hours_per_day * weight / total_weight) if total_weight > 0 else 0
        return min(allocated_hours, hours_remaining / days_left)
    
    def generate_daily_goals(self):
        today = datetime.now()
        goals = []
        
        for subject in self.subjects:
            daily_hours = self.calculate_daily_hours(subject)
            if daily_hours > 0:
                goal = {
                    'id': f"{subject['id']}-{today.strftime('%Y%m%d')}",
                    'subject': subject['name'],
                    'hours': round(daily_hours, 1),
                    'tasks': self.generate_tasks(subject, daily_hours),
                    'date': today.strftime('%Y-%m-%d'),
                    'completed': False
                }
                goals.append(goal)
        
        return goals
    
    def generate_tasks(self, subject, hours):
        tasks = []
        if hours >= 2:
            tasks = [
                f"Study {subject['name']} theory (1 hour)",
                f"Practice {subject['name']} problems (1 hour)"
            ]
        elif hours >= 1:
            tasks = [f"Study {subject['name']} key concepts ({hours} hour)"]
        else:
            tasks = [f"Quick review of {subject['name']} ({int(hours*60)} min)"]
        return tasks
    
    def generate_weekly_review(self):
        today = datetime.now()
        review_plan = []
        
        for i in range(7):
            day = today + timedelta(days=i)
            day_name = day.strftime('%A')
            
            if day_name in ['Saturday', 'Sunday']:
                review_plan.append({
                    'day': day_name,
                    'date': day.strftime('%Y-%m-%d'),
                    'activity': 'Complete practice tests and review weak areas',
                    'focus': 'All subjects'
                })
            else:
                subjects_for_day = [s['name'] for s in self.subjects[i % len(self.subjects):i % len(self.subjects) + 2]] if self.subjects else []
                review_plan.append({
                    'day': day_name,
                    'date': day.strftime('%Y-%m-%d'),
                    'activity': 'Daily study sessions',
                    'focus': ', '.join(subjects_for_day) if subjects_for_day else 'No subjects'
                })
        
        return review_plan
    
    def mark_goal_complete(self, goal_id):
        self.completed_goals.add(goal_id)
        for subject in self.subjects:
            if str(subject['id']) in goal_id:
                subject['hours_completed'] += 0.5
                self.progress[subject['name']] = (subject['hours_completed'] / subject['hours_needed']) * 100
    
    def get_progress_summary(self):
        summary = []
        for subject in self.subjects:
            completion = (subject['hours_completed'] / subject['hours_needed']) * 100
            summary.append({
                'subject': subject['name'],
                'completion': round(completion, 1),
                'hours_completed': subject['hours_completed'],
                'hours_total': subject['hours_needed']
            })
        return summary
    
    def display_study_plan(self):
        print("\n" + "="*60)
        print("SMART STUDY PLAN GENERATOR")
        print("="*60)
        
        days_left = self.days_until_exam()
        if days_left is not None:
            print(f"\n📅 EXAM COUNTDOWN: {days_left} days remaining")
            print(f"   Exam Date: {self.exam_date.strftime('%B %d, %Y')}")
        
        print(f"\n⏰ Daily Study Time: {self.study_hours_per_day} hours")
        
        print("\n" + "-"*60)
        print("📚 SUBJECTS")
        print("-"*60)
        for subject in self.subjects:
            print(f"  • {subject['name']} - Priority: {subject['priority'].upper()}")
            print(f"    Hours needed: {subject['hours_needed']}h | Completed: {subject['hours_completed']}h")
        
        print("\n" + "-"*60)
        print("🎯 TODAY'S STUDY GOALS")
        print("-"*60)
        daily_goals = self.generate_daily_goals()
        for goal in daily_goals:
            status = "✓" if goal['id'] in self.completed_goals else "○"
            print(f"\n  {status} {goal['subject']} ({goal['hours']}h)")
            for task in goal['tasks']:
                print(f"     - {task}")
        
        print("\n" + "-"*60)
        print("📅 WEEKLY REVIEW PLAN")
        print("-"*60)
        weekly_plan = self.generate_weekly_review()
        for day in weekly_plan:
            print(f"\n  {day['day']} ({day['date']})")
            print(f"    Activity: {day['activity']}")
            print(f"    Focus: {day['focus']}")
        
        print("\n" + "-"*60)
        print("📊 PROGRESS SUMMARY")
        print("-"*60)
        progress = self.get_progress_summary()
        for item in progress:
            bar_length = int(item['completion'] / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  {item['subject']}")
            print(f"    [{bar}] {item['completion']}%")
            print(f"    {item['hours_completed']}/{item['hours_total']} hours")
        
        print("\n" + "="*60)


