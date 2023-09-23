import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

st.markdown("""
<style>
.eyeqlp51.st-emotion-cache-fblp2m.ex0cdmw0
{
            visibility: hidden;
}
.st-emotion-cache-h5rgaw.ea3mdgi1
{
            visibility: hidden;
}
</style>
""", unsafe_allow_html= True)

data = pd.read_csv('Olympics_data.csv')

st.image('image.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overall Analysis','Medals per Gender','Team Participation','Medal Counts')
)
if user_menu=='Overall Analysis':
    st.subheader("Overall Analysis")

    editions = data['Year'].unique().shape[0] - 1
    cities = data['City'].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    events = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['NOC'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.subheader(editions)
    with col2:
        st.header("Hosts")
        st.subheader(cities)
    with col3:
        st.header("Sports")
        st.subheader(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.subheader(events)
    with col2:
        st.header("Nations")
        st.subheader(nations)
    with col3:
        st.header("Athletes")
        st.subheader(athletes)

if user_menu=='Medals per Gender':

    st.subheader("Count of Medals per Gender")

    # Filter data to exclude 'No_Medal' type
    filtered_data = data[data['Medal'] != 'No_Medal']

    # Calculate the total number of males and females
    total_counts = filtered_data['Sex'].value_counts().reset_index()
    total_counts.columns = ['Gender', 'Total Count']

    # Group data by 'Sex' and 'Medal' and count the occurrences
    da2 = filtered_data.groupby(['Sex', 'Medal'])['Medal'].count().reset_index(name='count')

    # Create a stacked bar chart to visualize the count of medals per gender
    fig = go.Figure()

    for medal_type in da2['Medal'].unique():
        medal_data = da2[da2['Medal'] == medal_type]
        fig.add_trace(go.Bar(
            x=medal_data['Sex'],
            y=medal_data['count'],
            name=medal_type,
            text=medal_data['count'],
            textposition='auto',
        ))

    # Add the total number of males and females as annotations to the chart
    for i, row in total_counts.iterrows():
        fig.add_annotation(
            x=row['Gender'],
            y=row['Total Count'],
            text=str(row['Total Count']),
            showarrow=True,
            arrowhead=1,
        )

    fig.update_layout(
        barmode='stack',
        xaxis_title='Gender',
        yaxis_title='Medal Count',
        legend_title='Medal Type',
    )

    # Update layout to remove grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig)

if user_menu=='Team Participation':

    # Create a list of unique teams
    teams = data['Team'].unique().tolist()

    # Streamlit app title and sidebar
    st.subheader("Team Participation in Sports")
    selected_team = st.selectbox("Select a Team", teams)

    # Filter data for the selected team
    filtered_data = data[data['Team'] == selected_team]

    # Count the number of sports for the selected team and sort in descending order
    sport_counts = filtered_data['Sport'].value_counts().reset_index()
    sport_counts.columns = ['Sport', 'Count']
    sport_counts = sport_counts.sort_values(by='Count', ascending=False)  # Sort in descending order

    # Create a bar chart to show sports participation for the selected team
    fig = px.bar(
        sport_counts,  # Use the sorted DataFrame
        x='Sport',
        y='Count',
        title=f'Sports Participation for {selected_team}',
        labels={'Sport': 'Sport', 'Count': 'Number of Participations'},
    )

    fig.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig)

if user_menu=='Medal Counts':

    st.subheader("Medal Counts By Athlete")

    # Create a list of unique athlete names
    athlete_names = data['Name'].unique()

    # Allow the user to select an athlete
    selected_athlete = st.selectbox("Select an Athlete", athlete_names)

    # Filter the data for the selected athlete
    filtered_data = data[data['Name'] == selected_athlete]

    # Count medals for the selected athlete
    medal_counts = filtered_data['Medal'].value_counts().reset_index()
    medal_counts.columns = ['Medal', 'Count']

    # Get the team for the selected athlete
    selected_team = filtered_data['Team'].iloc[0]

    # Create a pie chart to show the distribution of medals won by the selected athlete
    fig = px.pie(
        medal_counts,
        names='Medal',
        values='Count',
        title=f'Medal Distribution for {selected_athlete} ({selected_team})',
        labels={'Medal': 'Medal Type', 'Count': 'Medal Count'},
    )

    # Show the chart in the Streamlit app
    st.plotly_chart(fig)

    st.subheader('Medal Counts by Team')

    # Filter the data to exclude "No_medal" type
    filtered_data = data[data['Medal'] != 'No_medal']

    # Create a Streamlit slider to select the year
    selected_year = st.slider("Select a Year", min_value=data['Year'].min(), max_value=data['Year'].max(), value=data['Year'].min())

    # Filter the data based on the selected year
    filtered_data = filtered_data[filtered_data['Year'] == selected_year]

    # Group the data by 'Team' and count medals for each team
    team_medal_counts = filtered_data.groupby('Team')['Medal'].count().reset_index()

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(
        team_medal_counts,
        locations='Team',  # 'Team' column contains the team names
        locationmode='country names',  # Use country names for location data
        color='Medal',  # Color based on the medal count
        color_continuous_scale='Viridis',  # Choose a color scale
        title=f'Medal Counts by Team in {selected_year}',
    )

    # Show the map in the Streamlit app
    st.plotly_chart(fig)
