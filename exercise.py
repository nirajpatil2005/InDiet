import pandas as pd
class ExerciseRecommender:
    def __init__(self):
        self.exercises = {
            "Chest": [
                {"Exercise Name": "Push-ups", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 167},
                {"Exercise Name": "Bench Press", "Sets": 4, "Reps": "8-10", "Rest Period (seconds)": 90, "Calories Burned (30 mins)": 200},
                {"Exercise Name": "Incline Dumbbell Press", "Sets": 3, "Reps": "10-12", "Rest Period (seconds)": 75, "Calories Burned (30 mins)": 180},
                {"Exercise Name": "Chest Fly", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 150}
            ],
            "Core": [
                {"Exercise Name": "Plank", "Sets": 3, "Reps": "30-60 sec", "Rest Period (seconds)": 45, "Calories Burned (30 mins)": 120},
                {"Exercise Name": "Russian Twists", "Sets": 3, "Reps": "20/side", "Rest Period (seconds)": 45, "Calories Burned (30 mins)": 140},
                {"Exercise Name": "Leg Raises", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 130},
                {"Exercise Name": "Bicycle Crunches", "Sets": 3, "Reps": "20/side", "Rest Period (seconds)": 45, "Calories Burned (30 mins)": 150}
            ],
            "Back": [
                {"Exercise Name": "Pull-ups", "Sets": 3, "Reps": "8-10", "Rest Period (seconds)": 90, "Calories Burned (30 mins)": 180},
                {"Exercise Name": "Bent-over Rows", "Sets": 4, "Reps": "10-12", "Rest Period (seconds)": 75, "Calories Burned (30 mins)": 190},
                {"Exercise Name": "Lat Pulldown", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 160},
                {"Exercise Name": "Deadlifts", "Sets": 4, "Reps": "6-8", "Rest Period (seconds)": 120, "Calories Burned (30 mins)": 220}
            ],
            "Arms": [
                {"Exercise Name": "Bicep Curls", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 120},
                {"Exercise Name": "Tricep Dips", "Sets": 3, "Reps": "10-12", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 130},
                {"Exercise Name": "Hammer Curls", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 120},
                {"Exercise Name": "Skull Crushers", "Sets": 3, "Reps": "10-12", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 130}
            ],
            "Legs": [
                {"Exercise Name": "Squats", "Sets": 4, "Reps": "10-12", "Rest Period (seconds)": 90, "Calories Burned (30 mins)": 200},
                {"Exercise Name": "Lunges", "Sets": 3, "Reps": "12/side", "Rest Period (seconds)": 75, "Calories Burned (30 mins)": 180},
                {"Exercise Name": "Leg Press", "Sets": 4, "Reps": "12-15", "Rest Period (seconds)": 75, "Calories Burned (30 mins)": 190},
                {"Exercise Name": "Calf Raises", "Sets": 3, "Reps": "15-20", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 120}
            ],
            "Shoulders": [
                {"Exercise Name": "Overhead Press", "Sets": 4, "Reps": "8-10", "Rest Period (seconds)": 90, "Calories Burned (30 mins)": 170},
                {"Exercise Name": "Lateral Raises", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 130},
                {"Exercise Name": "Front Raises", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 130},
                {"Exercise Name": "Shrugs", "Sets": 3, "Reps": "12-15", "Rest Period (seconds)": 60, "Calories Burned (30 mins)": 140}
            ],
            "Cardio": [
                {"Exercise Name": "Running (6 mph)", "Sets": 1, "Reps": "20-30 min", "Rest Period (seconds)": 0, "Calories Burned (30 mins)": 300},
                {"Exercise Name": "Cycling", "Sets": 1, "Reps": "30 min", "Rest Period (seconds)": 0, "Calories Burned (30 mins)": 250},
                {"Exercise Name": "Jump Rope", "Sets": 1, "Reps": "15-20 min", "Rest Period (seconds)": 0, "Calories Burned (30 mins)": 280},
                {"Exercise Name": "Swimming", "Sets": 1, "Reps": "30 min", "Rest Period (seconds)": 0, "Calories Burned (30 mins)": 270}
            ]
        }
        
        self.weekly_plan = {
            "Monday": ["Chest", "Core"],
            "Tuesday": ["Back", "Arms"],
            "Wednesday": ["Legs", "Shoulders"],
            "Thursday": ["Chest", "Core"],
            "Friday": ["Back", "Arms"],
            "Saturday": ["Legs", "Shoulders"],
            "Sunday": ["Rest/Cardio"]
        }
        
        self.expert_tips = {
            "Chest": "Focus on full range of motion for chest exercises. Squeeze at the top of each rep for maximum contraction.",
            "Core": "Engage your core throughout the day, not just during workouts. Maintain proper form to protect your lower back.",
            "Back": "Pull with your elbows, not your hands. Retract your shoulder blades for proper back engagement.",
            "Arms": "Control the eccentric (lowering) phase. Avoid swinging to isolate the biceps/triceps effectively.",
            "Legs": "Keep your knees aligned with your toes during squats and lunges. Go deep but maintain proper form.",
            "Shoulders": "Don't neglect rear delts. Balance front, side, and rear delt exercises for shoulder health.",
            "Cardio": "Mix HIIT with steady-state cardio. Interval training boosts metabolism more effectively."
        }

    def recommend_full_body_workout(self, equipment, difficulty, calories_burned):
        # This method can be used for general recommendations
        return {
            "Chest": pd.DataFrame(self.exercises["Chest"][:2]),
            "Back": pd.DataFrame(self.exercises["Back"][:2]),
            "Legs": pd.DataFrame(self.exercises["Legs"][:2]),
            "Core": pd.DataFrame(self.exercises["Core"][:2])
        }
    
    def get_weekly_plan(self):
        """Returns the structured weekly workout plan"""
        return self.weekly_plan
    
    def get_day_workout(self, day):
        """Returns workout for specific day with proper error handling"""
        muscle_groups = self.weekly_plan.get(day, [])
        workout = {}
        
        for group in muscle_groups:
            if group == "Rest/Cardio":
                workout["Cardio"] = pd.DataFrame(self.exercises.get("Cardio", []))
            else:
                exercises = self.exercises.get(group, [])
                if exercises:  # Only add if exercises exist
                    workout[group] = pd.DataFrame(exercises)
        
        return workout if workout else {"Rest": pd.DataFrame([{"Note": "Rest day - active recovery recommended"}])}
    
    def get_expert_tips(self, muscle_group):
        """Returns expert tips for specific muscle group"""
        return self.expert_tips.get(muscle_group, "Focus on proper form and controlled movements.")