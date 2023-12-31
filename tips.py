# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:14:20 2023

@author: rahul
"""
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

# Load the dataset into a pandas dataframe
tips_df = pd.read_csv(r"C:\Users\jtrah\Downloads\tips.csv")

tips_df = pd.get_dummies(tips_df, columns=['sex','smoker','time'], drop_first=True)
tips_df = pd.get_dummies(tips_df, columns=['day'])
# Split the dataset into predictors (X) and response variable (y)
X = tips_df.drop(['tip'], axis=1)
y = tips_df['tip']

# Split the data into training and testing sets with an 80-20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# Print the size of the training and testing sets
print("Size of training set:", len(X_train))
print("Size of testing set:", len(X_test))



# Split the dataset into training and testing sets
train_data = tips_df.sample(frac=0.8, random_state=10)
test_data = tips_df.drop(train_data.index)

# Calculate the correlation coefficient between total_bill and tip
corr_coef = train_data['total_bill'].corr(train_data['tip'])

# Print the correlation coefficient
print("Correlation coefficient between total_bill and tip:", corr_coef)

# Plot scatter plots of all predictors against tip
sns.scatterplot(x="total_bill", y="tip", data=train_data)
sns.scatterplot(x="sex_Male", y="tip", data=train_data)
sns.scatterplot(x="day_Thur", y="tip", data=train_data)
sns.scatterplot(x="day_Fri", y="tip", data=train_data)
sns.scatterplot(x="day_Sat", y="tip", data=train_data)
sns.scatterplot(x="day_Sun", y="tip", data=train_data)
sns.scatterplot(x="time_Lunch", y="tip", data=train_data)
sns.scatterplot(x="size", y="tip", data=train_data)

#print(tips_df.columns)
# Define the predictors and response variable
X_train = train_data[['total_bill', 'size', 'sex_Male', 'smoker_Yes',
       'time_Lunch', 'day_Fri', 'day_Sat', 'day_Sun', 'day_Thur']]
y_train = train_data['tip']

# Add a constant to the predictors to fit the intercept term
X_train = sm.add_constant(X_train)

# Fit the multiple linear regression model
model = sm.OLS(y_train, X_train).fit()

# Print the model summary
print(model.summary())


# Make predictions on train and test data
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Calculate the mean squared error on train and test data
mse_train = mean_squared_error(y_train, y_train_pred)
mse_test = mean_squared_error(y_test, y_test_pred)

# Calculate the R-squared value on train and test data
r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)

# Print the MSE and R-squared values on train and test data
print("MSE on train data:", mse_train)
print("MSE on test data:", mse_test)

print("R2 on train data:", r2_train)
print("R2 on test data:", r2_test)

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

# Define the range of polynomial orders to try
orders = [1, 2, 3, 4]

# Create an empty list to store the cross validation scores for each order
cv_scores = []

# Loop over the range of polynomial orders
for order in orders:
    # Create a pipeline that includes polynomial features and linear regression
    model = make_pipeline(PolynomialFeatures(order), LinearRegression())
    # Compute the cross validation scores for this order using mean squared error as the scoring metric
    scores = -1 * cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    # Append the average score to the list of scores
    cv_scores.append(np.mean(scores))
    # Print the order and the average score for this order
    print(f"Polynomial order: {order}, Mean Squared Error: {np.mean(scores)}, R2 score: {np.mean(cross_val_score(model, X_train, y_train, cv=5))}")


from sklearn.preprocessing import PolynomialFeatures
X_test = sm.add_constant(X_test)
X_test = X_test.drop(['Serialno'], axis=1)

# create polynomial features with degree 2
poly = PolynomialFeatures(degree=2)

# fit and transform the train data with the polynomial features
X_poly_train = poly.fit_transform(X_train)

# create the polynomial regression model and fit it to the train data
poly_reg = LinearRegression()
poly_reg.fit(X_poly_train, y_train)

# transform the test data with the polynomial features
X_poly_test = poly.transform(X_test)

# evaluate performance on train and test data
y_pred_train = poly_reg.predict(X_poly_train)
y_pred_test = poly_reg.predict(X_poly_test)

mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)

r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print("MSE on train data:", mse_train)
print("MSE on test data:", mse_test)
print("R2 on train data:", r2_train)
print("R2 on test data:", r2_test)

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Split data into train and test sets
train_data = tips_df.sample(frac=0.8, random_state=10)
test_data = tips_df.drop(train_data.index)

# Separate predictors and response variable in train and test data
X_train = train_data.drop('tip', axis=1)
y_train = train_data['tip']
X_test = test_data.drop('tip', axis=1)
y_test = test_data['tip']

# Fit Decision Tree model
dt = DecisionTreeRegressor(random_state=10)
dt.fit(X_train, y_train)

# Evaluate performance on train and test data
y_train_pred = dt.predict(X_train)
mse_train = mean_squared_error(y_train, y_train_pred)
r2_train = r2_score(y_train, y_train_pred)
print("MSE on train data:", mse_train)
print("R2 on train data:", r2_train)

y_test_pred = dt.predict(X_test)
mse_test = mean_squared_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)
print("MSE on test data:", mse_test)
print("R2 on test data:", r2_test)

# Print height of Decision Tree
print("Height of Decision Tree:", dt.get_depth())

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

# Define the decision tree model
model = DecisionTreeRegressor()

# Define the hyperparameters to search over
params = {'ccp_alpha': [0.0, 0.001, 0.01, 0.1, 1.0]}

# Perform cross-validation to find the best value of alpha
grid = GridSearchCV(model, params, cv=5, scoring='neg_mean_squared_error')
grid.fit(X_train, y_train)

# Print the best value of alpha and the corresponding cross-validation score
print('Best alpha:', grid.best_params_['ccp_alpha'])
print('CV score:', -grid.best_score_)

# Build the pruned model with the best value of alpha
pruned_model = DecisionTreeRegressor(ccp_alpha=grid.best_params_['ccp_alpha'])
pruned_model.fit(X_train, y_train)

# Evaluate performance on train and test data
train_pred = pruned_model.predict(X_train)
test_pred = pruned_model.predict(X_test)
train_mse = mean_squared_error(y_train, train_pred)
test_mse = mean_squared_error(y_test, test_pred)
train_r2 = r2_score(y_train, train_pred)
test_r2 = r2_score(y_test, test_pred)
print('MSE on train data:', train_mse)
print('MSE on test data:', test_mse)
print('R2 on train data:', train_r2)
print('R2 on test data:', test_r2)

from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Set up the bagging model with decision tree as the base estimator
bagging = BaggingRegressor(base_estimator=DecisionTreeRegressor())

# Define the range of hyperparameters to search over
param_grid = {'n_estimators': [10, 20, 30, 40, 50, 70, 100, 300, 500]}

# Perform grid search with 5-fold cross validation
grid_search = GridSearchCV(bagging, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Print the best parameter and its corresponding cross-validation score
print("Best parameter: ", grid_search.best_params_)
print("Cross-validation score: ", grid_search.best_score_)

# Train the bagging model on the entire train data using the best hyperparameter value
bagging = BaggingRegressor(base_estimator=DecisionTreeRegressor(), n_estimators=grid_search.best_params_['n_estimators'])
bagging.fit(X_train, y_train)

# Evaluate performance on train data
y_train_pred = bagging.predict(X_train)
train_mse = mean_squared_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)
print("MSE on train data:", train_mse)
print("R2 on train data:", train_r2)

# Evaluate performance on test data
y_test_pred = bagging.predict(X_test)
test_mse = mean_squared_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)
print("MSE on test data:", test_mse)
print("R2 on test data:", test_r2)


from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

# Define the base estimator
base_estimator = DecisionTreeRegressor(max_depth=1)

# Define the parameter grid
param_grid = {'n_estimators': [10, 20, 30, 40, 50, 70, 100, 300, 500]}

# Perform 5-fold cross validation to find the best value of num_trees
grid_search = GridSearchCV(AdaBoostRegressor(base_estimator=base_estimator),
                           param_grid=param_grid,
                           cv=5,
                           scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Print the results of cross validation
for i, score in enumerate(grid_search.cv_results_['mean_test_score']):
    print(f"num_trees = {param_grid['n_estimators'][i]}, MSE = {-score}")

# Get the best value of num_trees
num_trees = grid_search.best_params_['n_estimators']

# Train the AdaBoost model on the training data with the best value of num_trees
ada_boost_model = AdaBoostRegressor(base_estimator=base_estimator, n_estimators=num_trees)
ada_boost_model.fit(X_train, y_train)

# Evaluate performance on train and test data
train_preds = ada_boost_model.predict(X_train)
test_preds = ada_boost_model.predict(X_test)

train_mse = mean_squared_error(y_train, train_preds)
test_mse = mean_squared_error(y_test, test_preds)

train_r2 = r2_score(y_train, train_preds)
test_r2 = r2_score(y_test, test_preds)

print(f"MSE on train data: {train_mse}")
print(f"MSE on test data: {test_mse}")
print(f"R2 on train data: {train_r2}")
print(f"R2 on test data: {test_r2}")

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np

# Define the range of values for num_trees and num_features
num_trees_range = [10, 20, 30, 40, 50, 70, 100, 300, 500]
num_features_range = [1, 2, 3]

# Create a dictionary of hyperparameter values to test
param_grid = {'n_estimators': num_trees_range, 'max_features': num_features_range}

# Create a Random Forest model object
rf_model = RandomForestRegressor(random_state=42)

# Create a GridSearchCV object
grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='neg_mean_squared_error')

# Fit the GridSearchCV object to the data
grid_search.fit(X_train, y_train)

# Print results for each combination of hyperparameters
for i in range(len(grid_search.cv_results_['params'])):
    print(f"n_estimators={grid_search.cv_results_['params'][i]['n_estimators']}, "
          f"max_features={grid_search.cv_results_['params'][i]['max_features']}: "
          f"mean_test_score={grid_search.cv_results_['mean_test_score'][i]:.4f}, "
          f"std_test_score={grid_search.cv_results_['std_test_score'][i]:.4f}")


# Print the best hyperparameters
print("Best parameters: ", grid_search.best_params_)

# Train the model with the best hyperparameters on the entire training data
rf_model = RandomForestRegressor(n_estimators=grid_search.best_params_['n_estimators'],
                                  max_features=grid_search.best_params_['max_features'],
                                  random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the performance on train and test data
y_train_pred = rf_model.predict(X_train)
train_mse = mean_squared_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

y_test_pred = rf_model.predict(X_test)
test_mse = mean_squared_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("MSE on train data: {}".format(train_mse))
print("R2 on train data: {}".format(train_r2))
print("MSE on test data: {}".format(test_mse))
print("R2 on test data: {}".format(test_r2))

from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score

# Ridge Regression
alpha_range = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
ridge_scores = []
for alpha in alpha_range:
    ridge_reg = Ridge(alpha=alpha)
    scores = cross_val_score(ridge_reg, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    ridge_scores.append(-1 * scores.mean())

best_alpha_ridge = alpha_range[ridge_scores.index(min(ridge_scores))]

ridge_reg = Ridge(alpha=best_alpha_ridge)
ridge_reg.fit(X_train, y_train)

y_train_pred_ridge = ridge_reg.predict(X_train)
y_test_pred_ridge = ridge_reg.predict(X_test)

print('Ridge Regression:')
print(f'Best alpha: {best_alpha_ridge}')
print(f'MSE on train data: {mean_squared_error(y_train, y_train_pred_ridge)}')
print(f'R2 on train data: {r2_score(y_train, y_train_pred_ridge)}')
print(f'MSE on test data: {mean_squared_error(y_test, y_test_pred_ridge)}')
print(f'R2 on test data: {r2_score(y_test, y_test_pred_ridge)}\n')

# Lasso Regression
alpha_range = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
lasso_scores = []
for alpha in alpha_range:
    lasso_reg = Lasso(alpha=alpha, max_iter=10000)
    scores = cross_val_score(lasso_reg, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    lasso_scores.append(-1 * scores.mean())

best_alpha_lasso = alpha_range[lasso_scores.index(min(lasso_scores))]

lasso_reg = Lasso(alpha=best_alpha_lasso, max_iter=10000)
lasso_reg.fit(X_train, y_train)

y_train_pred_lasso = lasso_reg.predict(X_train)
y_test_pred_lasso = lasso_reg.predict(X_test)

print('Lasso Regression:')
print(f'Best alpha: {best_alpha_lasso}')
print(f'MSE on train data: {mean_squared_error(y_train, y_train_pred_lasso)}')
print(f'R2 on train data: {r2_score(y_train, y_train_pred_lasso)}')
print(f'MSE on test data: {mean_squared_error(y_test, y_test_pred_lasso)}')
print(f'R2 on test data: {r2_score(y_test, y_test_pred_lasso)}')


from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Create polynomial features
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Ridge regression
ridge = Ridge()
ridge_params = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}
ridge_cv = GridSearchCV(ridge, param_grid=ridge_params, cv=5)
ridge_cv.fit(X_train_poly, y_train)

print("Ridge Regression:")
print("Best alpha:", ridge_cv.best_params_['alpha'])

# Train and evaluate Ridge model
ridge_model = make_pipeline(poly, Ridge(alpha=ridge_cv.best_params_['alpha']))
ridge_model.fit(X_train, y_train)
y_pred_train = ridge_model.predict(X_train)
y_pred_test = ridge_model.predict(X_test)

print("MSE on train data:", mean_squared_error(y_train, y_pred_train))
print("R2 on train data:", r2_score(y_train, y_pred_train))
print("MSE on test data:", mean_squared_error(y_test, y_pred_test))
print("R2 on test data:", r2_score(y_test, y_pred_test))

# Lasso regression
lasso = Lasso()
lasso_params = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}
lasso_cv = GridSearchCV(lasso, param_grid=lasso_params, cv=5)
lasso_cv.fit(X_train_poly, y_train)

print("\nLasso Regression:")
print("Best alpha:", lasso_cv.best_params_['alpha'])

# Train and evaluate Lasso model
lasso_model = make_pipeline(poly, Lasso(alpha=lasso_cv.best_params_['alpha']))
lasso_model.fit(X_train, y_train)
y_pred_train = lasso_model.predict(X_train)
y_pred_test = lasso_model.predict(X_test)

print("MSE on train data:", mean_squared_error(y_train, y_pred_train))
print("R2 on train data:", r2_score(y_train, y_pred_train))
print("MSE on test data:", mean_squared_error(y_test, y_pred_test))
print("R2 on test data:", r2_score(y_test, y_pred_test))

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Define the KNN model
knn = KNeighborsRegressor()

# Define the hyperparameters to search over
parameters = {'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]}

# Use 5-fold cross validation to find the best value of K
cv = GridSearchCV(knn, parameters, cv=5)
cv.fit(X_train, y_train)

# Print the best value of K
print("Best K value: ", cv.best_params_['n_neighbors'])

# Train the model with the best value of K
knn = KNeighborsRegressor(n_neighbors=cv.best_params_['n_neighbors'])
knn.fit(X_train, y_train)

# Evaluate performance on train and test data
y_train_pred = knn.predict(X_train)
y_test_pred = knn.predict(X_test)

print("MSE on train data:", mean_squared_error(y_train, y_train_pred))
print("MSE on test data:", mean_squared_error(y_test, y_test_pred))
print("R2 on train data:", r2_score(y_train, y_train_pred))
print("R2 on test data:", r2_score(y_test, y_test_pred))

from sklearn.svm import LinearSVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Define the model
model = LinearSVR(loss='epsilon_insensitive')

# Define the parameter grid
param_grid = {'C': [2**-3, 2**-1, 20, 21, 23]}

# Define the cross-validation object
cv = GridSearchCV(model, param_grid=param_grid, cv=5)

# Fit the cross-validation object to the data
cv.fit(X_train, y_train)

# Get the best value of C
best_C = cv.best_params_['C']
print("Best C:", best_C)

# Train the final model with the best C value
model = LinearSVR(loss='epsilon_insensitive', C=best_C)
model.fit(X_train, y_train)

# Evaluate the model on the train data
train_predictions = model.predict(X_train)
mse_train = mean_squared_error(y_train, train_predictions)
r2_train = r2_score(y_train, train_predictions)
print("MSE on train data:", mse_train)
print("R2 on train data:", r2_train)

# Evaluate the model on the test data
test_predictions = model.predict(X_test)
mse_test = mean_squared_error(y_test, test_predictions)
r2_test = r2_score(y_test, test_predictions)
print("MSE on test data:", mse_test)
print("R2 on test data:", r2_test)

from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Define range of hyperparameters to search over
param_grid = {'C': [10**i for i in range(-3, 3)],
              'gamma': [10**i for i in range(-5, 3)]}

# Create a SVR object
svm_rbf = SVR(kernel='rbf')

# Perform grid search with 5-fold cross-validation to find the best hyperparameters
grid_search = GridSearchCV(svm_rbf, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Print the best hyperparameters and corresponding mean cross-validation score
print("Best hyperparameters:", grid_search.best_params_)
print("Best cross-validation score:", -grid_search.best_score_)

# Create a final SVR object with the best hyperparameters
best_svm_rbf = SVR(kernel='rbf', C=grid_search.best_params_['C'], gamma=grid_search.best_params_['gamma'])

# Fit the model on the training data
best_svm_rbf.fit(X_train, y_train)

# Evaluate the model on the training data
y_train_pred = best_svm_rbf.predict(X_train)
train_mse = mean_squared_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)
print("MSE on train data:", train_mse)
print("R2 on train data:", train_r2)

# Evaluate the model on the test data
y_test_pred = best_svm_rbf.predict(X_test)
test_mse = mean_squared_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)
print("MSE on test data:", test_mse)
print("R2 on test data:", test_r2)

