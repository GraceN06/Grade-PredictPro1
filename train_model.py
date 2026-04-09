import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("students_academic_history.csv")

X = df[
    [
        'f1_math_avg', 'f1_english_avg', 'f1_biology_avg', 'f1_chemistry_avg',
        'f1_physics_avg', 'f1_history_avg', 'f1_geography_avg', 'f1_business_avg',

        'f2_math_avg', 'f2_english_avg', 'f2_biology_avg', 'f2_chemistry_avg',
        'f2_physics_avg', 'f2_history_avg', 'f2_geography_avg', 'f2_business_avg',

        'f3_math_avg', 'f3_english_avg', 'f3_biology_avg', 'f3_chemistry_avg',
        'f3_physics_avg', 'f3_history_avg', 'f3_geography_avg', 'f3_business_avg',

        'f4_math_avg', 'f4_english_avg', 'f4_biology_avg', 'f4_chemistry_avg',
        'f4_physics_avg', 'f4_history_avg', 'f4_geography_avg', 'f4_business_avg'
    ]
]

# Target
y = df['final_exam_score']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained and saved successfully as model.pkl")