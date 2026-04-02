import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# LOAD DATA
df = pd.read_csv('students_data.csv')

# FEATURES
X = df[['cat', 'assignment', 'attendance']]

# TARGET (final score)
y = df['final_score']

# TRAIN MODEL
model = LinearRegression()
model.fit(X, y)

# SAVE
joblib.dump(model, 'model.pkl')

print("Model trained for score prediction!")