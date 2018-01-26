# Lending-Club-Data-Analysis
## Data Source
<li> <strong>Loan Statistics</strong>: panal data. These files contain complete loan data for all loans issued through the time period stated. </li>
<li><strong>Payment Historical Data</strong>: time series of payment and balance of loans.</li> 

The first data set is of size (1646779, 151) including 1646779  loans and 150 features from 2007 to 2016 Q3. The second data set with payment history is of size (3790864, 40) including 134966 loans and 39 features. To enrich the data set and keep the time information, I combined two data sets together and got features and payment history of 92431 loans. 

The problem we are intersted is the loan status. In this data set, there are 8 kinds of status related to the loan: Current, Fully Paid, Issued, In Grace Period, Late(16-30 days), Late(31-120 days), Defualt, Charged off. We want to model the probability of transition from one status to another. Thus it will be a multi-label classification problem. 

First, take a look at the distribution of loan status.
![alt text](https://github.com/tongkewu/Lending-Club-Data-Analysis/master/images/loan_status.png "Loan Status")
