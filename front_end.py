import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS for HCSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        color: #003366;
    }
    .stSlider, .stMultiSelect {
        padding-bottom: 10px;
    }
    h1, h2, h3, h4 {
        color: #003366;
    }
    .st-emotion-cache-1avcm0n.ezrtsby2 {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.image("data/HCSS_Beeldmerk_Blauw_RGB1200 ppi.png", use_container_width=True)

# Load data
df = pd.read_csv("data/prepared_tables.csv")

# Define a blue palette which corresponds to the HCSS styling
blue_palette = ["#003366", "#336699", "#6699CC", "#99CCFF", "#66B3FF"]

st.title("HCSS text analysis: discussions of AIin Defense in Dutch Parliament")

st.write("""
This project examines discussions held by Dutch politicians in both the Lower and Upper Houses on key topics highlighted
at the REAIM summit, including artificial intelligence, machine learning, and other advanced military technologies.
By analyzing a large dataset of speeches and associated metadata, the study explores not only the overall sentiment but
also the underlying trends in support and opposition. The analysis further investigates how factors such as gender,
political orientation, and age correlate with attitudes toward these emerging technologies, offering a deeper insight
into the topic. Only the data from 2022 was taken for this analysis, since the topic of military technologies got 
significantly more discussed after the Russian invasion in Ukraine in 2022, and hardly brought up earlier.
""")

# Filters for the page by party and Upper/Lower houses
with st.sidebar:
    st.header("Filters")
    # Party filter
    selected_parties = st.multiselect(
        "Select the Party",
        options=df["Speaker_party"].unique(),
        default=df["Speaker_party"].unique()
    )
    # Body filter with "Both" option
    body_options = ["Both"] + list(df["Body"].unique())
    body_choice = st.radio("Select the House", options=body_options, index=0)

filtered_df = df[df["Speaker_party"].isin(selected_parties)]
if body_choice != "Both":
    filtered_df = filtered_df[filtered_df["Body"] == body_choice]

st.header("Sentiment Analysis")
st.write("""
         In this research the sentiment analysis was performed, which is shown as AI positivity index. It varies from 
         -1 to 1, where -1 is completely negative, and 1 is completely positive.
         """)

# Create scatterplot with an OLS trendline
age_ai_positivity_fig = px.scatter(
    filtered_df,
    x="Age",
    y="compound",
    trendline="ols",
    title="Age vs AI Positivity Scatterplot",
    labels={"Age": "Age", "compound": "AI Positivity"},
    color_discrete_sequence=["#003366"]
)
age_ai_positivity_fig.update_traces(marker=dict(color="#003366"))
st.plotly_chart(age_ai_positivity_fig)
if len(filtered_df) > 1:
    corr_value = filtered_df["Age"].corr(filtered_df["compound"])
    st.write(f"Correlation between Age and Compound: {corr_value:.2f}")
else:
    st.write("Not enough data points to compute correlation.")

# The box plot with Gender's and their positions regarding the AI in military domain
gender_ai_positivity_fig = px.box(
    filtered_df,
    x="is_female",
    y="compound",
    title="Gender vs AI Positivity",
    labels={"is_female": "is_female", "compound": "AI Positivity"},
    color="is_female",
    color_discrete_sequence=["#003366", "#6699FF"]
)
st.plotly_chart(gender_ai_positivity_fig)
if len(filtered_df) > 1:
    corr_value = filtered_df["is_female"].corr(filtered_df["compound"])
    st.write(
        f"Correlation between being a female and AI positivity: {corr_value:.2f}")
else:
    st.write("Not enough data points to compute correlation.")

st.header("Monthly trends")
st.write("""It's also essential to understand, how many times the topics of AI and military technologies werebrought up
         throughout the months and how the average sentiment changed""")
min_month = int(filtered_df['Month'].min())
max_month = int(filtered_df['Month'].max())
selected_month_range = st.slider(
    "Select Month Range",
    min_value=min_month,
    max_value=max_month,
    value=(min_month, max_month)
)

# Filter the dataframe based on the selected month range
filtered_df = filtered_df[(filtered_df['Month'] >= selected_month_range[0]) &
                          (filtered_df['Month'] <= selected_month_range[1])]

month_names = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


aggregated_frequency = filtered_df.groupby(
    'Month').size().reset_index(name='Frequency')
# Map numeric month to month names
aggregated_frequency['MonthName'] = aggregated_frequency['Month'].map(
    month_names)
# Create a line chart with markers using the month names on the x-axis
freq_fig = px.line(
    aggregated_frequency,
    x='MonthName',
    y='Frequency',
    markers=True,
    title="Monthly Frequency of topic mentioning by politicians",
    labels={"MonthName": "Month", "Frequency": "Frequency"},
    category_orders={"MonthName": list(month_names.values())}
)
freq_fig.update_traces(fill='tozeroy', fillcolor='rgba(51,102,153,0.2)',
                       line=dict(color="#003366"), marker=dict(color="#003366"))
# Add a vertical dashed line at February when the war started
freq_fig.add_vline(
    x=1,
    line_dash="dash",
    line_color="red",
    annotation_text="Beginning Of the War in Ukraine",
    annotation_position="top right"
)
st.plotly_chart(freq_fig)

# Average AI positivity by month
aggregated_positivity = filtered_df.groupby(
    'Month')['compound'].mean().reset_index(name='Avg_Compound')
aggregated_positivity['MonthName'] = aggregated_positivity['Month'].map(
    month_names)
# Create a line chart with markers for average compound values using month names on the x-axis
compound_fig = px.line(
    aggregated_positivity,
    x='MonthName',
    y='Avg_Compound',
    markers=True,
    title="Monthly Average AI positivity",
    labels={"MonthName": "Month", "Avg_Compound": "Average AI Positivity"},
    category_orders={"MonthName": list(month_names.values())}
)
compound_fig.update_traces(fill='tozeroy', fillcolor='rgba(51,102,153,0.2)',
                           line=dict(color="#003366"), marker=dict(color="#003366"))
# Add a vertical dashed line in February whne the war started
compound_fig.add_vline(
    x=1,
    line_dash="dash",
    line_color="red",
    annotation_text="Beginning Of the War in Ukraine",
    annotation_position="top right"
)
st.plotly_chart(compound_fig)


st.header("Descriptive Analytics")
st.write("""
In this section of our research, we conduct a descriptive analysis to identify which types of politicians are most
engaged with the selected topic. Understanding these trends is important because it provides insight into the
distribution of opinions and helps us evaluate which political groups are more vocal on these issues.
""")

# Create bar chart showing frequency of Speaker_party values
party_counts = filtered_df['Speaker_party'].value_counts().reset_index()
party_counts.columns = ['Speaker_party', 'Frequency']
bar_fig = px.bar(
    party_counts,
    x='Speaker_party',
    y='Frequency',
    color='Speaker_party',
    title="Frequency of the topic mentioning by Speaker Parties",
    labels={"Frequency": "Frequency", "Speaker_party": "Political Party"},
    color_discrete_sequence=blue_palette
)
bar_fig.update_layout(showlegend=False)
st.plotly_chart(bar_fig)

# Gender bar chart

# Map boolean values to gender labels
filtered_df['Gender'] = filtered_df['is_female'].apply(
    lambda x: 'Female' if x else 'Male')

# Count the occurrences of each gender
gender_counts = filtered_df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

# Create bar chart using Plotly Express with a blue-only color scheme
gender_bar_fig = px.bar(
    gender_counts,
    x='Gender',
    y='Count',
    color='Gender',
    title='Frequency of topic mentioning by Gender',
    labels={"Count": "Frequency", "Gender": "Gender"},
    color_discrete_map={'Female': "#6699FF", 'Male': "#336699"}
)
st.plotly_chart(gender_bar_fig)

# If the speaker is the minister or not
minister_not_minister_count = filtered_df['Speaker_minister'].value_counts(
).reset_index()
minister_not_minister_count.columns = ['Speaker_minister', 'Count']
pie_minister_fig = px.pie(
    minister_not_minister_count,
    values='Count',
    names='Speaker_minister',
    title="Frequencies by Minister status"
)

# Party status and minster status analysis
party_status_counts = filtered_df['Party_status'].value_counts().reset_index()
party_status_counts.columns = ['Party_status', 'Count']
pie_status_fig = px.pie(
    party_status_counts,
    values='Count',
    names='Party_status',
    title="Frequency by Party Status"
)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(pie_status_fig)
with col2:
    st.plotly_chart(pie_minister_fig)


# Prepare Party_orientation pie chart
party_orientation_counts = filtered_df['Party_orientation'].value_counts(
).reset_index()
party_orientation_counts.columns = ['Party_orientation', 'Count']
pie_orientation_fig = px.pie(
    party_orientation_counts,
    values='Count',
    names='Party_orientation',
    title="Frequencies of the topic discussion by Party Orientation",
    color_discrete_sequence=blue_palette
)
st.plotly_chart(pie_orientation_fig)

# Prepare kamers pie chart and the frequencies of topic mentioning
kamer_counts = filtered_df['Body'].value_counts().reset_index()
kamer_counts.columns = ['Body', 'Count']
pie_kamer_fig = px.pie(
    kamer_counts,
    values='Count',
    names='Body',
    title="Frequencies of the topic discussions by different Kamers"
)
st.plotly_chart(pie_kamer_fig)
speaker_counts = filtered_df['Speaker_name'].value_counts().reset_index()
speaker_counts.columns = ['Speaker_name', 'Count']
top10_speakers = speaker_counts.head(10)

# Create a horizontal bar chart with the most frequent speakers about the advanced technologies in military and defense
# domains.
top10_fig = px.bar(
    top10_speakers,
    x='Count',
    y='Speaker_name',
    orientation='h',
    title="Top 10 Speakers about the Topic",
    color='Count',
    labels={"Count": "Frequency", "Speaker_name": "Name of the politician"},
    color_continuous_scale='Blues'
)
# Order the y-axis so that the highest counts are at the top
top10_fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(top10_fig)
