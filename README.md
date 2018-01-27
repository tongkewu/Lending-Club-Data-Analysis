# Lending-Club-Data-Analysis
## Data Source
<li> <strong>Loan Statistics</strong>: panal data. These files contain complete loan data for all loans issued through the time period stated. </li>
<li><strong>Payment Historical Data</strong>: time series of payment and balance of loans.</li> 

The first data set is of size (1646779, 151) including 1646779  loans and 150 features from 2007 to 2016 Q3. The second data set with payment history is of size (3790864, 40) including 134966 loans and 39 features. To enrich the data set and keep the time information, I combined two data sets together and got features and payment history of 92431 loans. 

The problem we are intersted is the loan status. In this data set, there are 8 kinds of status related to the loan: Current, Fully Paid, Issued, In Grace Period, Late(16-30 days), Late(31-120 days), Defualt, Charged off. We want to model the probability of transition from one status to another. Thus it will be a multi-label classification problem. 

## Data Processing
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

Finally, we got a complete data set. 

## Data Exploration
### Response Variable -- Loan Status
Most of the loans are current and fully paid. The late and default loans are in small proportion thus this is an unbalanced case. We should consider set class_weight to improve the model performance in the future.

<img src="/image/loan_status_dist.png">

## Modeling
### Random Forest Classifier

<img src="/image/feature_importance.png">

|                    | precision | recall | f1-score | support |
|--------------------|:---------:|:------:|:--------:|:--------|
| Charged off        |      1.00 |   0.99 |     0.99 |    1098 |
| Current            |      1.00 |   1.00 |     1.00 |  178698 |
| Default            |     0.00  |  0.01  |  0.00    |     770 |
| Fully Paid         |      0.89 |  0.81  |    0.85  |    5583 |
| In Grace Period    |   0.00    |  0.00  |    0.00  |       5 |
| Issued             |    0.00   |   0.00 |    0.00  |     0   |
| Late (16-30 days)  |    0.02   |  0.46  |  0.04    |    165  |
| Late (31-120 days) |    0.00   |  0.00  |   0.00   |   4461  |
| avg / total        |    0.97   |   0.96 |    0.97  |  190780 |

### Logistic Classifier

|                   | precision |   recall | f1-score |  support|
|-------------------|:----------|:---------|:---------|:--------|
|       Charged Off |      1.00 |     1.00 |     1.00 |     1098|
|           Current |      0.99 |     1.00 |     0.99 |   178698|
|           Default |      0.88 |     0.24 |     0.37 |      770|
|        Fully Paid |      0.98 |     0.97 |     0.97 |     5583|
|   In Grace Period |      0.00 |     0.00 |     0.00 |        5|
|            Issued |      0.00 |     0.00 |     0.00 |        0|
| Late (16-30 days) |      0.00 |     0.00 |     0.00 |      165|
|Late (31-120 days) |      0.83 |     0.66 |     0.74 |     4461|
|       avg / total |      0.98 |     0.99 |     0.98 |   190780|
