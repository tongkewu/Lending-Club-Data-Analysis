import glob
import pandas as pd 
import pickle

######## Data 1
# read data from csv files
df_list = []
for file in glob.glob('./LCData/*.csv'):
	df = pd.read_csv(file, engine = 'python', skiprows = 1, skipfooter = 2)
	df_list.append(df)

loan1 = pd.concat(df_list, axis = 0, join = 'outer') # the loan_data frame with shape (1646779, 151)

# store data in pickle file
with open('LCData1.pl', 'wb') as f:
	pickle.dump(loan_data,f)

with open('LCData11.pl', 'rb') as f:
	loan1 = pickle.load(f)

smr1 = pd.DataFrame({'missing_value':loan1.isnull().sum(), 'number_of_value s':loan1.apply(lambda x: len(x.unique()))})

######## Data 2 with Payment history
loan_all = pd.read_csv('PMTHIST_ALL_201712.csv', dtype = {'Inquiries6M':'str'}) # shape (3790864, 40)

smr2 = pd.DataFrame({'missing_value':loan_all.isnull().sum(), 'number_of_value s':loan_all.apply(lambda x: len(x.unique()))})


# find loans existing in both Data 1 and Data 2
id_all = set(loan_all['LOAN_ID'])  # 134966 ids
id1 = set(loan1['id'])             # 1646779 ids
id_wtd = id_all.intersection(id1)  # 92431 ids

data1 = loan1.loc[loan1['id'].isin(id_wtd)]  # shape (92431, 151)
data2 = loan_all.loc[loan_all['LOAN_ID'].isin(id_wtd)]  # shape (2543732, 40)

df2 = data2.loc[:,['LOAN_ID','PBAL_BEG_PERIOD','PRNCP_PAID','INT_PAID','FEE_PAID','DUE_AMT','RECEIVED_AMT','RECEIVED_D','PERIOD_END_LSTAT','MONTH','PBAL_END_PERIOD','MOB','CO','COAMT','VINTAGE']]

# new data set
loan_data = df2.merge(data1, how = 'outer', left_on = 'LOAN_ID', right_on = 'id')  # shape (2543732, 166)

msv = pd.DataFrame({'missing_value':loan_data.isnull().sum()})
msv['percent'] = msv['missing_value']/len(loan_data)

drop_cols = ['member_id', 'id','loan_status','url','debt_settlement_flag','debt_settlement_flag_date','settlement_status','settlement_date',
'settlement_amount','settlement_percentage','settlement_term','hardship_flag','hardship_type',
'hardship_reason','hardship_status','deferral_term','hardship_amount','hardship_start_date',
'hardship_end_date','payment_plan_start_date','hardship_length','hardship_dpd','hardship_loan_status',
'orig_projected_additional_accrued_interest','hardship_payoff_balance_amount','hardship_last_payment_amount'
'annual_inc_joint','dti_joint','verification_status_joint','next_pymnt_d','last_pymnt_d','last_pymnt_amnt', 'last_credit_pull_d']

loan_data = loan_data.drop(drop_cols, axis = 1)

# add dummy variables to missing value
msv = pd.DataFrame({'count':loan_data.isnull().sum()})
add_dummy_cols = msv[msv['count']!=0].index.values.tolist() + ['desc','zip_code','addr_state']

def add_dummy_variable(df, col_name):
	idx = df[col_name].index[df[col_name].isnull()]
	dummy_col_name = col_name + '_dummy'
	df[dummy_col_name] = [1] * len(df)
	df.loc[idx, dummy_col_name] = 0

for col in add_dummy_cols:
	add_dummy_variable(loan_data, col)

# format time data
import datetime

issue_d = [datetime.datetime.strptime(dt,'%b-%Y') for dt in loan_data['issue_d']]
month = [datetime.datetime.strptime(dt,'%b%Y') for dt in loan_data['MONTH']]
mths_after_issue_d = [(m-i).days//30 for m,i in zip(month,issue_d)]  # same as MOB

earliest_cr_line = [datetime.datetime.strptime(dt,'%b-%Y') for dt in loan_data['earliest_cr_line']]
ecl_issue = [(i-e).days//30 for e,i in zip(earliest_cr_line,issue_d)]
loan_data['ecl_issue'] = ecl_issue

term = [int(s.split(' ')[1]) for s in loan_data['term']]
loan_data['term'] = term

useless_col = ['desc','zip_code','addr_state','issue_d', 'MONTH', 'earliest_cr_line', 'RECEIVED_D']
loan_data = loan_data.drop(useless_col, axis = 1)

# convert str of percentage to float
def str2float(df, col_name):
	df[col_name] = [float(s.strip('%'))/100 for s in df[col_name].values]

str_cols = ['revol_util', ]

# add variable of Last_loan_status
last_status = loan_data.groupby('LOAN_ID').apply(lambda x: pd.Series(['Current']).append(x['PERIOD_END_LSTAT'][:-1])).values
loan_data['last_loan_status'] = last_status

# split training set and test set
loan_data = pd.read_csv('new_data.csv')

from sklearn.preprocessing import LabelEncoder
# translate categorical data into numerical
def Label_encoder(df, col_name):
	le = LabelEncoder()
	df[col_name] = le.fit_transform(df[col_name].values)
le_cols = ['PERIOD_END_LSTAT', 'last_loan_status', 'VINTAGE', 'grade', 'sub_grade', 'emp_title', 'emp_length', 'home_ownership', 'verification', 'pymnt_plan', 'purpose','title','initial_list_status', 'application_type']
for col in le_cols:
	Label_encoder(loan_data, col)

y = loan_data['PERIOD_END_LSTAT'].values

var_names = loan_data.columns.values.tolist()
var_names.remove('PERIOD_END_LSTAT')
var_names.remove('LOAN_ID')

X = loan_data.loc[:,var_names].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 5)

