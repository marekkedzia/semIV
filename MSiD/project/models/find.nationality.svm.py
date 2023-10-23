import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from imblearn.over_sampling import ADASYN
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize


def load_data():
    df = pd.read_csv("../data/converted_merchants_data.csv", skiprows=1,
                     names=["uboat", "commander", "ship_name", "tonnage", "nationality", "convoy", "coordinates", "year", "month", "day"])
    return df


def preprocess_data(df):
    df["tonnage"] = df["tonnage"].str.replace(',', '.').astype(float)
    df[['latitude','longitude']] = df['coordinates'].str.replace('[','').str.replace(']','').str.replace('(','').str.replace(')','').str.replace("'",'').str.replace(' ','').str.split(',',expand=True)
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    df = df.drop(columns=["coordinates"])
    return df


def select_features_and_target(df):
    features = ["uboat", "commander", "ship_name", "tonnage", "convoy", "year", "month", "day", "latitude", "longitude"]
    X = df[features].copy()
    y = df["nationality"]
    return X, y


def encode_features(X):
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_encoded = ohe.fit_transform(X[["uboat", "commander", "ship_name", "convoy"]])
    X_encoded_df = pd.DataFrame(X_encoded, columns=ohe.get_feature_names_out(["uboat", "commander", "ship_name", "convoy"]))
    X = pd.concat([X_encoded_df, X[["tonnage", "year", "month", "day", "latitude", "longitude"]]], axis=1)
    return X


def remove_single_sample_classes(X, y):
    class_counts = y.value_counts()
    single_sample_classes = class_counts[class_counts <= 6].index

    mask = ~y.isin(single_sample_classes)
    X_filtered = X[mask]
    y_filtered = y[mask]

    return X_filtered, y_filtered


def reencode_labels(y):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return y_encoded


def oversample_data(X, y):
    adasyn = ADASYN(random_state=42)
    X_res, y_res = adasyn.fit_resample(X, y)
    return X_res, y_res


def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    clf = LinearSVC(random_state=42)
    clf.fit(X_train, y_train)
    return clf


def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)

    print_classification_report(y_test, y_pred)
    print_confusion_matrix(y_test, y_pred)


def print_classification_report(y_test, y_pred):
    with open("classification_report.svm.txt", "w") as f:
        f.write("\nClassification Report:\n\n")
        f.write(classification_report(y_test, y_pred))


def print_confusion_matrix(y_test, y_pred):
    with open("classification_report.svm.txt", "a") as f:
        f.write("\nConfusion Matrix:\n\n")
        f.write(str(confusion_matrix(y_test, y_pred)))


def print_auc(y_test, y_prob, y_train):
    n_classes = len(set(y_train))
    y_test_bin = label_binarize(y_test, classes=list(range(n_classes)))
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    with open("classification_report.txt", "a") as f:
        f.write("\nAUC for each class:\n\n")
        for i in range(n_classes):
            f.write("Class {0}, AUC = {1:0.2f}\n".format(i, roc_auc[i]))


df = load_data()
df = preprocess_data(df)
X, y = select_features_and_target(df)
X = encode_features(X)
X, y = remove_single_sample_classes(X, y)
y = reencode_labels(y)
X_res, y_res = oversample_data(X, y)
X_train, X_test, y_train, y_test = split_data(X_res, y_res)
clf = train_model(X_train, y_train)
evaluate_model(clf, X_test, y_test)
