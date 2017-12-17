import numpy as np
import matplotlib.pyplot as plt
import seaborn; seaborn.set()
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import collections
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

location = r"data\Data_train.csv"
ts = pd.read_csv(location, sep=",", parse_dates=[0], header=0)
y = np.array( ts["Deal_Size"].values)
result = []
# Lọc từ cao đến thấp
listExample = sorted(y, reverse=True) 
print(listExample)
