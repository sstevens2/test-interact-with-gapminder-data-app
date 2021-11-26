import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interact with Gapminder Data")

df = pd.read_csv("Data/gapminder_tidy.csv")

continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())
metric_labels = {"gdpPercap": "GDP Per Capita", "lifeExp": "Average Life Expectancy", "pop": "Population"}

def format_metric(metric_raw):
    return metric_labels[metric_raw]

with st.sidebar:
    st.subheader("Configure the plot")
    continent = st.selectbox(label = "Choose a continent", options = continent_list)
    metric = st.selectbox(label = "Choose a metric", options = metric_list, format_func=format_metric)
    show_data = st.checkbox("Show Data?")
    

query = f"continent=='{continent}' & metric=='{metric}'"
df_filtered = df.query(query)

countries_list = list(df_filtered['country'].unique())
countries = st.sidebar.multiselect(label = "Which countries should be plotted?", options = countries_list, default = countries_list)
df_filtered = df_filtered[df_filtered.country.isin(countries)]


year_min = int(df_filtered['year'].min())
year_max = int(df_filtered['year'].max())
years = st.sidebar.slider("Which years should be plotted", min_value = year_min, max_value = year_max, value = (year_min, year_max))
df_filtered = df_filtered[ (df_filtered['year'] >= years[0]) & (df_filtered['year'] <= years[1])]

title = f"{metric_labels[metric]} for countries in {continent}"
fig = px.line(df_filtered, x = "year", y = "value", color = "country", title = title, labels={"value": f"{metric_labels[metric]}"})
st.plotly_chart(fig, use_container_width=True)
st.markdown(f"This plot shows the {metric_labels[metric]} from {years[0]} to {years[1]} for the following countries in {continent}: {', '.join(countries)}.")

if show_data:
    st.subheader("Data for the above plot")
    st.dataframe(df_filtered)
