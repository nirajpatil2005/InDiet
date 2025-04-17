import pandas as pd
import numpy as np
import random
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go

@st.cache_data
def load_data():
    # Load and preprocess data
    df = pd.read_csv("resource/sd.csv")
    
    # Select features for clustering
    features = ['nutrient_score', 'health_score', 'diversity_score', 'protein_calorie_ratio']
    X = df[features].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    return df

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def calculate_bmr(age, gender, weight_kg, height_cm):
    if gender == "Male":
        return 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

def calculate_daily_calories(bmr, activity_level, goal):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    maintenance_calories = bmr * activity_multipliers.get(activity_level, 1.2)
    
    if goal == "Weight Loss":
        return maintenance_calories * 0.85
    elif goal == "Muscle Gain":
        return maintenance_calories * 1.15
    else:
        return maintenance_calories

def recommend_diet(daily_calories, pref_nutrient, pref_health, pref_diversity, pref_protein, region_pref, food_pref, allergies, data):
    # Normalize Weights
    total_weight = pref_nutrient + pref_health + pref_diversity + pref_protein
    w_nutrient = pref_nutrient / total_weight
    w_health = pref_health / total_weight
    w_diversity = pref_diversity / total_weight
    w_protein = pref_protein / total_weight

    # Filter Data Based on User Preferences
    filtered_data = data[data["region"].isin(region_pref)]
    if food_pref != "Any":
        filtered_data = filtered_data[filtered_data["food_group_nin"] == food_pref]
    if allergies:
        filtered_data = filtered_data[~filtered_data["allergies"].isin(allergies)]

    # Meal Planning
    total_nutrients = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fats": 0}
    meal_plans = {}

    for meal in ["breakfast", "lunch", "snacks", "dinner"]:
        meal_subset = filtered_data[filtered_data["food_type"] == meal]
        calories_per_meal = daily_calories * 0.25

        if len(meal_subset) > 0:
            # Compute weighted score
            meal_subset["weighted_score"] = (
                meal_subset["nutrient_score"] * w_nutrient +
                meal_subset["health_score"] * w_health +
                meal_subset["diversity_score"] * w_diversity +
                meal_subset["protein_calorie_ratio"] * w_protein
            )

            # Pick top 10 highest-ranked meals
            top_meals = meal_subset.nlargest(10, "weighted_score")

            # Randomly select 3 meals from the top 10
            random_meals = top_meals.sample(n=min(3, len(top_meals)), random_state=random.randint(1, 100))

            meal_plan = []
            meal_calories = 0

            for _, row in random_meals.iterrows():
                factor = calories_per_meal / row["energy_kcal"]
                adjusted_serving = max(50, min(400, round(row["Serving_Size_g"] * factor, 1)))
                adjusted_energy = row["energy_kcal"] * (adjusted_serving / row["Serving_Size_g"])
                adjusted_protein = row["protein_g"] * (adjusted_serving / row["Serving_Size_g"])
                adjusted_carbs = row["carb_g"] * (adjusted_serving / row["Serving_Size_g"])
                adjusted_fats = row["fat_g"] * (adjusted_serving / row["Serving_Size_g"])

                meal_plan.append([row["food_name"], adjusted_serving, round(adjusted_energy, 1), 
                                round(adjusted_protein, 1), round(adjusted_carbs, 1), round(adjusted_fats, 1)])
                meal_calories += adjusted_energy

                # Add to total nutrients
                total_nutrients["Calories"] += adjusted_energy
                total_nutrients["Protein"] += adjusted_protein
                total_nutrients["Carbs"] += adjusted_carbs
                total_nutrients["Fats"] += adjusted_fats

            meal_plans[meal] = meal_plan
            
    return meal_plans, total_nutrients

def show_3d_visualization(df, pref_nutrient, pref_health, pref_diversity, pref_protein, goal):
    # Features used for analysis
    features = ['nutrient_score', 'health_score', 'diversity_score', 'protein_calorie_ratio']
    
    # Prepare data with fresh scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features].values)
    
    # Dynamic PCA
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(X_scaled)
    
    # Create normalized user vector based on current goal
    if goal == "Weight Loss":
        user_vector = np.array([pref_nutrient*0.7, pref_health*1.3, pref_diversity*1.2, pref_protein*0.8])
    elif goal == "Muscle Gain":
        user_vector = np.array([pref_nutrient*1.4, pref_health*0.9, pref_diversity*0.7, pref_protein*1.5])
    else:
        user_vector = np.array([pref_nutrient, pref_health, pref_diversity, pref_protein])
    
    user_vector = user_vector / user_vector.sum()
    user_pca = pca.transform(user_vector.reshape(1, -1))[0]
    
    # Dynamic clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['current_cluster'] = kmeans.fit_predict(X_scaled)
    
    # Find nearest cluster for current user
    nbrs = NearestNeighbors(n_neighbors=1).fit(pca_result)
    _, user_cluster_idx = nbrs.kneighbors(user_pca.reshape(1, -1))
    user_cluster = df.iloc[user_cluster_idx[0][0]]['current_cluster']
    
    # Create the visualization
    fig = go.Figure()
    
    # Color mapping
    cluster_colors = {
        0: '#636EFA', 1: '#EF553B', 2: '#00CC96', 
        3: '#AB63FA', 4: '#FFA15A'
    }
    
    # Add food items
    for cluster in sorted(df['current_cluster'].unique()):
        cluster_mask = df['current_cluster'] == cluster
        fig.add_trace(go.Scatter3d(
            x=pca_result[cluster_mask, 0],
            y=pca_result[cluster_mask, 1],
            z=pca_result[cluster_mask, 2],
            mode='markers',
            marker=dict(
                size=6,
                color=cluster_colors[cluster],
                opacity=0.7 if cluster == user_cluster else 0.3,
                line=dict(width=0.5, color='white')
            ),
            name=f'Cluster {cluster}',
            text=df[cluster_mask]['food_name'],
            hoverinfo='text'
        ))
    
    # Add user point
    fig.add_trace(go.Scatter3d(
        x=[user_pca[0]],
        y=[user_pca[1]],
        z=[user_pca[2]],
        mode='markers',
        marker=dict(
            size=15,
            color='#FFD700',
            opacity=1,
            line=dict(width=2, color='black')
        ),
        name='YOU',
        hoverinfo='text',
        text=[f"Your Preferences<br>Goal: {goal}<br>Nearest to Cluster {user_cluster}"]
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Nutritional Space - Goal: {goal}',
        scene=dict(
            xaxis_title=f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)',
            yaxis_title=f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)',
            zaxis_title=f'PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=800
    )
    
    st.plotly_chart(fig, use_container_width=True, key="3d_food_visualization")
    
    # Cluster interpretation
    cluster_descriptions = {
        0: "High Protein, Low Carb (Best for muscle gain)",
        1: "Balanced Nutrition (General health)",
        2: "High Carb, Low Fat (Endurance activities)",
        3: "High Nutrient Density (Vitamins/minerals)",
        4: "High Diversity (Varied microbiome support)"
    }
    
    st.markdown(f"""
    ### Cluster Interpretation
    - **Your position is nearest to Cluster {user_cluster}**: {cluster_descriptions.get(user_cluster, 'General')}
    - Other clusters:
    {''.join([f'\n- **Cluster {k}**: {v}' for k,v in cluster_descriptions.items() if k != user_cluster])}
    """)