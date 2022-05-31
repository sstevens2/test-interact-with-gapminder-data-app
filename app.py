import streamlit as st
import pandas as pd
import plotly.express as px

# set up the app with wide view preset and a title
st.set_page_config(layout = "wide")
st.title("Interact with Gapminder Data")

# read in the tidy gapminder data
df = pd.read_csv("Data/gapminder_tidy.csv")

# get a list of all possible continents and metrics, for the widgets
continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())

# map the actual data values to more readable strings
metric_labels = {"gdpPercap": "GDP Per Capita", "lifeExp": "Average Life Expectancy", "pop": "Population"}

# function to be used in widget argument format_func that maps metric vals to readable labes, using abv dict
def format_metric(metric_raw):
    return metric_labels[metric_raw]

# put all widgets in a sidebar with subtitle
with st.sidebar:
    st.subheader("Configure the plot")
    continent = st.selectbox(label = "Choose a continent", options = continent_list)
    metric = st.selectbox(label = "Choose a metric", options = metric_list, format_func = format_metric)

# use selected values from widgets to filter dataset down to only the rows we need
query = f"continent=='{continent}' & metric=='{metric}'"
df_filtered = df.query(query)

# select which countries should be displayed
countries_list = list(df_filtered['country'].unique())
with st.sidebar:
    countries = st.multiselect(label = "Which countries should be plotted?", options = countries_list, default = countries_list)
df_filtered = df_filtered[df_filtered.country.isin(countries)]

# select which years should be displayed
year_min = int(df_filtered['year'].min())
year_max = int(df_filtered['year'].max())

with st.sidebar:
    years = st.slider(label = "What years should be plotted?", min_value = year_min, max_value = year_max,
                     value = (year_min, year_max))
df_filtered = df_filtered[(df_filtered.year >= years[0]) & (df_filtered.year <= years[1])]


# create plot of data
title = f"{metric_labels[metric]} for countries in {continent}"
fig = px.line(df_filtered, x = "year", y = "value", color = "country", 
              title = title, labels={"value": f"{metric_labels[metric]}"})
st.plotly_chart(fig)  # display the plot

st.markdown(f"This plot shows the {metric_labels[metric]} for countries in {continent}")

with st.sidebar:
    show_data = st.checkbox(label = "Show the data used to generate this plot", value = False)

if show_data:
    st.dataframe(df_filtered)
