import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.svm import SVC, OneClassSVM
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
import joblib
import os 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
# 1. Load and clean
df = pd.read_csv("../data_collector/dataset.csv").dropna()

# 2. Encode protocol
le_protocol = LabelEncoder()
df["protocol"] = le_protocol.fit_transform(df["protocol"])

# 3. Drop unused string fields
drop_cols = ["timestamps", "src_ip", "dst_ip", "src_mac", "dst_mac"]
df = df.drop(columns=drop_cols, errors="ignore")

# 4. Define features and labels
packet_size = df["packet_size"].values
X = df.drop("label", axis=1)
y = df["label"]

# 5. Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 6. Train/Test split
X_train, X_test, y_train, y_test, ps_train, ps_test = train_test_split(
    X_scaled, y, packet_size, test_size=0.2, random_state=42
)

# 7. Train Supervised Models
clf_rf = RandomForestClassifier().fit(X_train, y_train)
clf_knn = KNeighborsClassifier().fit(X_train, y_train)
clf_svc = SVC().fit(X_train, y_train)

# 8. Train Regressors (Predict `packet_size`)
reg_rf = RandomForestRegressor().fit(X_train, ps_train)
reg_lr = LinearRegression().fit(X_train, ps_train)

# 9. Train Unsupervised Models
iso_forest = IsolationForest().fit(X_scaled)
one_class_svm = OneClassSVM().fit(X_scaled)

# 10. Save everything
joblib.dump(clf_rf, os.path.join(MODELS_DIR, "clf_rf.pkl"))
joblib.dump(clf_knn, os.path.join(MODELS_DIR, "clf_knn.pkl"))
joblib.dump(clf_svc, os.path.join(MODELS_DIR, "clf_svc.pkl"))
joblib.dump(reg_rf, os.path.join(MODELS_DIR, "reg_rf.pkl"))
joblib.dump(reg_lr, os.path.join(MODELS_DIR, "reg_lr.pkl"))
joblib.dump(iso_forest, os.path.join(MODELS_DIR, "iso_forest.pkl"))
joblib.dump(one_class_svm, os.path.join(MODELS_DIR, "one_class_svm.pkl"))
joblib.dump(scaler, os.path.join(MODELS_DIR, "minmax_scaler.pkl"))
joblib.dump(le_protocol, os.path.join(MODELS_DIR, "label_encoder_protocol.pkl"))