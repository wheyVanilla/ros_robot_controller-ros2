# Re-import necessary modules after code execution reset
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


# Recreate the original data
data = {
    'Speed (rps)': [0.1]*3 + [0.5]*3 + [1.0]*3 + [1.5]*3 + [2.5]*3,
    'Calculated': [0.93, 1.84, 2.77, 0.92, 1.88, 2.74, 0.88, 1.86, 2.68, 0.88, 1.78, 2.71, 0.87, 1.8, 2.64],
    'Real':       [1.0, 2.0, 3.0, 1.0, 2.06, 3.0, 1.0, 2.08, 2.98, 1.0, 2.0, 3.03, 0.98, 2.02, 2.99],
}

data = {
    'Speed (rps)': [0.1]*2 + [1.0]*2 + [2.5]*2,
    'Calculated': [ 1.05, 2.12, 
                    1.06, 2.12, 
                    1.04, 2.06],
    'Real':       [ 1.0, 2.0, 
                    1.0, 2.0, 
                    1.03, 2.01],
}

df = pd.DataFrame(data)

# Linear regression to get correction factor
X = df['Real'].values.reshape(-1, 1)
y = df['Calculated'].values
model = LinearRegression()
model.fit(X, y)
alpha = model.coef_[0]
correction_factor = 1 / alpha

# Apply correction factor
df['Corrected'] = df['Calculated'] * correction_factor
df['Corrected_Error (%)'] = (df['Corrected'] - df['Real']) / df['Real'] * 100

# Show the corrected results
print(correction_factor)
