# import necessary modules
from scratchai.trees import DecisionTreeRegressor, DecisionTreeClassifier
from scratchai.metrics import mean_squared_error, accuracy
from tests.data import load_regression, load_classification

# Genaret the data
X, y = load_classification(500)

model = DecisionTreeClassifier()
model.fit(X, y)

y_pred = model.predict(X)
print(accuracy(y, y_pred))