# Lending-Club-Data-Analysis
## Data Source
<li> <strong>Loan Statistics</strong>: panal data. These files contain complete loan data for all loans issued through the time period stated. </li>
<li><strong>Payment Historical Data</strong>: time series of payment and balance of loans.</li> 

The first data set is of size (1646779, 151) including 1646779  loans and 150 features from 2007 to 2016 Q3. The second data set with payment history is of size (3790864, 40) including 134966 loans and 39 features. To enrich the data set and keep the time information, I combined two data sets together and got features and payment history of 92431 loans. 

The problem we are intersted is the loan status. In this data set, there are 8 kinds of status related to the loan: Current, Fully Paid, Issued, In Grace Period, Late(16-30 days), Late(31-120 days), Defualt, Charged off. We want to model the probability of transition from one status to another. Thus it will be a multi-label classification problem. 

## Data Processing
There are 166 features at the beginning. However, the data is not complete and we should check missing values first. Then we need to figure out why the data is missing and make adjustment.

<img src="/image/missing_value_dist.png">

1. Records related to settlement are absent for 99.09%. Settlement is a plan for borrower who gets charged off. Therefore, only loans charged off keep this record. Since settlement is the consequence of charged off, data related to it should not be considered as feature that can classify loan status. Thus I dumped 7 features related to settlement.

2. Records related to hardship plan are missing for 99.96%. Since there is only one loan with hardship plan features, I decided to abondon the 15 colomns of data related to hardship plan.

3. Data related to date. There are several data such as 'issue_d', 'next_pymnt_d' in the format of time stamp. However, most of this time data come from Loan Statistics -- the panel data. It turns out missing when we expend the time line. Furthermore, most of them seem extra since they have nothing to do with the loan payment like 'next_pymnt_d' (next payment date). Thus I removed these kind of data. A few other time data can be used in relative value, ie. the difference of 'issue_d' (issue_date) and 'MONTH' represents the age of loan (it turned out the same as MOB in the data set which has no definition). I kept the calculated value and dumped the original values. 

4. The rest of missing value cannot be removed directly since we do not know the reason of missing. Thus I created dummy variables to indicate whether the data is missing and treated them as new features.

5. Convert categorical variable (string) into numbers. Yet here is the exception. The feature 'emp_title' means employment title where the input varies from case to case. Thus it is not reasonable to keep a categorical variable of 64712 levels. The similar features includes 'desc'(description), 'url', 'zip_code'. One way to solve this problem is to use dummy variable to indiate whethere the data entry exsits.

## Data Exploration
### Response Variable -- Loan Status
Most of the loans are current and fully paid. The late and default loans are in small proportion thus this is an unbalanced case. We should consider set class_weight to improve the model performance in the future.

<img src="/image/loan_status_dist.png.png">
