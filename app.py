import streamlit as st
from diet import load_data, calculate_bmi, calculate_bmr, calculate_daily_calories, recommend_diet, show_3d_visualization
from exercise import ExerciseRecommender
import pandas as pd
import plotly.express as px

# Streamlit UI Configuration
st.set_page_config(page_title="🍽️ Personalized Diet & Exercise Plan", page_icon="🏋️", layout="wide")

# Language translations
translations = {
    "english": {
        "title": "🍽️ Personalized Diet & Exercise Plan",
        "instructions": "Fill in your details to generate a personalized meal and exercise plan.",
        "personal_info": "👤 Personal Information",
        "age": "Enter Your Age",
        "gender": "Gender",
        "weight": "Enter Your Weight (kg)",
        "height": "Enter Your Height (cm)",
        "activity": "Activity Level",
        "goals": "🎯 Goals & Preferences",
        "goal_select": "Select Your Goal",
        "food_pref": "Food Preference",
        "region_pref": "Preferred Region",
        "allergies": "Allergies/Dietary Restrictions",
        "calorie_intake": "🔥 Calorie Intake (Optional)",
        "use_calculated": "Use calculated recommended calories",
        "enter_calories": "Enter Daily Calorie Intake (kcal)",
        "nutrient_weight": "⚖️ Nutrient Weightage",
        "nutrient_score": "Importance of Nutrient Score",
        "health_score": "Importance of Health Score",
        "diversity_score": "Importance of Diversity Score",
        "protein_ratio": "Importance of Protein Ratio",
        "generate": "✨ Generate Plans",
        "how_it_works": "How it works:",
        "step1": "Fill in your personal details in the sidebar",
        "step2": "Set your goals and preferences",
        "step3": "Click 'Generate Plans' to get your customized recommendations",
        "health_metrics": "📊 Your Health Metrics",
        "bmi": "BMI",
        "underweight": "Underweight: Consider increasing calories",
        "normal": "Normal Weight: Good job!",
        "overweight": "Overweight: Consider reducing calories",
        "obese": "Obese: Significant calorie reduction recommended",
        "recommended_calories": "Recommended Calories",
        "your_intake": "Your Calorie Intake",
        "lower": "Your intake is lower than recommended",
        "higher": "Your intake is higher than recommended",
        "aligns": "Your intake aligns with recommendations",
        "meal_plan": "🍽️ Your Personalized Meal Plan",
        "daily_meals": "Your Daily Meals",
        "nutrient_intake": "📊 Daily Nutrient Intake Breakdown",
        "macronutrient": "🥗 Macronutrient Distribution",
        "food_recommendation": "🔍 Food Recommendation Space",
        "exercise_plan": "🏋️ Your Personalized Exercise Plan",
        "full_body": "Full-Body Workout Plan",
        "exercise_tips": "Exercise Tips",
        "weight_loss_tips": "- Focus on cardio exercises (30-60 mins per session)\n- Incorporate HIIT workouts 2-3 times per week\n- Strength training helps maintain muscle while losing fat",
        "muscle_gain_tips": "- Prioritize strength training (3-5 times per week)\n- Focus on progressive overload\n- Allow adequate rest between workouts",
        "maintenance_tips": "- Balance between cardio and strength training\n- Try different activities to prevent boredom\n- Listen to your body and adjust as needed",
        "download_meal": "📥 Download Meal Plan",
        "fill_details": "👈 Fill in your details in the sidebar and click 'Generate Plans' to get started"
    },
    "hindi": {
        "title": "🍽️ व्यक्तिगत आहार और व्यायाम योजना",
        "instructions": "अपना व्यक्तिगत भोजन और व्यायाम योजना प्राप्त करने के लिए अपने विवरण भरें।",
        "personal_info": "👤 व्यक्तिगत जानकारी",
        "age": "अपनी आयु दर्ज करें",
        "gender": "लिंग",
        "weight": "अपना वजन दर्ज करें (किलो)",
        "height": "अपनी ऊंचाई दर्ज करें (सेमी)",
        "activity": "गतिविधि स्तर",
        "goals": "🎯 लक्ष्य और प्राथमिकताएं",
        "goal_select": "अपना लक्ष्य चुनें",
        "food_pref": "भोजन प्राथमिकता",
        "region_pref": "पसंदीदा क्षेत्र",
        "allergies": "एलर्जी/आहार प्रतिबंध",
        "calorie_intake": "🔥 कैलोरी सेवन (वैकल्पिक)",
        "use_calculated": "गणना की गई अनुशंसित कैलोरी का उपयोग करें",
        "enter_calories": "दैनिक कैलोरी सेवन दर्ज करें (किलोकैलोरी)",
        "nutrient_weight": "⚖️ पोषक तत्व वजन",
        "nutrient_score": "पोषक तत्व स्कोर का महत्व",
        "health_score": "स्वास्थ्य स्कोर का महत्व",
        "diversity_score": "विविधता स्कोर का महत्व",
        "protein_ratio": "प्रोटीन अनुपात का महत्व",
        "generate": "✨ योजना बनाएं",
        "how_it_works": "यह कैसे काम करता है:",
        "step1": "साइडबार में अपनी व्यक्तिगत जानकारी भरें",
        "step2": "अपने लक्ष्य और प्राथमिकताएं निर्धारित करें",
        "step3": "अनुकूलित सिफारिशें प्राप्त करने के लिए 'योजना बनाएं' पर क्लिक करें",
        "health_metrics": "📊 आपके स्वास्थ्य मेट्रिक्स",
        "bmi": "बीएमआई",
        "underweight": "कम वजन: कैलोरी बढ़ाने पर विचार करें",
        "normal": "सामान्य वजन: अच्छा काम!",
        "overweight": "अधिक वजन: कैलोरी कम करने पर विचार करें",
        "obese": "मोटापा: कैलोरी में महत्वपूर्ण कमी की सिफारिश की गई",
        "recommended_calories": "अनुशंसित कैलोरी",
        "your_intake": "आपका कैलोरी सेवन",
        "lower": "आपका सेवन अनुशंसित से कम है",
        "higher": "आपका सेवन अनुशंसित से अधिक है",
        "aligns": "आपका सेवन सिफारिशों के अनुरूप है",
        "meal_plan": "🍽️ आपकी व्यक्तिगत भोजन योजना",
        "daily_meals": "आपके दैनिक भोजन",
        "nutrient_intake": "📊 दैनिक पोषक तत्व सेवन विवरण",
        "macronutrient": "🥗 मैक्रोन्यूट्रिएंट वितरण",
        "food_recommendation": "🔍 भोजन सिफारिश स्थान",
        "exercise_plan": "🏋️ आपकी व्यक्तिगत व्यायाम योजना",
        "full_body": "पूर्ण-शरीर वर्कआउट योजना",
        "exercise_tips": "व्यायाम सुझाव",
        "weight_loss_tips": "- कार्डियो व्यायाम पर ध्यान दें (30-60 मिनट प्रति सत्र)\n- सप्ताह में 2-3 बार HIIT वर्कआउट शामिल करें\n- मांसपेशियों को बनाए रखने के लिए स्ट्रेंथ ट्रेनिंग",
        "muscle_gain_tips": "- स्ट्रेंथ ट्रेनिंग को प्राथमिकता दें (सप्ताह में 3-5 बार)\n- प्रोग्रेसिव ओवरलोड पर ध्यान दें\n- वर्कआउट्स के बीच पर्याप्त आराम दें",
        "maintenance_tips": "- कार्डियो और स्ट्रेंथ ट्रेनिंग के बीच संतुलन बनाएं\n- ऊब से बचने के लिए विभिन्न गतिविधियों को आजमाएं\n- अपने शरीर की सुनें और आवश्यकतानुसार समायोजित करें",
        "download_meal": "📥 भोजन योजना डाउनलोड करें",
        "fill_details": "👈 शुरू करने के लिए साइडबार में अपना विवरण भरें और 'योजना बनाएं' पर क्लिक करें"
    },
    "marathi": {
        "title": "🍽️ वैयक्तिक आहार आणि व्यायाम योजना",
        "instructions": "तुमची वैयक्तिक आहार आणि व्यायाम योजना मिळविण्यासाठी तुमचे तपशील भरा.",
        "personal_info": "👤 वैयक्तिक माहिती",
        "age": "तुमचे वय प्रविष्ट करा",
        "gender": "लिंग",
        "weight": "तुमचे वजन प्रविष्ट करा (किलो)",
        "height": "तुमची उंची प्रविष्ट करा (सेमी)",
        "activity": "क्रियाकलाप स्तर",
        "goals": "🎯 उद्दिष्टे आणि प्राधान्ये",
        "goal_select": "तुमचे उद्दिष्ट निवडा",
        "food_pref": "अन्न प्राधान्य",
        "region_pref": "पसंतीचे प्रदेश",
        "allergies": "ॲलर्जी/आहार निर्बंध",
        "calorie_intake": "🔥 कॅलरी सेवन (पर्यायी)",
        "use_calculated": "गणना केलेल्या शिफारस केलेल्या कॅलरी वापरा",
        "enter_calories": "दैनंदिन कॅलरी सेवन प्रविष्ट करा (किलोकॅलरी)",
        "nutrient_weight": "⚖️ पोषक घटक वजन",
        "nutrient_score": "पोषक घटक स्कोरचे महत्त्व",
        "health_score": "आरोग्य स्कोरचे महत्त्व",
        "diversity_score": "विविधता स्कोरचे महत्त्व",
        "protein_ratio": "प्रथिने गुणोत्तराचे महत्त्व",
        "generate": "✨ योजना तयार करा",
        "how_it_works": "हे कसे कार्य करते:",
        "step1": "साइडबारमध्ये तुमचे वैयक्तिक तपशील भरा",
        "step2": "तुमची उद्दिष्टे आणि प्राधान्ये सेट करा",
        "step3": "सानुकूलित शिफारसी मिळविण्यासाठी 'योजना तयार करा' वर क्लिक करा",
        "health_metrics": "📊 तुमचे आरोग्य मेट्रिक्स",
        "bmi": "BMI",
        "underweight": "कमी वजन: कॅलरी वाढविण्याचा विचार करा",
        "normal": "सामान्य वजन: चांगले काम!",
        "overweight": "अधिक वजन: कॅलरी कमी करण्याचा विचार करा",
        "obese": "स्थूलता: कॅलरीमध्ये लक्षणीय घट करण्याची शिफारस",
        "recommended_calories": "शिफारस केलेल्या कॅलरी",
        "your_intake": "तुमचे कॅलरी सेवन",
        "lower": "तुमचे सेवन शिफारस केलेल्यापेक्षा कमी आहे",
        "higher": "तुमचे सेवन शिफारस केलेल्यापेक्षा जास्त आहे",
        "aligns": "तुमचे सेवन शिफारसींशी जुळते आहे",
        "meal_plan": "🍽️ तुमची वैयक्तिक आहार योजना",
        "daily_meals": "तुमचे दैनंदिन जेवण",
        "nutrient_intake": "📊 दैनंदिन पोषक घटक सेवन तपशील",
        "macronutrient": "🥗 मॅक्रोन्यूट्रिएंट वितरण",
        "food_recommendation": "🔍 अन्न शिफारस जागा",
        "exercise_plan": "🏋️ तुमची वैयक्तिक व्यायाम योजना",
        "full_body": "संपूर्ण-शरीर व्यायाम योजना",
        "exercise_tips": "व्यायाम टिपा",
        "weight_loss_tips": "- कार्डिओ व्यायामांवर लक्ष केंद्रित करा (30-60 मिनिटे प्रति सत्र)\n- आठवड्यातून 2-3 वेळा HIIT व्यायाम समाविष्ट करा\n- स्नायू टिकवून ठेवण्यासाठी स्ट्रेंथ ट्रेनिंग",
        "muscle_gain_tips": "- स्ट्रेंथ ट्रेनिंगला प्राधान्य द्या (आठवड्यातून 3-5 वेळा)\n- प्रगतीशील ओव्हरलोडवर लक्ष केंद्रित करा\n- व्यायामांदरम्यान पुरेसा विश्रांती घ्या",
        "maintenance_tips": "- कार्डिओ आणि स्ट्रेंथ ट्रेनिंगमध्ये संतुलन राखा\n- कंटाळा टाळण्यासाठी विविध क्रियाकलाप करा\n- तुमच्या शरीराचे ऐका आणि आवश्यकतेनुसार समायोजित करा",
        "download_meal": "📥 आहार योजना डाउनलोड करा",
        "fill_details": "👈 सुरू करण्यासाठी साइडबारमध्ये तुमचे तपशील भरा आणि 'योजना तयार करा' वर क्लिक करा"
    }
}

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stSlider {
        color: #4CAF50;
    }
    .stPlot {
        margin: 0;
        padding: 0;
    }
    .info-box {
        background-color: #2c3e50;
        color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .info-box h4 {
        color: #4CAF50;
        margin-top: 0;
    }
    .info-box ol {
        padding-left: 20px;
    }
    .info-box li {
        margin-bottom: 8px;
    }
    .snack-container {
        background-color:#f0f8ff; 
        padding:10px; 
        border-radius:10px; 
        border-left: 5px solid #4CAF50; 
        margin-bottom:20px;
    }
    .snack-container h4 {
        color:#2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Language selection
language = st.sidebar.selectbox("🌐 Language", ["English", "Hindi", "Marathi"], index=0).lower()
t = translations[language]

# Sidebar for User Inputs
st.sidebar.title(t["title"])
st.sidebar.write(t["instructions"])

# User Inputs
st.sidebar.header(t["personal_info"])
age = st.sidebar.number_input(t["age"], min_value=10, max_value=100, step=1)
gender = st.sidebar.radio(t["gender"], ["Male", "Female"])
weight_kg = st.sidebar.number_input(t["weight"], min_value=30, max_value=200, step=1)
height_cm = st.sidebar.number_input(t["height"], min_value=100, max_value=250, step=1)
activity_level = st.sidebar.selectbox(t["activity"], ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])

st.sidebar.header(t["goals"])
goal = st.sidebar.selectbox(t["goal_select"], ["Weight Loss", "Maintenance", "Muscle Gain"])
food_pref = st.sidebar.radio(t["food_pref"], ["Any", "Vegetarian", "Non-Vegetarian"])
region_pref = st.sidebar.multiselect(t["region_pref"], options=load_data()["region"].unique(), default=load_data()["region"].unique())
allergies = st.sidebar.multiselect(t["allergies"], options=load_data()["allergies"].dropna().unique())

st.sidebar.header(t["calorie_intake"])
use_calculated = st.sidebar.checkbox(t["use_calculated"], value=True)
if not use_calculated:
    daily_calories = st.sidebar.number_input(t["enter_calories"], min_value=800, max_value=4000, step=50, value=2000)
else:
    daily_calories = None

st.sidebar.header(t["nutrient_weight"])
pref_nutrient = st.sidebar.slider(t["nutrient_score"], 0, 100, 40)
pref_health = st.sidebar.slider(t["health_score"], 0, 100, 30)
pref_diversity = st.sidebar.slider(t["diversity_score"], 0, 100, 20)
pref_protein = st.sidebar.slider(t["protein_ratio"], 0, 100, 10)

# Main Content Area
st.title(t["title"])
st.markdown(f"""
<div class="info-box">
    <h4>{t["how_it_works"]}</h4>
    <ol>
        <li>{t["step1"]}</li>
        <li>{t["step2"]}</li>
        <li>{t["step3"]}</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Generate Plans Button
if st.sidebar.button(t["generate"]):
    with st.spinner("Generating your personalized meal and exercise plan..."):
        # Calculate BMI and Recommended Calories
        bmi = calculate_bmi(weight_kg, height_cm)
        bmr = calculate_bmr(age, gender, weight_kg, height_cm)
        recommended_calories = calculate_daily_calories(bmr, activity_level, goal)
        
        # Use calculated calories if not manually specified
        if use_calculated:
            daily_calories = recommended_calories

        # Create Tabs for Diet and Exercise
        tab1, tab2 = st.tabs(["🍽️ " + t["meal_plan"], "🏋️ " + t["exercise_plan"]])

        # Diet Plan Tab
        with tab1:
            st.header(t["health_metrics"])
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("BMI", f"{bmi:.1f}")
                if bmi < 18.5:
                    st.warning(t["underweight"])
                elif 18.5 <= bmi < 24.9:
                    st.success(t["normal"])
                elif 25 <= bmi < 29.9:
                    st.warning(t["overweight"])
                else:
                    st.error(t["obese"])
            
            with col2:
                st.metric(t["recommended_calories"], f"{recommended_calories:.0f} kcal")
                if not use_calculated:
                    st.metric(t["your_intake"], f"{daily_calories} kcal")
                    if daily_calories < recommended_calories * 0.95:
                        st.warning(t["lower"])
                    elif daily_calories > recommended_calories * 1.05:
                        st.warning(t["higher"])
                    else:
                        st.success(t["aligns"])

            st.header(t["meal_plan"])
            data = load_data()
            
            # Show diet recommendations
            meal_plans, total_nutrients = recommend_diet(
                daily_calories=daily_calories,
                pref_nutrient=pref_nutrient,
                pref_health=pref_health,
                pref_diversity=pref_diversity,
                pref_protein=pref_protein,
                region_pref=region_pref,
                food_pref=food_pref,
                allergies=allergies,
                data=data
            )
            
            # Create a DataFrame for the meal plan
            meal_plan_df = pd.DataFrame()
            for meal, plan in meal_plans.items():
                meal_df = pd.DataFrame(plan, columns=["Food Item", "Serving Size (g)", "Calories", "Protein (g)", "Carbs (g)", "Fats (g)"])
                meal_df["Meal"] = meal.capitalize()
                meal_plan_df = pd.concat([meal_plan_df, meal_df])
            
            # Add download button for meal plan
            csv = meal_plan_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t["download_meal"],
                data=csv,
                file_name='personalized_meal_plan.csv',
                mime='text/csv',
            )
            
            # Display all meals with special styling for snacks
            st.subheader(t["daily_meals"])
            for meal, plan in meal_plans.items():
                if meal == "snack":
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="snack-container">
                                <h4>🍎 {meal.capitalize()}</h4>
                                {pd.DataFrame(plan, columns=["Food Item", "Serving Size (g)", "Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]).to_html(index=False)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    with st.container():
                        st.subheader(f"🍽️ {meal.capitalize()}")
                        st.table(pd.DataFrame(plan, columns=["Food Item", "Serving Size (g)", "Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]))
            
            # Daily Nutrient Intake Table
            st.header(t["nutrient_intake"])
            
            # Create a more detailed nutrient table
            nutrient_data = {
                "Nutrient": ["Calories", "Protein", "Carbohydrates", "Fats"],
                "Total Intake": [
                    total_nutrients["Calories"],
                    total_nutrients["Protein"],
                    total_nutrients["Carbs"],
                    total_nutrients["Fats"]
                ],
                "Recommended": [
                    daily_calories,
                    daily_calories * 0.3 / 4,  # 30% of calories from protein (4 cal/g)
                    daily_calories * 0.5 / 4,   # 50% of calories from carbs (4 cal/g)
                    daily_calories * 0.2 / 9     # 20% of calories from fats (9 cal/g)
                ],
                "Percentage": [
                    f"{total_nutrients['Calories']/daily_calories*100:.1f}%",
                    f"{total_nutrients['Protein']/(daily_calories*0.3/4)*100:.1f}%",
                    f"{total_nutrients['Carbs']/(daily_calories*0.5/4)*100:.1f}%",
                    f"{total_nutrients['Fats']/(daily_calories*0.2/9)*100:.1f}%"
                ]
            }
            
            # Display the nutrient table with conditional formatting
            df_nutrients = pd.DataFrame(nutrient_data)
            st.dataframe(
                df_nutrients.style.format({
                    "Total Intake": "{:.1f}",
                    "Recommended": "{:.1f}"
                }).applymap(lambda x: "color: green" if float(x[:-1]) > 90 else "color: orange" if x.endswith("%") and float(x[:-1]) < 70 else "", 
                          subset=["Percentage"]),
                use_container_width=True
            )
            
            # Macronutrient Pie Chart
            st.header(t["macronutrient"])
            fig = px.pie(
                names=["Protein", "Carbs", "Fats"],
                values=[total_nutrients["Protein"]*4, total_nutrients["Carbs"]*4, total_nutrients["Fats"]*9],
                title="Calorie Contribution by Macronutrient",
                color=["Protein", "Carbs", "Fats"],
                color_discrete_map={"Protein": "#4CAF50", "Carbs": "#FFC107", "Fats": "#FF5722"}
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True, key="macronutrient_pie_chart")
            
            # Show visualization
            st.header(t["food_recommendation"])
            st.write("Visualizing how your preferences align with different food options:")
            show_3d_visualization(
                df=data,
                pref_nutrient=pref_nutrient,
                pref_health=pref_health,
                pref_diversity=pref_diversity,
                pref_protein=pref_protein,
                goal=goal
            )

        # Exercise Plan Tab
# In your Streamlit app, replace the exercise plan tab content with:

# Exercise Plan Tab
        with tab2:
            st.header("🏋️ Your Personalized Weekly Exercise Plan")
            
            # Initialize ExerciseRecommender
            recommender = ExerciseRecommender()
            
            # Show weekly plan overview
            st.subheader("📅 Weekly Workout Schedule")
            weekly_plan = recommender.get_weekly_plan()
            
            cols = st.columns(7)
            for i, (day, muscles) in enumerate(weekly_plan.items()):
                with cols[i]:
                    st.markdown(f"**{day}**")
                    if "Rest" in muscles[0]:
                        st.write("🛌 Rest")
                        st.write("or")
                        st.write("🏃 Cardio")
                    else:
                        for muscle in muscles:
                            st.write(f"💪 {muscle}")
            
            # Show detailed workouts for all days
            st.subheader("💡 Daily Workout Details")
            for day in weekly_plan:
                with st.expander(f"{day} Workout", expanded=True):
                    day_workout = recommender.get_day_workout(day)
                    
                    if "Rest" in day_workout:
                        st.markdown("### Rest Day Recommendations")
                        st.write("""
                        - Active recovery (light walking, stretching)
                        - Focus on mobility work
                        - Hydrate well
                        - Optionally do light cardio (30 mins max)
                        """)
                    else:
                        for muscle_group, exercises in day_workout.items():
                            st.markdown(f"### {muscle_group} Exercises")
                            st.table(exercises)
                            st.markdown(f"**Expert Tip:** {recommender.get_expert_tips(muscle_group)}")
                        
                        # Add workout notes section
                        st.text_area("Add your personal notes for this workout", 
                                key=f"notes_{day}",
                                height=100)

            # Add general exercise tips based on goal
            st.subheader("🎯 Goal-Specific Training Tips")
            if goal == "Weight Loss":
                st.write(t["weight_loss_tips"])
            elif goal == "Muscle Gain":
                st.write(t["muscle_gain_tips"])
            else:  # Maintenance
                st.write(t["maintenance_tips"])
            
            # Add download option for workout plan
            st.download_button(
                label="📥 Download Weekly Workout Plan",
                data=pd.DataFrame.from_dict(weekly_plan, orient='index').to_csv(),
                file_name='weekly_workout_plan.csv',
                mime='text/csv'
    )
# Show instructions if not generated yet
else:
    st.info(t["fill_details"])
    st.image("https://images.unsplash.com/photo-1498837167922-ddd27525d352", caption="Healthy eating and exercise lead to better health")