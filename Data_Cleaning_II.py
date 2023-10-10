import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

data = pd.read_csv('processed_job_data.csv')
print(data.head())

#SALARY
data['hourly'] = data['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
data['employer provided salary'] = data['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)
salary = data['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kde = salary.apply(lambda x: x.replace('K','').replace('Employer Provided Salary:','').replace('$','').replace('Per Hour',''))

correct_format = minus_kde.apply(lambda x: x.replace(x,x+' - '+x) if '-' not in x else x)
data['min_salary'] = correct_format.apply(lambda x:float(x.split(' - ')[0]))
data['max_salary'] = correct_format.apply(lambda x: float(x.split(' - ')[1]))
data['avg_salary'] = (data.min_salary+data.max_salary)/2

#job_state
data['job_state'] = data['Location'].apply(lambda x: x.split(',')[-1])
print(data['job_state'])


#Type of Ownership
print(data['Type of ownership'].isna().sum())
data['Type of ownership'] = data['Type of ownership'].apply(lambda x: np.nan if x=='Unknown' else x)
print(data['Type of ownership'].isna().sum())
data['Type of ownership'] = data['Type of ownership'].apply(lambda x: x.replace('Company - ','') if type(x)!=float else x)

#Founded Take only Year
data.Founded.fillna('-1',inplace=True)
data['Founded'] = data['Founded'].apply(lambda x: int(x) if len(x)==4  else float(x[-4:]))
data['Founded'] = data.Founded.astype(int)


temp = data.dropna()
print(temp.shape,data.shape)



#Revenue
"""data['Revenue']=data['Revenue'].apply(lambda x: np.nan if x=='Unknown / Non-Applicable' else x)
print("Revenue NAN Data is: ",data['Revenue'].isna().sum())

'''MAKING A ML MODEL TO CALCULATE REMAINING REVENUE'''


train_rev = data[data['Revenue'].isna()==False]
print("Train Size: ",train_rev.shape)

transforming_elements=['Revenue','Company Name','Location','job_state','Size','Industry','Type of ownership','Sector']
for i in transforming_elements:
    train_rev[i] = LabelEncoder().fit_transform(train_rev[i])
#print(train_rev['Revenue Label'].unique())

removing_elements = ['Revenue','Unnamed: 0','Salary Estimate','Job Title','Job Description']
features = list(train_rev.columns)
for i in removing_elements:
    features.remove(i)

x = train_rev[features]
y = train_rev['Revenue']

x_train,x_test,y_train,y_test = train_test_split(x,y,train_size=0.75,random_state=0)

'''DECISION TREE MODEL '''
rev_model = DecisionTreeClassifier().fit(x_train,y_train)
y_predict = rev_model.predict(x_test)
print("ACCURACY of Decision Tree Model: ",metrics.accuracy_score(y_test,y_predict))

'''RandomForest Model'''
rev_rfmodel = RandomForestClassifier().fit(x_train,y_train)
y_predict = rev_rfmodel.predict(x_test)
print("Accuracy of RFMODEL: ",metrics.accuracy_score(y_test,y_predict))"""