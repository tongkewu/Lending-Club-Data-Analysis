import pickle
import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

with open('train_test_set.pl', 'rb') as f:
X_train, X_test, y_train, y_test = pickle.load(f)



train_as_dicts = [dict(r.iteritems()) for _, r in X_train.fillna(-1).iterrows()]
vectorizer = DictVectorizer()
X_train_vec = vectorizer.fit_transform(train_as_dicts) #n380855x26828
test_as_dicts = [dict(r.iteritems()) for _, r in X_test.fillna(-1).iterrows()]
X_test_vec = vectorizer.transform(test_as_dicts)

def Label_enc(df):
    le = LabelEncoder()
    le.fit(df.unique())
    vec = le.transform(df.values)
    return vec

y_train_vec = Label_enc(y_train)
y_test_vec = Lahel_enc(y_test)

#%%
logistic = LogisticRegression(multi_class = 'multinomial', solver = 'sag')
logistic.fit(X_train_vec, y_train_vec)

y_pred_log = logistic.predict(X_test_vec)
y_test_vec = Label_enc(y_test)
target_names = ['Charged Off', 'Current', 'Default', 'Fully Paid', 'In Grace Period', 'Issued', 'Late (16-30 days)', 'Late (31-120 days)']
print(classification_report(y_test_vec, y_pred_log, target_names = target_names))

#%%
# Compute ROC curve and ROC area for each class
y_test_bin = label_binarize(y_test_vec, classes = [0,1,2,3,4,5,6,7])
y_score = logistic.decision_function(X_test_vec)

fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(8):
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    
#%%
import matplotlib.pyplot as plt
from itertools import cycle
import matplotlib.patches as mpatches

fig = plt.figure()
ax  = fig.add_subplot(111)
ax.set_position([0.02,0.1,0.6,0.8])
colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'deeppink', 'navy','purple', 'green', 'yellow'])
for i, color, lab in zip(range(8), colors, target_names):
    ax.plot(fpr[i], tpr[i], color=color, lw = 2,
             label='{0} (area = {1:0.2f})'
             ''.format(lab, roc_auc[i]))
    
plt.plot([0, 1], [0, 1], 'k--', lw = 2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves of Predicted Loan Status')
plt.legend(bbox_to_anchor = (1, 1))
plt.savefig('roc_curves.png', bbox_inches='tight')
#plt.show()


