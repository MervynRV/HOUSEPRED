import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder

dataset = pd.read_csv("C:\Programs\py\DAA\HousePricePrediction.xlsx")

#printing the first 5 records of the dataset

print(dataset.head(5))
dataset.shape


obj = (dataset.dtypes == 'object')
object_cols = list(obj[obj].index)
print("Categorical variables:",len(object_cols))

int_ = (dataset.dtypes =='int')
num_cols = list(int_[int_].index)
print("Integer variables:", len(num_cols))

fl = (dataset.dtypes == 'float')
fl_cols = list(fl[fl].index)
print("Float Variables :",len(fl_cols))

#exploratory Data analysis
numeric_cols = dataset.select_dtypes(include=['number'])  # Select all numeric columns

# Calculate the correlation matrix for numeric columns
correlation_matrix = numeric_cols.corr()

# Create a heatmap of the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt='.2f', linewidths=0.5)

# Display the heatmap
plt.show()

#the bar plot areaaa...


dataset = pd.read_excel("C:\Programs\py\DAA\HousePricePrediction.xlsx")

# Identify categorical columns
object_cols = dataset.select_dtypes(include=['object']).columns.tolist()

# Calculate the number of unique values for each categorical column
unique_values = [dataset[col].nunique() for col in object_cols]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.title('Number of Unique Values in Categorical Features')
plt.xticks(rotation=90)
sns.barplot(x=object_cols, y=unique_values)

# Show the plot
plt.show()

#the subplot area
# ypoo

dataset = pd.read_excel("C:\Programs\py\DAA\HousePricePrediction.xlsx")


object_cols = dataset.select_dtypes(include=['object']).columns.tolist()


plt.figure(figsize=(18, 36))
plt.suptitle('Categorical Features: Distribution', fontsize=16)
plt.subplots_adjust(hspace=0.5)

index = 1

for col in object_cols:
    y = dataset[col].value_counts()
    ax = plt.subplot(2, 2, index)
    plt.xticks(rotation=90)
    sns.barplot(x=list(y.index), y=y)
    ax.set_title(col)
    index += 1


plt.tight_layout(rect=[0, 0, 1, 0.97])

plt.show()

#data cleaning
# id column will not be participating
#soo dropped for data cleaning
dataset.drop(['Id'],
             axis=1,
             inplace=True)

dataset['SalePrice'] = dataset['SalePrice'].fillna(
    dataset['SalePrice'].mean())

new_dataset = dataset.dropna()

new_dataset.isnull().sum()




s = (new_dataset.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables")
print(object_cols)
print("No. of  categorical features", len(object_cols))


OH_encoder = OneHotEncoder(sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(new_dataset[object_cols]))
OH_cols.index = new_dataset.index
OH_cols.columns = OH_encoder.get_feature_names_out()
df_final = new_dataset.drop(object_cols, axis=1)
df_final = pd.concat([df_final, OH_cols], axis=1)

#splitting the data into training and Testing

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

X = df_final.drop(['SalePrice'], axis=1)
Y = df_final['SalePrice']

X_train, X_valid, Y_train, Y_valid = train_test_split(
    X, Y, train_size=0.8, test_size=0.2, random_state=0
)

from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_percentage_error

model_SVR = svm.SVR()
model_SVR.fit(X_train, Y_train)
Y_pred = model_SVR.predict(X_valid)

print(mean_absolute_percentage_error(Y_valid, Y_pred))


#random forest

from sklearn.ensemble import RandomForestRegressor

model_RFR = RandomForestRegressor(n_estimators=10)
model_RFR.fit(X_train, Y_train)
Y_pred = model_RFR.predict(X_valid)

mean_absolute_percentage_error(Y_valid, Y_pred)

print(mean_absolute_percentage_error(Y_valid, Y_pred))


from sklearn.linear_model import LinearRegression

model_LR = LinearRegression()
model_LR.fit(X_train, Y_train)
Y_pred =model_LR.predict(X_valid)

print(mean_absolute_percentage_error(Y_valid, Y_pred))

from sklearn.metrics import r2_score
from catboost import CatBoostRegressor
cb_model = CatBoostRegressor()
cb_model.fit(X_train, Y_train)
preds = cb_model.predict(X_valid)

cb_r2_score=r2_score(Y_valid, preds)
cb_r2_score
print("R2 Score for Catooster regressor :",cb_r2_score)
