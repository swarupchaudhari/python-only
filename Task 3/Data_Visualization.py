import matplotlib.pyplot as plt

category_count = df["Category"].value_counts()

category_count.plot(kind="bar")
plt.title("Number of Books by Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()


avg_price = df.groupby("Category")["Price"].mean()

avg_price.plot(kind="bar")
plt.title("Average Price by Category")
plt.xlabel("Category")
plt.ylabel("Average Price")
plt.xticks(rotation=45)
plt.show()



ratings = df.groupby("Category")["Rating"].mean()

ratings.plot(kind="bar")
plt.title("Average Rating by Category")
plt.xlabel("Category")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.show()




plt.hist(df["Price"], bins=20)
plt.title("Book Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()




plt.boxplot(df["Price"])
plt.title("Book Price Box Plot")
plt.ylabel("Price")
plt.show()


plt.scatter(df["Rating"], df["Stock"])
plt.title("Rating vs Stock")
plt.xlabel("Rating")
plt.ylabel("Stock")
plt.show()

category_count.plot(kind="pie", autopct="%1.1f%%")
plt.title("Book Categories Distribution")
plt.ylabel("")
plt.show()

