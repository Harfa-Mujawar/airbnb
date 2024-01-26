pip install pymongo
import pandas as pd
import numpy as np
import pymongo
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud
     

client = pymongo.MongoClient("mongodb+srv://preranaraj:guvi1234@cluster0.1960q02.mongodb.net/?retryWrites=true&w=majority")
db = client.sample_airbnb
col = db.listingsAndReviews
     

rel_data = []
for i in col.find():
    data = dict(Id = i['_id'],
                Listing_url = i['listing_url'],
                Name = i.get('name'),
                Description = i['description'],
                House_rules = i.get('house_rules'),
                Property_type = i['property_type'],
                Room_type = i['room_type'],
                Bed_type = i['bed_type'],
                Min_nights = int(i['minimum_nights']),
                Max_nights = int(i['maximum_nights']),
                Cancellation_policy = i['cancellation_policy'],
                Accomodates = i['accommodates'],
                Total_bedrooms = i.get('bedrooms'),
                Total_beds = i.get('beds'),
                Availability_365 = i['availability']['availability_365'],
                Price = i['price'],
                Security_deposit = i.get('security_deposit'),
                Cleaning_fee = i.get('cleaning_fee'),
                Extra_people = i['extra_people'],
                Guests_included= i['guests_included'],
                No_of_reviews = i['number_of_reviews'],
                Review_scores = i['review_scores'].get('review_scores_rating'),
                Amenities = ', '.join(i['amenities']),
                Host_id = i['host']['host_id'],
                Host_name = i['host']['host_name'],
                Street = i['address']['street'],
                Country = i['address']['country'],
                 Country_code = i['address']['country_code'],
                Location_type = i['address']['location']['type'],
                Longitude = i['address']['location']['coordinates'][0],
                Latitude = i['address']['location']['coordinates'][1],
                Is_location_exact = i['address']['location']['is_location_exact']
    )
    rel_data.append(data)
     

import csv
     

df = pd.DataFrame(rel_data)
df
df.info()
df.isna().sum()
df.isna().sum()
df.drop(labels=list(df[df.Name.duplicated(keep=False)].index),inplace=True)
     

df.reset_index(drop=True,inplace=True)
     

# Converting dataframe to csv file and saving it
df.to_csv('Airbnb_data.csv',index=False)
     

from google.colab import files
files.download('/content/Airbnb_data.csv')
plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,y=df.Property_type.values,order=df.Property_type.value_counts().index[:10])
ax.set_title("Top 10 Property Types available")
plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,x=df.Room_type)
ax.set_title("Total Listings in each Room Type")
df.Host_name.value_counts()
plt.figure(figsize=(10,8))
ax = sns.countplot(data=df,y=df.Host_name,order=df.Host_name.value_counts().index[:10])
ax.set_title("Top 10 Hosts with Highest number of Listings")
fig = px.choropleth(data_frame=df,
                    locations='Country_code',
                    color='Country',
                    locationmode='country names')
fig.show()
     

country_df = df.groupby('Country',as_index=False)['Price'].mean()
     

fig = px.scatter(data_frame=country_df,
           x='Country',y='Price',
           color='Country',
           size='Price',
           opacity=1,
           size_max=35,
           title='Avg Listing Price in each Countries')
fig.show()
     

rev_df = df.groupby('Room_type',as_index=False)['Review_scores'].mean().sort_values(by='Review_scores')
fig = px.bar(data_frame=rev_df,x='Room_type',y='Review_scores',color='Review_scores')
fig.show()
     

rev_df = df.groupby('Room_type',as_index=False)['Review_scores'].mean().sort_values(by='Review_scores')
fig = px.bar(data_frame=rev_df,x='Room_type',y='Review_scores',color='Review_scores')
fig.show()
     

pr_df = df.groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
fig = px.bar(data_frame=pr_df,x='Room_type',y='Price',color='Price')
fig.show()
     


     