import pandas as pd
import numpy as np
import Missing_data_scraper as mds
data = pd.read_csv("jobs.csv")

print("Number of rows are:",data.shape[0],"\tNumber of columns are:",data.shape[1])
#print(data.isna().sum(),"\n")


#Remove Competitors, Headquarters, Unnamed: 0
data.drop(['Competitors','Headquarters','Unnamed: 0'],axis=1,inplace=True)


#Duplicate Data
print("Total duplicate data are :",data.duplicated().sum())
data.drop_duplicates(inplace=True)


#Remove NAN for Salary Estimate
'''MIssing VALUES :
        Size                   35
        Founded               196
        Type of ownership      35
        Industry              124
        Sector                124
        Revenue                35
        Salary Estimate       159
        Rating                105'''

data = data[data["Salary Estimate"].isna()==False]
#print(data.isna().sum(),"\n Shape of Data is:",data.shape)


#Removing Rating from Company NAme
data['Company Name'] = data.apply(lambda x: x['Company Name'] if x['Rating']== np.nan else x['Company Name'][:-3],axis=1)

'''Predict Rating of the company'''
company_name = data[data['Rating'].isna()==True]['Company Name']
mds.mising_data(data,company_name,'Rating')
print("Now Missing Ratings are reduced to :",data['Rating'].isna().sum())


#Founded Using a Scraper
company_name = data[data['Founded'].isna()==True]['Company Name']
mds.mising_data(data,company_name,'Founded')
#mds.use_chat_gpt(data,company_name,'Founded')
print("Now Missing Ratings are reduced to :",data['Founded'].isna().sum())
        


#Sector Using a Scraper
company_name = data[data['Sector'].isna()==True]['Company Name']
mds.mising_data(data,company_name,'Sector')
#mds.use_chat_gpt(data,company_name,'Sector')
print("Now Missing Ratings are reduced to :",data['Sector'].isna().sum())

#Industry Using Scraper
company_name = data[data['Industry'].isna()==True]['Company Name']
mds.mising_data(data,company_name,'Industry')
print("Now Missing Ratings are reduced to :",data['Industry'].isna().sum())



data.to_csv("processed_job_data.csv",index=False)

