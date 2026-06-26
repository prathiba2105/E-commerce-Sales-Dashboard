import requests
import pandas as pd

url = "https://dummyjson.com/products"

response = requests.get(url)
data=response.json()
df=pd.DataFrame(data['products'])
print(df.head())
print(df.info())
print(df.isnull().sum())
df=df[["id","title","description","price","discountPercentage","rating","stock","brand","category"]]
print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
df.fillna(0,inplace=True)

#create new column
df["discount_amount"]=(df["price"]*df["discountPercentage"]/100)
df["final_price"]=(df["price"]-df["discount_amount"])
df.to_csv("clean_products.csv",index=False)

#connect python to mysql database
from sqlalchemy import create_engine
engine = create_engine('mysql://root:Prathiba@localhost/ecommerce')

#load data to mysql database
df.to_sql('products',engine, if_exists='replace', index=False)
print("Data loaded to MySQL database successfully!")
