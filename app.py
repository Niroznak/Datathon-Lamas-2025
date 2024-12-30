import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.map import Icon

# Sample DataFrame
data = {
    'City': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Los Angeles'],
    'Latitude': [40.7128, 34.0522, 41.8781, 40.7128, 34.0522],
    'Longitude': [-74.0060, -118.2437, -87.6298, -74.0060, -118.2437],
    'Category': ['A', 'B', 'A', 'C', 'C'],
    'Value': [10, 20, 30, 40, 50],  # Example column to determine marker color and size
    'Shape': ['circle', 'square', 'triangle', 'circle', 'square'],  # Example shapes
    'Info': ['Info about NY', 'Info about LA', 'Info about Chicago', 'More info about NY', 'More info about LA']  # Example info text
}
df = pd.DataFrame(data)

# Function to determine marker color based on value
def get_marker_color(value):
    if value < 15:
        return 'green'
    elif value < 25:
        return 'orange'
    else:
        return 'red'

# Function to determine marker icon based on shape
def get_marker_icon(shape):
    if shape == 'circle':
        return 'circle'
    elif shape == 'square':
        return 'square'
    elif shape == 'triangle':
        return 'triangle'
    else:
        return 'info-sign'  # Default icon

# from folium.features import CustomIcon
# def get_custom_icon(shape):
#     if shape == 'cross':
#         return CustomIcon('path/to/cross_icon.png', icon_size=(30, 30))
#     elif shape == 'star':
#         return CustomIcon('path/to/star_icon.png', icon_size=(30, 30))
#     else:
#         return CustomIcon('path/to/default_icon.png', icon_size=(30, 30))

# Streamlit app
st.title('Interactive Map with Selections')

# Dropdown for selecting city
selected_city = st.selectbox('Select City', df['City'].unique())

# Filter categories based on selected city
filtered_categories = df[df['City'] == selected_city]['Category'].unique()

# Dropdown for selecting category based on selected city
selected_category = st.selectbox('Select Category', filtered_categories)

# Filter DataFrame based on selections
filtered_df = df[(df['City'] == selected_city) & (df['Category'] == selected_category)]

# Create Folium map
m = folium.Map(location=[filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean()], zoom_start=5)

# Add markers to the map with colors and shapes based on 'Value' and 'Shape' columns
for _, row in filtered_df.iterrows():
    marker_color = get_marker_color(row['Value'])
    marker_icon = get_marker_icon(row['Shape'])
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['City'],
        icon=Icon(color=marker_color, icon=marker_icon, prefix='fa')
    ).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

# Sidebar to display information about the selected row
st.sidebar.title('Selected Row Information')
if not filtered_df.empty:
    selected_row = filtered_df.iloc[0]  # Assuming the first row is selected for simplicity
    st.sidebar.write(f"**City:** {selected_row['City']}")
    st.sidebar.write(f"**Category:** {selected_row['Category']}")
    st.sidebar.write(f"**Value:** {selected_row['Value']}")
    st.sidebar.write(f"**Info:** {selected_row['Info']}")
else:
    st.sidebar.write("No data available for the selected options.")
