# Lending-Club-Data-Analysis
## Data Source
<li> <strong>Loan Statistics</strong>: panal data. These files contain complete loan data for all loans issued through the time period stated. </li>
<li><strong>Payment Historical Data</strong>: time series of payment and balance of loans.</li> 

The first data set is of size (1646779, 151) including 1646779  loans and 150 features from 2007 to 2016 Q3. The second data set with payment history is of size (3790864, 40) including 134966 loans and 39 features. To enrich the data set and keep the time information, I combined two data sets together and got features and payment history of 92431 loans. 

The problem we are intersted is the loan status. In this data set, there are 8 kinds of status related to the loan: Current, Fully Paid, Issued, In Grace Period, Late(16-30 days), Late(31-120 days), Defualt, Charged off. We want to model the probability of transition from one status to another. Thus it will be a multi-label classification problem. 

## Data Processing

| BGN\END          | Charged Off | Current | Default | Fully Paid | In Grace Period | Issued | Late (16-30 days) | Late (31-120 days) |
|------------------|:-----------:|:-------:|:-------:|:----------:|:---------------:|:------:|:-----------------:|:-------------------|
| Charged Off      | 0           | 0       |  0      |  0         |   0             | 0      |   0               | 0                  |
| Current          | 22          | 2371634 |    0    | 74912      | 55              |      0 |           1750    |        19110       |
| Default          | 9452        |  38     |  361    |  25        |    0            |   0    |  0                |   0                |
|Fully Paid        |  0          | 252     | 0       | 0          | 0               | 0      | 0                 | 0                  |
|In Grace Period   | 0           |  28     |  0      | 4          |  1              | 0      | 4                 |  5                 |
|Issued            |  0          |  8      | 0       | 6          | 0               | 3      |  0                | 0                  |
|Late (16-30 days) | 31          |  670    | 0       | 73         | 1               | 0      | 342               | 1015               |
|Late (31-120 days)| 4899        | 4891    | 9527    | 588        | 3               | 0      | 118               | 39201              |


Then the transition matrix is as following

```python
transition = {'Issued':['Issued', 'Current','Fully Paid'],
              'Current': ['Current', 'Fully Paid', 'In Grace Period', 'Late (16-30 days)', 'Late (31-120 days)', 'Charged Off'], 
              'In Grace Period': ['Current', 'Fully Paid', 'Late (16-30 days)', 'Late (31-120 days)', 'In Grace Period'],
              'Late (16-30 days)': ['Current','Fully Paid', 'Late (16-30 days)', 'Late (31-120 days)', 'In Grace Period', 'Charged Off'],
              'Late (31-120 days)': ['Current','Fully Paid', 'Late (16-30 days)', 'Late (31-120 days)', 'In Grace Period', 'Default', 'Charged Off'],
              'Default': ['Current', 'Fully Paid', 'Default', 'Charged Off'],
              'Fully Paid': ['Fully Paid']}
```

There are 166 columns in the combineng dataset. However, the data is not complete and we should check missing values first. Then we need to figure out why the data is missing and make adjustments. Meanwhile, we should remove useless data that can be either not informative or carrying the same information.

<img src="/image/missing_value_dist.png">

1. 100% Missing Data: There are 16 variables related to joint borrower/second applicant completely blank. It may because the joint loan program just launched at March 2017 and it's been a short time. Thus I dumped these variables.

2. 99.96% Missing Data: There are 15 variables related to hardship plan only with one loan reacord. Thus I dropped them.

3. Consequential Data: 7 variables are related to settlement plan and are absent for 99.09%. Settlement is a plan for borrower who gets charged off. Therefore, only loans charged off keep this record. Since settlement is the consequence of charged off, data related to it should not be considered as feature that can classify loan status. Thus I dumped 7 features related to settlement.

4. Meaningless Data: including 'url', 'member_id', which are complete but not informative thus are dropped. And 'last_pymnt_d', 'last_pymnt_amt', 'next_pymnt_d' are removed since they have the same information as that of payment history data.

After the above steps, there remains 122 columns in the data set. The next step is to format time data. 

5. Time Data: The aim is to convert time data to numerical data. One kind of variable like 'term' which has entry of ' 36 month' can be directly made number. The other kind of variables like 'issued_d' and 'MONTH' should be calculated and produce new feature like 'age of loan' to keep the time information from both variables.

Then we should check the type of data and take strategy to deal with the rest of missing value that cannot be removed directly. 

6. Categorical Data: There are 19 categorical variables. However, some of them such as 'emp_title', 'desc' hold too many levels since they are text message. It will be great if NLP is employed to extract infromation from them to reduce the number of levels. Due to the time limit, I created dummy variables to simply indicate there is data point or not. For the rest of categorical variables, I added a level of 'missing' that represents missing value. 

7. Continuous Data: For continuous variables, I created dummy variables to indicate whether the data is missing and filled in missing value with arbitrary number. It is a good idea to use an obviously out of range data.

Then I added a column called 'last_loan_status' so that the the payment time series is decomposed into subsamples. Finally the feature matrix is of 172 columns and a subset of data with size (1271866, 172) will be analyzed.

## Data Exploration
### Loan Status
Most of the loans are current and fully paid. The late and default loans are in small proportion thus this is an unbalanced case. We should consider set class_weight to improve the model performance in the future.

<img src="/image/loan_status_dist.png">

### Credit Grade

<img src="/image/grade_dist.png">

### Purpose of Loan Application

<img src="/image/purpose_dist.png">

## Modeling
### Feature Vectorization
To deal with categorical features, we should convert a feature with k levels to k-1 dummy variables. A proper way to do is to use DictVectorizer in python to create dummy variables and store in the sparse matrix. After the vectorization, we got a expended feature matrix with size(890306,26856).
### Random Forest Classifier
A random forest classifier with parameters <i> n_estimators = 100, max_depth = 5 </i> is firstly build to find important features. The following are features ranked top 50. From the barplot, we find features related to payment history are more helpful to identify status of loans.

<img src="/image/feature_importance.png">

Now we will evaluate the performance of score by precision, recall and f1-score.

<strong>Precision</strong> (a.k.a positive predictive value) is the fraction of relevant instances among the retrieved instances.

<strong>Recall </strong> (a.k.a sensitivity) is the fraction of relevant instances that have been retrieved over the total amount of relevant instances.

|                  |  precision |   recall|  f1-score|   support|
|------------------|:----------:|:-------:|:--------:|:---------|
|       Charged Off|       1.00 |     1.00|      1.00|      2161|
|           Current|       1.00 |     1.00|      1.00|    357162|
|           Default|       0.02 |     0.18|      0.04|      1469|
|        Fully Paid|       0.07 |     0.00|     0.00 |    11435 |
|   In Grace Period|       0.00 |     0.00|      0.00|         7|
|            Issued|       0.00 |     0.00|      0.00|       336|
| Late (16-30 days)|       0.91 |     0.77|      0.84|      8990|
|       avg / total|       0.96 |     0.96|      0.96|    381560|

In this multiclass classification problem, we focus on identifying 'bad' loans inclunding default, late, in grace period. Thus we want the classifier with better recall which can identify 'bad' loans accurately from the pool. The above table shows this simple random forest classifier is good at identify late loans. And it can be improved by tuning parameters of trees. Especially, we can consider increase the class weight of 'bad' loans so the model will penalize more on wrong prediction of 'bad' loans.

### Logistic Classifier
This logistic classifier used multinomial form to solve multiclass classification. 

|                  |  precision|   recall | f1-score |  support |
|------------------|:---------:|:--------:|:--------:|:---------|
|       Charged Off|       1.00|      0.14|      0.25|      2128|
|           Current|       0.95|      1.00|      0.97|   356779 |
|           Default|       0.00|      0.00|      0.00|      1494|
|        Fully Paid|       0.96|      0.35|      0.51|     11261|
|   In Grace Period|       0.00|      0.00|      0.00|         9|
|            Issued|       0.00|      0.00|      0.00|       362|
| Late (16-30 days)|       0.00|      0.00|      0.00|      8822|
|Late (31-120 days)|       0.00|      0.00|      0.00|         0|
|       avg / total|       0.92|      0.95|      0.93|    380855|

<img src="/image/roc_curves.png">

Since there is no case of Late(31-120 days) in the test data, the roc of this class is meaningless.
