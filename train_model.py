import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

# Read dataset
df = pd.read_csv("dddddd.csv.csv")

# Check for missing values and drop rows with any missing data
if df.isnull().sum().any():
    df = df.dropna()

# Encode input features: convert 'yes'/'no' to 1/0
X = df.drop('career', axis=1).replace({'yes': 1, 'no': 0})

# Encode target labels
le = LabelEncoder()
y = le.fit_transform(df['career'])

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# Train model with limited depth to avoid overfitting
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Predict and calculate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model and label encoder
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(le, f)
