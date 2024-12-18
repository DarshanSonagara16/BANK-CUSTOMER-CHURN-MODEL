# -*- coding: utf-8 -*-
"""BANK CUSTOMER CHURN MODEL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uIM4tGbATPzGF2ZHFmmeVC-h-cC-0xAM

LEARN OBJECTIVE

1. DATA ENCODING
2. FEATURE SCALING
3. HANDLING LMBALANCE DATA

    A. RANDOM UNDER SAMPLING

    B. RANDOM OVER SAMPLING
4. SUPPORT VECTOR MACHINE CLASSIFIER
5. GRIED SEARCH FOR HYPERPARAMETER TUNNING
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/Bank Churn Modelling.csv')

df

df.head()

df.info()

df.isnull()

df.isnull().sum()

df.duplicated('CustomerId').sum()

df = df.set_index('CustomerId')

df.info()

"""ENCODING"""

df['Geography'].value_counts()

df.replace({'Geography':{'France' : 2 ,'Germany' : 1 , 'Spain' : 0}}, inplace = True)

df['Gender'].value_counts()

df.replace({'Gender':{'Female' : 1 , 'Male' : 0}}, inplace = True)

df['Num Of Products'].value_counts()

df.replace({'Num Of Products':{1 : 0 , 2 : 1 , 3 : 1 , 4 : 1}}, inplace = True)

df['Has Credit Card'].value_counts()

df['Is Active Member'].value_counts()

df.loc[(df['Balance']==0), 'Churn'].value_counts()

df['Zero Balance'] = np.where(df['Balance']>0,1,0)

df['Zero Balance'].hist()

df.groupby(['Churn','Geography']).count()

"""DEFINE LABEL AND FEATURES"""

df.columns

X = df.drop(['Surname','Churn'], axis = 1)

y = df['Churn']

X.shape , y.shape

"""HANDLING LMBALANCE DATA

CLASS LMBALANCE IS A COMMON PROBLEM IN KACHINE LEARNING , ESPECIALLY IN CLASSIFICATION PROBLAMS AS MACHINE LEARNING ALGORITHEM ARE DESIGN TO MAXIMIZE ACCURACY AND REDUCE ERRORS. IF THE DATA SET IS IMBALANCE THEN IN  SUCH CASES,JUST BY PRIDICT THE MAJORITY CLASS WE GET A PRETTY HIGH ACCURACY , BUT FAILS TO CAPTURE THE MINORITY CLASS, WHICH IS MOST OFTEN THE POINT OF CREATING THE MODEL IN THE FIRST PLACE. LIKE IN
  1. FRAUD DETECTION
  2. SPAM FILTERING
  3. DISEASE SCREENING
  4. ONLINE SALES CHURN
  5. ADVANCE CLICK-THROUGHS

UNDERSAMPLING CAN BE DEFINED AS REMOVING SOME OBSERVATION OF THE MAJORITY CLASS. THIS IS DONE UNTIL THE MJORITY AND MINORITY CLASS IS BLANCED OUT.

UNDERSAMPLING CAN BE A GOOD CHOICE WHEN YOU HAVE A TON OF DATA-THINK MILLIONS OF ROWS.BUT A DRAW BACK TO UNDERSAMPLING IS THAT WE ARE REMOVING INFORMATION THAT MAY BE VALUABLE.

IN UNDER-SAMPLING, THE SIMPLEST TECHNIQUE INVOLVE REMOVING RANDOM RECORDS FROM THE MAJORITY CLASS, WHIVH CAN CAUSE LOSS OF INFORMATION.

A DRAWBACK TO CONSIDER WHEN UNDERSAMPLING IS THAT IT CAN CAUSE OVERFITTING AND POOR GENRALIZATION TO YOUR TEST SET.

OVERSAMPLING CAN BE DEFINE AS ADDING MORE COPIES TO THE MINORITY CLASS. OVERSAMPLING CAN BE A GOOD CHOICE WHEN YOU DON'T HAVE A TON OF DATA TO WORK WITH.

THE SIMPLEST IMPLEMENTATION OF OVER-SAMPLING IS THE TO DUPLICATE RANDOM RECORD FROM THE MINORITY CLASS,WHICH CAN CAUSE OVERFITING




"""

df['Churn'].value_counts()

sns.countplot(x = 'Churn', data = df);

X.shape , y.shape

"""RANDOM UNDER SAMPLING"""

from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state = 2529)

X_rus , y_rus = rus.fit_resample(X,y)

X_rus.shape , y_rus.shape , X.shape , y.shape

y.value_counts()

y_rus.value_counts()

y_rus.plot(kind = 'hist')

"""RANDOM OVER SAMPLING"""

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state = 2529)

X_ros , y_ros = ros.fit_resample(X,y)

X_ros.shape , y_ros.shape , X.shape , y.shape

y.value_counts()

y_ros.value_counts()

y_ros.plot(kind = 'hist')

"""Train Test Split"""

from sklearn.model_selection import train_test_split

"""Split Original Data"""

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 2529)

"""Split Random Under Sample Data"""

X_train_rus, X_test_rus, y_train_rus, y_test_rus = train_test_split(X_rus,y_rus, test_size = 0.3, random_state = 2529)

"""Split Random Over Sample Data"""

X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)

"""STANDARDIZE FEATURE"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

"""STANDARDIZE ORIGINAL DATA"""

X_train[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_train[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

X_test[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_test[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

"""STANDARDIZE RANDOM UNDER SAMPLE DATA"""

X_train_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_train_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

X_test_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_test_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

"""STANDERDIZE RANDOM OVER SAMPLE DATA"""

X_train_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_train_rus[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

X_test_ros[['CreditScore','Age','Tenure','Balance','Estimated Salary']] = sc.fit_transform(X_test_ros[['CreditScore','Age','Tenure','Balance','Estimated Salary']])

"""SUPPORT VECTOR MACHINE CLASSIFIER"""

from sklearn.svm import SVC

svc = SVC()

svc.fit(X_train, y_train)

y_pred = svc.predict(X_test)

"""MODEL ACCURACY"""

from sklearn.metrics import confusion_matrix, classification_report

confusion_matrix(y_test, y_pred)

print(classification_report(y_test, y_pred))

"""HYPERPARAMETER TUNNING"""

from sklearn.model_selection import GridSearchCV

param_grid = {'C' : [0.1 , 1 , 10],
              'gamma' :[1 , 0.1 , 0.01],
              'kernel' : ['rbf'],
              'class_weight': ['balanced']}

grid = GridSearchCV(SVC(),param_grid, refit = True,verbose = 2,cv = 2)
grid.fit(X_train, y_train)

print(grid.best_estimator_)

grid_predictions = grid.predict(X_test)

confusion_matrix(y_test, grid_predictions)

print(classification_report(y_test, grid_predictions))

"""MODEL WITH RANDOM UNDER SAMPLING"""

from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_train_rus, y_train_rus = rus.fit_resample(X_train, y_train)

print(X_train_rus.shape, y_train_rus.shape)

svc_rus = SVC()

svc_rus.fit(X_train_rus, y_train_rus)

y_pred_rus = svc_rus.predict(X_test_rus)

"""MODEL ACCURACY"""

from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_train_rus, y_train_rus = rus.fit_resample(X_train, y_train)

from sklearn.svm import SVC

svc_rus = SVC()
svc_rus.fit(X_train_rus, y_train_rus)

y_pred_rus = svc_rus.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_test, y_pred_rus)
print("Confusion Matrix:\n", cm)

print("Classification Report:\n", classification_report(y_test, y_pred_rus))

"""HYPERPARAMETER TUNNING"""

param_grid = {'C' : [0.1 , 1 , 10],
              'gamma' :[1 , 0.1 , 0.01],
              'kernel' : ['rbf'],
              'class_weight': ['balanced']}

grid_rus = GridSearchCV(SVC(),param_grid, refit = True,verbose = 2,cv = 2)
grid_rus.fit(X_train_rus, y_train_rus)

print(grid_rus.best_estimator_)

grid_predictions_rus = grid_rus.predict(X_test_rus)

confusion_matrix(y_test_rus, grid_predictions_rus)

print(classification_report(y_test_rus, grid_predictions_rus))

"""Model with random over sampling"""

svc_ros = SVC()

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=42)
X_train_ros, y_train_ros = ros.fit_resample(X_train, y_train)

print("X_train_ros shape:", X_train_ros.shape)
print("y_train_ros shape:", y_train_ros.shape)

svc_ros.fit(X_train_ros, y_train_ros)

y_pred_ros = svc_ros.predict(X_test_ros)

"""Model Accuracy"""

confusion_matrix(y_test_ros, y_pred_ros)

# Previous line with the error:
#X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)

# Corrected line:
X_train_ros, X_test_ros, y_train_ros, y_test_ros = train_test_split(X_ros, y_ros, test_size=0.3, random_state=2529) # Corrected the variable names to assign the oversampled test data correctly

"""HYPERPARAMETER TUNNING"""

param_grid = {'C' : [0.1 , 1 , 10],
              'gamma' :[1 , 0.1 , 0.01],
              'kernel' : ['rbf'],
              'class_weight': ['balanced']}

grid_ros = GridSearchCV(SVC(),param_grid, refit = True,verbose = 2,cv = 2)
grid_ros.fit(X_train_ros, y_train_ros)

print(grid_ros.best_estimator_)

grid_predictions_ros = grid_ros.predict(X_test_ros)

X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)

# Previous line with the error:
#X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)

# Corrected line:
X_train_ros, X_test_ros, y_train_ros, y_test_ros = train_test_split(X_ros, y_ros, test_size=0.3, random_state=2529) # Corrected the variable names to assign the oversampled test data correctly

"""LETS COMPARE"""

print(classification_report(y_test, y_pred))

print(classification_report(y_test,grid_predictions))

# Previous code with the error:
#y_pred_rus = svc_rus.predict(X_test_rus)
#from sklearn.metrics import confusion_matrix, classification_report
#cm = confusion_matrix(y_test, y_pred_rus)

# Corrected code:
y_pred_rus = svc_rus.predict(X_test)  # Predict on the original test data (X_test)
from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_test, y_pred_rus) # Compare with the original test labels (y_test)

# Assuming X_rus and y_rus are your under-sampled data
X_train_rus, X_test_rus, y_train_rus, y_test_rus = train_test_split(X_rus, y_rus, test_size=0.3, random_state=2529)

# Fit the model with under-sampled training data
grid_rus = GridSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=2)
grid_rus.fit(X_train_rus, y_train_rus)

# Predict on the under-sampled test data
grid_predictions_rus = grid_rus.predict(X_test_rus) # Changed from X_test to X_test_rus

# Generate the classification report using the under-sampled test data and predictions
print(classification_report(y_test_rus, grid_predictions_rus)) # Changed from grid_rus to grid_predictions_rus

# Previous line with the error:
#X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)

# Corrected line:
X_train_ros, X_test_ros, y_train_ros, y_test_ros = train_test_split(X_ros, y_ros, test_size=0.3, random_state=2529) # Corrected the variable names to assign the oversampled test data correctly

X_tarin_ros, X_test_ros, y_train_rus, y_test_rus = train_test_split(X_ros,y_ros, test_size = 0.3, random_state = 2529)