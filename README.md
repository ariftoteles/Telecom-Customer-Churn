# Final-Project-Telecom-Customer-Churn
<h3>About Customer Churn</h3>
<hr>

Customer Churn is the number or presentation of customers who stop using a product or unsubscribe during a certain period, this is caused by customer dissatisfaction, cheaper offers from competitors, better marketing by competitors, or other causes.

In a growing business, the cost of getting new customers is far greater than the cost of keeping existing customers. Customer churn impact on lossing revenue and company's reputation, in such a position it is more difficult to get new customers.

<h3>Purpose</h3>
<hr>

1. Analyze what factors have the potential to cause customers churn
2. Build Machine Learning Model to predict customers churn

<h3>Dataset</h3>
<hr>

The dataset provide by [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn) to analyze and predict customer churning. The dataset is a sample data from IBM consists of 7043 samples and 21 columns with the following description:
- __customerID:__ Customer ID
- __gender:__ Whether the customer is a male or a female
- __SeniorCitizen:__ Whether the customer is a senior citizen or not (Yes, No)
- __Partner:__ Whether the customer has a partner or not (Yes, No)
- __Dependents:__ Whether the customer has dependents or not (Yes, No)
- __tenure:__ Number of months the customer has stayed with the company
- __PhoneService:__ Whether the customer has a phone service or not (Yes, No)
- __MultipleLines:__ Whether the customer has multiple lines or not (Yes, No, No phone service)
- __InternetService:__ Customer’s internet service provider (DSL, Fiber optic, No)
- __OnlineSecurity:__ Whether the customer has online security or not (Yes, No, No internet service)
- __OnlineBackup:__ Whether the customer has online backup or not (Yes, No, No internet service)
- __DeviceProtection:__ Whether the customer has device protection or not (Yes, No, No internet service)
- __TechSupport:__ Whether the customer has tech support or not (Yes, No, No internet service)
- __StreamingTV:__ Whether the customer has streaming TV or not (Yes, No, No internet service)
- __StreamingMovies:__ Whether the customer has streaming movies or not (Yes, No, No internet service)
- __Contract:__ The contract term of the customer (Month-to-month, One year, Two year)
- __PaperlessBilling:__ Whether the customer has paperless billing or not (Yes, No)
- __PaymentMethod:__ The customer’s payment method (Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic))
- __MonthlyCharges:__ The amount charged to the customer monthly
- __TotalCharges:__ The total amount charged to the customer
- __Churn:__ Whether the customer churned or not (Yes or No)

<h3>Model Prediction</h3>
<hr>

Build Supervised Machine Learning with 4 algorithm
- Logisitic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors methods.

Since the dataset is imbalance, I used 4 Experiment :

- Training models use the Imbalance dataset
- Training model use a balance dataset (Under Sample)
- Training model use a balance dataset (Random Over Sample)
- Training model use a balance dataset (SMOTE)

Best Model:

- Because we used imbalance dataset, evaluation matrics based on Recall,F1 Score, and AUC Score
- Logistic Regression who train used a balance dataset (Random Over Sample) get highest Recall, F1 Score and AUC Score

<h3>Model Interface</h3>
<hr>

__Home Page__
 ![home](./MyWebsite.png)
 
 <hr>
__Analysis__
 ![Analysis](./Analysis.png)

<hr>
__Form Prediction__
 ![Predict](./Predict.png)

<hr>
__Result__
 ![result](./result.png)

