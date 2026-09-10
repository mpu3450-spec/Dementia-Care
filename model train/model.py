import pandas as pd
df= pd.read_csv("game_results.csv")
# print the used dataset
print("Original dataset")
print(df.head())

# check the missing values
print("Missing values:")
print(df.isnull().sum())

# Handle the missing value
df=df.dropna()
print(df.isnull().sum())

# Check the duplicate rows
print("Duplicate rows:")
print(df.duplicated().sum())

# Check the invalid values
# Score
df=df[(df["score"]>=0) & (df["score"]<=100)]
# Accuracy
df=df[(df["accuracy"]>=0) & (df["accuracy"]<=100)]
# Response Time
df=df[(df["response_time"]>0)]

# Import cleaned dataset
df.to_csv("cleangame_results.csv",index=False)
print("Data cleaning Done.")

#Feature engineering
df=pd.read_csv("cleangame_results.csv")

#Mistake rate
df["mistake_rate"] = df["mistakes"]/df["attempts"]
print(df["mistake_rate"])

# Speed Score
df["speed_score"]= 100/(1+df["response_time"])
print(df["speed_score"])
# Normalize speed score
min_speed= df["speed_score"].min()
max_speed= df["speed_score"].max()
df["speed_score_normalized"]=(df["speed_score"]-min_speed)/(max_speed- min_speed)*100

# Performance Score
df["performance_score"]=(0.40* df["accuracy"]+
                         0.30* df["score"]+
                         0.20* df["speed_score_normalized"]+
                         0.10*(100 - df["mistake_rate"]*100))
print(df[["patient_id","score","accuracy","mistake_rate","speed_score_normalized","performance_score"]].head())

# Trend Analysis
df["date"]= pd.to_datetime(df["date"])
df= df.sort_values(["patient_id","date"])

def calculate_trend(scores):
    if len(scores)<2:
        return "Not Enough Data"
    difference= scores.iloc[-1]- scores.iloc[0]

    if difference > 5:
        return "Improving"
    elif difference < -5:
        return "Declining"
    else:
        return "Stable"

# Trend of each patient
trend_data=df.groupby("patient_id")["performance_score"].apply(calculate_trend)
print(trend_data)

# Performance level 
def get_performance_level(score):
    if score < 50:
        return "Low"
    elif score < 75:
        return "Medium"
    else:
        return "High"
df["performance_level"]=df["performance_score"].apply(get_performance_level)

# Select input and output feature 
features = [
    "accuracy",
    "response_time",
    "mistakes",
    "attempts",
    "score"
]
X = df[features]
y = df["performance_level"]

# Train test split
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

# Model training 
from sklearn.ensemble import RandomForestClassifier
model= RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)
print("Model training complete.")

# Model prediction
y_pred= model.predict(X_test)

# Accuracy
from sklearn.metrics import accuracy_score
accuracy= accuracy_score(y_test,y_pred)
print("Model Accuracy: ", accuracy*100)

# Precision
from sklearn.metrics import precision_score
precision= precision_score(y_test,y_pred,average="weighted")
print("Precision:",precision*100)

# Recall
from sklearn.metrics import recall_score
recall= recall_score(y_test,y_pred,average="weighted")
print("Recall:",recall*100)

# F1 score
from sklearn.metrics import f1_score
f1= f1_score(y_test,y_pred,average="weighted")
print("f1 score :",f1*100)

# Add predicted performance to dataset
df["predicted_performance"]=model.predict(df[features])

# Save output backend
output = df[
    [
        "patient_id",
        "date",
        "performance_score",
        "performance_level",
        "predicted_performance"
    ]
]

output.to_csv("model_predictions.csv", index=False)

print("M1 prediction output saved successfully.")