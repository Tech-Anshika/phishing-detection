import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

def train_model(input_csv="data/final_feature_dataset.csv", model_file="models/phish_model.pkl"):
    # Load dataset
    df = pd.read_csv(input_csv)

    if "label" not in df.columns:
        raise ValueError("❌ Dataset me 'label' column missing hai! Add labels first.")

    # Drop unwanted columns
    X = df.drop(columns=["domain", "label", "ssl_issuer", "error"], errors="ignore")
    y = df["label"]

    # ✅ Save the feature column order for prediction
    feature_cols = X.columns.tolist()
    os.makedirs("models", exist_ok=True)
    joblib.dump(feature_cols, "models/feature_cols.pkl")
    print("✅ Feature columns saved for prediction:", feature_cols)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("\n✅ Model Training Completed!\n")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model
    joblib.dump(clf, model_file)
    print(f"\n💾 Model saved at {model_file}")


if __name__ == "__main__":
    train_model()
