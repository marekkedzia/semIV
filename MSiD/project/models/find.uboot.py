import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from imblearn.over_sampling import ADASYN, SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

def load_and_prepare_data():
    df = pd.read_csv("../data/converted_merchants_data.csv", skiprows=1,
                     names=["uboat", "commander", "ship_name", "tonnage", "nationality", "convoy", "coordinates", "year", "month", "day"])
    df["tonnage"] = df["tonnage"].str.replace(',', '.').astype(float)
    return df

def select_features_and_target(df):
    features = ["commander", "ship_name", "tonnage", "nationality", "convoy", "year", "month", "day"]
    X = df[features].copy()
    y = df["uboat"]
    return X, y

def encode_labels(X):
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_encoded = ohe.fit_transform(X[["commander", "ship_name", "nationality", "convoy"]])
    X_encoded_df = pd.DataFrame(X_encoded, columns=ohe.get_feature_names_out(["commander", "ship_name", "nationality", "convoy"]))
    X = pd.concat([X_encoded_df, X[["tonnage", "year", "month", "day"]]], axis=1)
    return X

def encode_target(y):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return y_encoded, le

def apply_smote(X, y):
    smote = SMOTE(sampling_strategy='minority', k_neighbors=3, random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res

def remove_single_sample_classes(X, y):
    # Identify classes with only one sample
    class_counts = y.value_counts()
    single_sample_classes = class_counts[class_counts <= 3].index

    # Remove single-sample classes from X and y
    mask = ~y.isin(single_sample_classes)
    X_filtered = X[mask]
    y_filtered = y[mask]

    return X_filtered, y_filtered

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_and_evaluate_model(X_train, X_test, y_train, y_test, le):
    clf = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # Odwrócenie kodowania etykiet, aby uzyskać oryginalne nazwy klas
    y_test = le.inverse_transform(y_test)
    y_pred = le.inverse_transform(y_pred)

    with open("classification_report_find_uboot.txt", "w") as f:
        f.write("\nClassification Report:\n\n")
        f.write(classification_report(y_test, y_pred, zero_division=1))


df = load_and_prepare_data()
X, y = select_features_and_target(df)
X = encode_labels(X)
X, y = remove_single_sample_classes(X, y)
y, le = encode_target(y)
X_res, y_res = apply_smote(X, y)
X_train, X_test, y_train, y_test = split_data(X_res, y_res)
train_and_evaluate_model(X_train, X_test, y_train, y_test, le)
