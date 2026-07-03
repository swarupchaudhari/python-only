import pandas as pd

df = pd.read_csv("books_data.csv")

print(df.head())
print(df.shape)
print(df.columns)


print(df.info())


print(df.dtypes)



df['Price'] = df['Price'].replace('£','', regex=True).astype(float)



print(df.describe())



print(df.isnull().sum())

df.dropna(inplace=True)



print(df.sort_values(by='Price', ascending=False).head(10))


print(df.sort_values(by='Price').head(10))



import matplotlib.pyplot as plt

plt.hist(df['Price'], bins=10)
plt.title("Book Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()



count_books.plot(kind="bar")
plt.title("Books by Category")
plt.show()


avg_price.plot(kind="bar")
plt.title("Average Price by Category")
plt.show()


ratings.plot(kind="bar")
plt.title("Average Rating by Category")
plt.show()


df["Price"].hist(bins=20)
plt.title("Price Distribution")
plt.show()


import matplotlib.pyplot as plt

corr = df[["Price", "Rating", "Stock"]].corr()

plt.imshow(corr)

plt.xticks(range(len(corr.columns)), corr.columns)

plt.yticks(range(len(corr.columns)), corr.columns)

plt.colorbar()

plt.show()





Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)

IQR = Q3 - Q1

outliers = df[
    (df['Price'] < Q1 - 1.5*IQR) |
    (df['Price'] > Q3 + 1.5*IQR)
]

print(outliers)




count = df[
    (df['Price'] >= 20) &
    (df['Price'] <= 40)
]

print(len(count))



print(df.duplicated().sum())

df.drop_duplicates(inplace=True)



print(df.dtypes)

print(df.isnull().sum())


