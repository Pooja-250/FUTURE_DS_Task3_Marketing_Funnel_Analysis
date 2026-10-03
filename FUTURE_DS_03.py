#!/usr/bin/env python
# coding: utf-8

# # Marketing Funnel & Conversion Analysis
# 
# ## Future Interns – Data Science & Analytics Task 3
# 
# This project analyzes e-commerce user behavior to understand the customer funnel, identify conversion drop-offs, compare user behavior across product categories, and generate actionable insights to improve conversions.
# 

# In[3]:


import pandas as pd

df = pd.read_csv("2019-csv.csv")
df.head()


# In[7]:


df.columns


# In[10]:


df["event_type"].value_counts()


# In[11]:


funnel_users = df.groupby("event_type")["user_id"].nunique()
funnel_users


# In[14]:


view_users = funnel_users["view"]
cart_users = funnel_users["cart"]
purchase_users = funnel_users["purchase"]

view_to_cart = (cart_users / view_users) * 100
cart_to_purchase = (purchase_users / cart_users) * 100
view_to_purchase = (purchase_users / view_users) * 100

view_to_cart, cart_to_purchase, view_to_purchase


# In[15]:


event_counts = df["event_type"].value_counts()
event_counts


# In[16]:


purchase_users = df[df["event_type"] == "purchase"]["user_id"].nunique()
purchase_users


# In[17]:


total_users = df["user_id"].nunique()

purchase_conversion = (purchase_users / total_users) * 100

total_users, purchase_conversion


# In[18]:


category_purchase = (
    df[df["event_type"] == "purchase"]
    .groupby("category_code")["user_id"]
    .nunique()
    .sort_values(ascending=False)
)

category_purchase.head(10)


# In[19]:


category_funnel = (
    df.groupby(["category_code", "event_type"])["user_id"]
    .nunique()
    .unstack(fill_value=0)
)

category_funnel["conversion_rate"] = (
    category_funnel["purchase"] / category_funnel["view"]
) * 100

category_funnel.sort_values(
    "conversion_rate", ascending=False
).head(10)


# In[20]:


category_analysis = category_funnel[category_funnel["view"] >= 1000]

category_analysis.sort_values(
    "conversion_rate", ascending=False
).head(10)


# In[21]:


view_events = event_counts["view"]
cart_events = event_counts["cart"]
purchase_events = event_counts["purchase"]

view_to_cart_rate = (cart_events / view_events) * 100
view_to_purchase_rate = (purchase_events / view_events) * 100

view_to_cart_rate, view_to_purchase_rate


# In[22]:


funnel_summary = pd.DataFrame({
    "Stage": ["View", "Cart", "Purchase"],
    "Events": [view_events, cart_events, purchase_events]
})

funnel_summary


# In[23]:


import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.bar(
    funnel_summary["Stage"],
    funnel_summary["Events"]
)

plt.title("Marketing Funnel - Event Overview")
plt.xlabel("Funnel Stage")
plt.ylabel("Number of Events")
plt.show()


# In[24]:


category_purchase = (
    df[df["event_type"] == "purchase"]
    .groupby("category_code")["user_id"]
    .nunique()
    .sort_values(ascending=False)
)

category_purchase.head(10)


# In[25]:


category_funnel = (
    df.groupby(["category_code", "event_type"])["user_id"]
    .nunique()
    .unstack(fill_value=0)
)

category_funnel["purchase_rate"] = (
    category_funnel["purchase"] / category_funnel["view"]
) * 100

category_funnel[category_funnel["view"] >= 1000] \
    .sort_values("purchase_rate", ascending=False) \
    .head(10)


# In[26]:


import matplotlib.pyplot as plt

top_categories = (
    category_funnel[category_funnel["view"] >= 1000]
    .sort_values("purchase_rate", ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_categories.index[::-1],
    top_categories["purchase_rate"][::-1]
)

plt.title("Top Product Categories by Purchase Rate")
plt.xlabel("Purchase Rate (%)")
plt.ylabel("Product Category")
plt.show()


# In[27]:


brand_purchase = (
    df[df["event_type"] == "purchase"]
    .groupby("brand")["user_id"]
    .nunique()
    .sort_values(ascending=False)
)

brand_purchase.head(10)


# In[28]:


top_brands = brand_purchase.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_brands.index[::-1],
    top_brands.values[::-1]
)

plt.title("Top Brands by Purchase Users")
plt.xlabel("Unique Purchasing Users")
plt.ylabel("Brand")
plt.show()


# In[29]:


purchase_data = df[df["event_type"] == "purchase"]

average_order_value = purchase_data["price"].mean()

average_order_value


# In[30]:


df["event_time"] = pd.to_datetime(df["event_time"])

df["month"] = df["event_time"].dt.to_period("M").astype(str)

monthly_events = (
    df.groupby(["month", "event_type"])
    .size()
    .unstack(fill_value=0)
)

monthly_events


# ## Recommendations
# 
# Based on the funnel and user behavior analysis, the following actions can help improve conversions:
# 
# 1. **Reduce the gap between views and purchases** by improving product pages, pricing visibility, product information, and calls-to-action.
# 
# 2. **Focus on high-performing product categories**, especially electronics, and identify what makes these categories more successful so similar practices can be applied elsewhere.
# 
# 3. **Monitor cart activity carefully** to identify users who show purchase intent but do not complete the purchase. Retargeting, reminders, and a simpler checkout experience can help reduce potential drop-offs.
# 
# 4. **Prioritize high-performing brands and products** when planning campaigns and promotional activities.
# 
# 5. **Track funnel KPIs regularly**, including views, cart events, purchases, purchasing users, and purchase rate, to identify changes in customer behavior.
# 
# ## Dataset Limitation
# 
# The dataset contains e-commerce event-level records for November 2019 only. It does not provide a dedicated order ID or guaranteed sequential journey for every user. Therefore, the analysis uses descriptive event and user-level metrics rather than assuming a strict View → Cart → Purchase sequence.
# 
# Since only one month of data is available, month-to-month trend and campaign-period comparisons could not be performed.

# In[ ]:




