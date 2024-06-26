# -*- coding: utf-8 -*-
"""Wine_Quality_Prediction.ipynb

Automatically generated by Colab.

Install the ucimlrepo (https://github.com/uci-ml-repo/ucimlrepo)
"Package to easily import datasets from the UC Irvine Machine Learning Repository into scripts and notebooks." (description from their github repo)
This is the command to install in a Jupyter notebook.
"""

# !pip3 install -U ucimlrepo

# # Upgrade libraries to latest versions
# !pip3 install -U scikit-learn
# !pip3 install -U pandas
# !pip3 install -U numpy
# !pip3 install -U matplotlib
# !pip3 install -U seaborn

"""### Dataset:
Cortez,Paulo, Cerdeira,A., Almeida,F., Matos,T., and Reis,J.. (2009). Wine Quality. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T.
"""

from ucimlrepo import fetch_ucirepo
from IPython.display import display

# fetch dataset
wine_quality = fetch_ucirepo(id=186)

# data (as pandas dataframes)
X = wine_quality.data.features
y = wine_quality.data.targets

# metadata
print(wine_quality.metadata)



# variable information
print(wine_quality.variables)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#print(X.head())
Xy = pd.concat([X, y], axis=1)
display(Xy)

Xy.describe()

y.describe()

Xy.info()

sns.pairplot(Xy, vars=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
                             'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'quality'])

sns.countplot(x=Xy['quality'], label='Count')

plt.bar(Xy['quality'], Xy['alcohol'])
plt.xlabel('quality')
plt.ylabel('alcohol')
plt.show()

# Check correlation between variables
plt.figure(figsize=(20,10))
sns.heatmap(Xy.corr(), annot=True)

"""## Model Training
Trying to find what factors best contribute to wine quality.
"""

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# X is the pandas dataframe for wine_quality.data.features
# y is the wine_quality.data.targets



print(f"'X' shape: {X.shape}")
print(f"'y' shape: {y.shape}")

pipeline = Pipeline([
    ('min_max_scaler', MinMaxScaler()),
    ('std_scaler', StandardScaler())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"'X_train' shape: {X_train.shape}")
print(f"'X_test' shape: {X_test.shape}")
print(f"'y_trian' shape: {y_train.shape}")
print(f"'y_test' shape: {y_test.shape}")

"""Function to format results for any support vector machine kernel type."""

from sklearn.metrics import accuracy_score, classification_report

def print_score(clf, X_train, y_train, X_test, y_test, train=True):
    if train:
        pred = clf.predict(X_train)
        accuracy = accuracy_score(y_train, pred)
        error_rate = 1 - accuracy
        clf_report = pd.DataFrame(classification_report(y_train, pred, output_dict=True, zero_division=0))
        print("==================== Train Result ============================")
        print(f"Accuracy Score: {accuracy * 100:.2f}%")
        print("_______________________________________________")
        print(f"Error Rate: {error_rate * 100:.2f}%")
        print("_______________________________________________")
        print(f"CLASSIFICATION REPORT:\n{clf_report}\n")

    elif train==False:
        pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, pred)
        error_rate = 1 - accuracy
        clf_report = pd.DataFrame(classification_report(y_test, pred, output_dict=True, zero_division=0))
        print("==================== Train Result ============================")
        print(f"Accuracy Score: {accuracy * 100:.2f}%")
        print("_______________________________________________")
        print(f"Error Rate: {error_rate * 100:.2f}%")
        print("_______________________________________________")
        print(f"CLASSIFICATION REPORT:\n{clf_report}")

"""## Support Vector Machines (SVM)
### Kernels and Kernel Parameters
- C: float, default value = 1.0
  - Regularization parameter and it's strenght is inversely proprtional to C. Controls the adjustment between a decision boundary that's smooth versus classifying training points. Small C value has a low penalty for misclassification (soft margin). Large C value has a high penalty for misclassification (hard margin).
- kernel: {‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’} or callable, default = ’rbf’
  - The kernel type that is going to be used in the algorithm.
- degree: int, default value = 3
  - Degree of the polynomial kernel function (‘poly’). Ignored by all other kernels. Can not be a negative value.
- gamma: {‘scale’, ‘auto’} or float, default=’scale’
  - For a large gamma value, there's a high weight on the closer data points. For a small gamma value, the solution is more generalized.

## Linear Kernel SVM
"""

from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler

# Preprocess data first, standardized features
#scaler = StandardScaler()
#X_train = scaler.fit(X_train).transform(X_train)
#X_test = scaler.fit(X_test).transform(X_test)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Column-vector y needs to be a 1d array and change continuous value as int
#y = y_train.ravel()
y_train = np.array(y_train).astype(int)
#y_train = scaler.fit(y_train).transform(y_train)
#yt = y_test.ravel()
y_test = np.array(y_test).astype(int)
#y_test = scaler.fit(y_test).transform(y_test)

model = LinearSVC(loss='hinge', dual=True, max_iter=1_100)
y_train = y_train.squeeze()
y_test = y_test.squeeze()
model.fit(X_train, y_train)


print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

"""## Polynomial Kernel SVM"""

from sklearn.svm import SVC

# The hyperparameter coef0 controls how much the model is influenced by high degree ploynomials
model = SVC(kernel='poly', degree=2, gamma='auto', coef0=1, C=5)
model.fit(X_train, y_train)

print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

"""## Radial Kernel SVM"""

model = SVC(kernel='rbf', gamma=0.5, C=0.1)
model.fit(X_train, y_train)

print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

"""## Data Preparation with SVM"""

X_train = pipeline.fit_transform(X_train)
X_test = pipeline.transform(X_test)

print("=======================Linear Kernel SVM==========================")
model = SVC(kernel='linear')
model.fit(X_train, y_train)

print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

print("=======================Polynomial Kernel SVM==========================")
from sklearn.svm import SVC

model = SVC(kernel='poly', degree=2, gamma='auto')
model.fit(X_train, y_train)

print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

print("=======================Radial Kernel SVM==========================")
from sklearn.svm import SVC

model = SVC(kernel='rbf', gamma=1)
model.fit(X_train, y_train)

print_score(model, X_train, y_train, X_test, y_test, train=True)
print_score(model, X_train, y_train, X_test, y_test, train=False)

"""## Support Vector Machine Hyperparameter Tuning"""

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

param_grid = {'C': [0.1, 1, 10],
              'gamma': [1, 0.75, 0.5],
              'kernel': ['rbf', 'poly', 'linear']}

#grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=1, cv=4)
grid = RandomizedSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=4, n_iter=3, random_state=23)
grid.fit(X_train, y_train)

best_params = grid.best_params_
print(f"Best params: {best_params}")

svm_clf = SVC(**best_params)
svm_clf.fit(X_train, y_train)
print_score(svm_clf, X_train, y_train, X_test, y_test, train=True)
print_score(svm_clf, X_train, y_train, X_test, y_test, train=False)

"""## Principal Component Analysis (PCA)
- Using Singular Value Decomposition, project data to a lower dimensional space. In other words, linear dimentionality reduction.
- Unsupervised.
- See what feature(s) contribute to the most variance by transforming our data.
"""

scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.decomposition import PCA

pca = PCA(n_components=3)
scaler = StandardScaler()

X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

plt.figure(figsize=(8,6))
plt.scatter(X_train[:,0],X_train[:,1], c=y_train.squeeze(), cmap='plasma')
plt.xlabel('First principal component')
plt.ylabel('Second Principal Component')

"""## Components interpreting"""

param_grid = {'C': [1, 10, 100],
              'gamma': [1, 0.1, 0.01],
              'kernel': ['rbf', 'poly', 'linear']}

#grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=1, cv=4)
grid = RandomizedSearchCV(SVC(), param_grid, refit=True, verbose=2, cv=4, n_iter=3, random_state=30)
grid.fit(X_train, y_train.squeeze())
best_params = grid.best_params_
print(f"Best params: {best_params}")

svm_clf = SVC(**best_params)
svm_clf.fit(X_train, y_train.squeeze())

print_score(svm_clf, X_train, y_train, X_test, y_test, train=True)
print_score(svm_clf, X_train, y_train, X_test, y_test, train=False)
