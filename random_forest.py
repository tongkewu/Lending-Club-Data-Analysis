import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

with open('train_test_set.pl', 'rb') as f:
    X_train, X_test, y_train, y_test = pickle.load(f)

# Feature Vectorization
train_as_dicts = [dict(r.iteritems()) for _, r in X_train.fillna(-1).iterrows()]
vectorizer = DictVectorizer()
vectorized_sparse = vectorizer.fit_transform(train_as_dicts) 
#vectorized_array = vectorized_sparse.toarray()
test_as_dicts = [dict(r.iteritems()) for _, r in X_test.fillna(-1).iterrows()]
X_test_vec = vectorizer.transform(test_as_dicts)

# Label Encoding
def Label_enc(df):
    le = LabelEncoder()
    le.fit(df.unique())
    vec = le.transform(df.values)
    return vec

y_train_vec = Label_enc(y_train)

# Build Classifier
rfr = RandomForestRegressor(n_estimators = 100, max_depth = 5)
rfr.fit(X_train, y_train)

y_pred = [int(y_p) for y_p in rfr.predict(X_test_vec)]
target_names = ['Charged Off', 'Current', 'Default', 'Fully Paid', 'In Grace Period', 'Issued', 'Late (16-30 days)', 'Late (31-120 days)']
print(classification_report(y_test_vec, y_pred, target_names = target_names))

feat_import = pd.DataFrame(rfr.feature_importances_, index = vectorizer.feature_names_, columns = ["Feature_Importance"]).sort_values(by = "Feature_Importance", ascending = True)
ax = feat_import.iloc[-50:, :].plot.barh(figsize = (7, 14), fontsize = 12, legend = False)
fig = ax.get_figure()
ax.set_title("Feature Importance", fontsize = 15)
fig.savefig('feature_importance.png')

