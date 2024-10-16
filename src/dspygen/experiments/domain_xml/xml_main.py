import xml.etree.ElementTree as ET
import pandas as pd
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tpot import TPOTRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Parse XML Data
xml_data = """<?xml version='1.0' ?><!-- pageok --><rss version='2.0' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:admin='http://webns.net/mvcb/' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:slash='http://purl.org/rss/1.0/modules/slash/' xmlns:wfw='http://wellformedweb.org/CommentAPI/' xmlns:content='http://purl.org/rss/1.0/modules/content/'><channel><title>Go Daddy Auctions - All Auctions Ending Today</title><link>https://auctions.godaddy.com/trpHome.aspx?isc=rssTD01</link><description>All Auctions ending today at Go Daddy Auctions</description><language>en-us</language><copyright>Copyright 2024</copyright><lastBuildDate>Sun, 29 Sep 2024 13:58:10 GMT</lastBuildDate><ttl>60</ttl><image><url>http://img1.wsimg.com/fos/img/img_logo_65x65_white.jpg</url><title>Go Daddy Auctions - auctions.godaddy.com</title><link>https://auctions.godaddy.com/trpHome.aspx?isc=rssTD01</link></image><item><title>Auctions Ending Today</title><link><![CDATA[https://auctions.godaddy.com/trpSearchResults.aspx?ra=1019062920240958&isc=rssTD01]]></link><description><![CDATA[The domains people want are going fast at auctions.godaddy.com]]></description><guid><![CDATA[https://auctions.godaddy.com/trpSearchResults.aspx?ra=1019062920240958&isc=rssTD01]]></guid></item>
<item><title>HOUSANDCOMPANY.ORG</title><link><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151272&isc=rssTD01]]></link><description><![CDATA[Auction Type: Bid, Auction End Time: 09/29/2024 09:00 AM (PDT), Price: $10, Number of Bids: 0, Domain Age: 7, Description: , Traffic: 0, Valuation: $352, IsAdult: false]]></description><guid><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151272]]></guid></item>
<item><title>OURCOMMUNITYNEEDSUGANDA.ORG</title><link><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151275&isc=rssTD01]]></link><description><![CDATA[Auction Type: Bid, Auction End Time: 09/29/2024 09:00 AM (PDT), Price: $10, Number of Bids: 0, Domain Age: 1, Description: , Traffic: 11, Valuation: $1, IsAdult: false]]></description><guid><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151275]]></guid></item>
<item><title>ACCUEILBOLA.INFO</title><link><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151947&isc=rssTD01]]></link><description><![CDATA[Auction Type: Bid, Auction End Time: 09/29/2024 09:00 AM (PDT), Price: $25, Number of Bids: 0, Domain Age: 1, Description: , Traffic: 0, Valuation: $1, IsAdult: false]]></description><guid><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587151947]]></guid></item>
<item><title>PARISH-LIFE.ORG</title><link><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587161550&isc=rssTD01]]></link><description><![CDATA[Auction Type: Bid, Auction End Time: 09/29/2024 09:00 AM (PDT), Price: $10, Number of Bids: 0, Domain Age: 1, Description: , Traffic: 0, Valuation: $210, IsAdult: false]]></description><guid><![CDATA[https://auctions.godaddy.com/trpItemListing.aspx?miid=587161550]]></guid></item>
</channel></rss>"""

root = ET.fromstring(xml_data)
items = []
for item in root.findall('./channel/item'):
    item_data = {}
    item_data['title'] = item.find('title').text
    item_data['link'] = item.find('link').text
    item_data['guid'] = item.find('guid').text
    description = item.find('description').text
    desc_pairs = re.findall(r'(\w[\w\s]*?):\s*([^,]+)', description)
    for key, value in desc_pairs:
        key = key.strip().replace(' ', '_')
        item_data[key] = value.strip()
    items.append(item_data)
df = pd.DataFrame(items)
columns_order = ['title', 'link', 'guid', 'Auction_Type', 'Auction_End_Time', 'Price',
                'Number_of_Bids', 'Domain_Age', 'Description', 'Traffic', 'Valuation', 'IsAdult']
columns_order = [col for col in columns_order if col in df.columns]
df = df[columns_order]

# 2. Data Preprocessing
df_clean = df.dropna(subset=['Valuation']).copy()
df_clean.reset_index(drop=True, inplace=True)
df_clean['Valuation'] = df_clean['Valuation'].replace({'\$': ''}, regex=True).astype(float)
df_clean['Price'] = df_clean['Price'].replace({'\$': ''}, regex=True).astype(float)
df_clean['Traffic'] = pd.to_numeric(df_clean['Traffic'], errors='coerce')
df_clean['Number_of_Bids'] = pd.to_numeric(df_clean['Number_of_Bids'], errors='coerce')
df_clean['Domain_Age'] = pd.to_numeric(df_clean['Domain_Age'], errors='coerce')
df_clean['Auction_End_Time'] = pd.to_datetime(df_clean['Auction_End_Time'], format='%m/%d/%Y %I:%M %p (%Z)', errors='coerce')
df_clean['Auction_End_Hour'] = df_clean['Auction_End_Time'].dt.hour
df_clean['Auction_End_Day'] = df_clean['Auction_End_Time'].dt.day
df_clean['Auction_End_Month'] = df_clean['Auction_End_Time'].dt.month
df_clean['Auction_End_Year'] = df_clean['Auction_End_Time'].dt.year
df_clean.drop('Auction_End_Time', axis=1, inplace=True)
df_clean['IsAdult'] = df_clean['IsAdult'].map({'true': 1, 'false': 0})
le = LabelEncoder()
df_clean['Auction_Type'] = le.fit_transform(df_clean['Auction_Type'])
numerical_cols = ['Price', 'Number_of_Bids', 'Domain_Age', 'Traffic']
for col in numerical_cols:
    df_clean[col].fillna(df_clean[col].median(), inplace=True)
df_clean.drop(['Description', 'title', 'link', 'guid'], axis=1, inplace=True)

# 3. Define Target and Features
X = df_clean.drop('Valuation', axis=1)
y = df_clean['Valuation']

# 4. Split the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Run TPOT
tpot = TPOTRegressor(
    generations=5,
    population_size=50,
    verbosity=2,
    random_state=42,
    n_jobs=-1
)
tpot.fit(X_train, y_train)
tpot.export('tpot_best_pipeline.py')

# 6. Evaluate the Model
y_pred = tpot.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score: {r2:.2f}")
