import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title for the Streamlit app
st.set_page_config(page_title="Fast Food Analysis", layout="wide")
st.title("🍔 Fast Food Nutritional Analysis App")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("fastfood.csv")
    return df.dropna()

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
restaurants = st.sidebar.multiselect("Select Restaurants", options=df['restaurant'].unique(), default=df['restaurant'].unique())
calories_range = st.sidebar.slider("Select Calorie Range", int(df['calories'].min()), int(df['calories'].max()), (200, 1000))

# Apply filters
filtered_df = df[(df['restaurant'].isin(restaurants)) & (df['calories'].between(calories_range[0], calories_range[1]))]

# Display dataset
st.write("### Filtered Dataset")
st.dataframe(filtered_df, use_container_width=True)

# Key statistics
st.write("### Nutritional Statistics")
st.metric("Average Calories", round(filtered_df["calories"].mean(), 2))
st.metric("Average Protein (g)", round(filtered_df["protein"].mean(), 2))
st.metric("Average Total Fat (g)", round(filtered_df["total_fat"].mean(), 2))
st.metric("Average Carbohydrates (g)", round(filtered_df["total_carb"].mean(), 2))

# Visualization: Top 10 High-Calorie Foods
st.write("### Top 10 High-Calorie Foods")
top_calories = filtered_df.nlargest(10, "calories", keep="first")
fig, ax = plt.subplots()
ax.barh(top_calories["item"], top_calories["calories"], color="red")
ax.set_xlabel("Calories")
ax.set_ylabel("Item")
ax.set_title("Top 10 High-Calorie Foods")
ax.invert_yaxis()
st.pyplot(fig)

# Visualization: Calories vs. Protein
st.write("### Calories vs. Protein Content")
fig, ax = plt.subplots()
ax.scatter(filtered_df["calories"], filtered_df["protein"], alpha=0.6, color="blue")
ax.set_xlabel("Calories")
ax.set_ylabel("Protein")
ax.set_title("Calories vs. Protein Content")
st.pyplot(fig)

# Visualization: Proportion of Restaurants (Pie Chart)
st.write("### Proportion of Restaurants in Dataset")
restaurant_counts = filtered_df['restaurant'].value_counts()
fig, ax = plt.subplots()
ax.pie(restaurant_counts, labels=restaurant_counts.index, autopct='%1.1f%%', colors=['lightblue', 'lightcoral', 'lightgreen', 'gold', 'violet'])
ax.set_title("Proportion of Restaurants in Dataset")
st.pyplot(fig)

# Visualization: Number of Items Per Restaurant
st.write("### Fast Food Restaurants")
fig, ax = plt.subplots()
ax.bar(restaurant_counts.index, restaurant_counts.values, color='royalblue')
ax.set_xlabel("Restaurant")
ax.set_ylabel("Total Items")
ax.set_title("Number of Items Per Restaurant")
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization: Distribution of Calories (Histogram)
st.write("### Distribution of Calories in Fast Food Items")
fig, ax = plt.subplots()
ax.hist(filtered_df['calories'], bins=20, color="blue", edgecolor='black', alpha=0.7)
ax.set_xlabel("Calories")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Calories in Fast Food Items")
st.pyplot(fig)

# Visualization: Calories vs. Total Fat
st.write("### Calories vs. Total Fat")
fig, ax = plt.subplots()
ax.scatter(filtered_df['calories'], filtered_df['total_fat'], color="purple", alpha=0.6)
ax.set_xlabel("Calories")
ax.set_ylabel("Total Fat (g)")
ax.set_title("Calories vs. Total Fat")
st.pyplot(fig)

# Visualization: Top 10 Sugary Foods
st.write("### The Amount of Sugar in Food")
df_ca = filtered_df[['item', 'sugar']].sort_values(by='sugar', ascending=False).head(10)
fig, ax = plt.subplots()
ax.barh(df_ca['item'], df_ca['sugar'], color='crimson')
ax.set_xlabel("Sugar Content (g)")
ax.set_ylabel("Food Item")
ax.set_title("Top 10 Sugary Food Items")
ax.invert_yaxis()
st.pyplot(fig)

# Visualization: Carbohydrate Content Across Restaurants (Box Plot)
st.write("### Carbohydrate Content Across Fast Food Restaurants")
df_ca = filtered_df[['restaurant', 'total_carb']]
restaurants = df_ca['restaurant'].unique()
data = [df_ca[df_ca['restaurant'] == restaurant]['total_carb'] for restaurant in restaurants]
fig, ax = plt.subplots()
ax.boxplot(data, labels=restaurants, patch_artist=True, boxprops=dict(facecolor="lightblue"))
ax.set_xlabel("Restaurant")
ax.set_ylabel("Total Carbohydrates (g)")
ax.set_title("Carbohydrate Content Across Fast Food Restaurants")
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization: Macronutrient Distribution (Stack Plot)
st.write("### Macronutrient Distribution Across Restaurants")
restaurant_grouped = filtered_df.groupby("restaurant")[["protein", "total_fat", "total_carb"]].sum()
fig, ax = plt.subplots()
ax.stackplot(
    restaurant_grouped.index,
    restaurant_grouped["protein"],
    restaurant_grouped["total_fat"],
    restaurant_grouped["total_carb"],
    labels=["Protein", "Total Fat", "Total Carbohydrates"],
    colors=["blue", "red", "green"],
    alpha=0.6
)
ax.set_xlabel("Restaurant")
ax.set_ylabel("Total Macronutrient Content (g)")
ax.set_title("Macronutrient Distribution Across Restaurants")
ax.legend(loc="upper left")
plt.xticks(rotation=45)
st.pyplot(fig)

# Download filtered data
st.write("### Download Filtered Data")
st.download_button(label="Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_fastfood.csv", mime="text/csv")

st.sidebar.success("Adjust filters to explore data interactively! 🎯")
