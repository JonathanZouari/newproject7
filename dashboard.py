import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Titanic Dataset Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🚢 Titanic Dataset Dashboard")
st.markdown("**Explore survival patterns and passenger demographics from the Titanic disaster**")

# Load Titanic dataset
@st.cache_data
def load_data():
    # Using seaborn's built-in Titanic dataset
    try:
        import seaborn as sns
        df = sns.load_dataset('titanic')
        return df
    except:
        # Fallback: create sample data if seaborn is not available
        st.warning("Seaborn not installed. Using sample data. Install with: pip install seaborn")
        return pd.DataFrame({
            'survived': [1, 0, 1, 0, 1] * 20,
            'pclass': [1, 2, 3, 1, 2] * 20,
            'sex': ['male', 'female'] * 50,
            'age': [22, 38, 26, 35, 35] * 20,
            'fare': [7.25, 71.28, 7.92, 53.1, 8.05] * 20,
            'embarked': ['S', 'C', 'S', 'S', 'C'] * 20,
            'class': ['First', 'Second', 'Third', 'First', 'Second'] * 20,
            'who': ['man', 'woman', 'woman', 'man', 'woman'] * 20,
            'adult_male': [True, False, False, True, False] * 20,
            'alone': [True, False, False, True, False] * 20
        })

df = load_data()

# Sidebar filters
st.sidebar.header("🎛️ Filters")

# Class filter
class_options = ['All'] + sorted(df['pclass'].dropna().unique().tolist())
selected_class = st.sidebar.selectbox("Passenger Class", class_options)

# Gender filter
gender_options = ['All'] + sorted(df['sex'].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Embarkation port filter
embark_options = ['All'] + sorted(df['embarked'].dropna().unique().tolist())
selected_embark = st.sidebar.selectbox("Embarkation Port", embark_options)

# Age range filter
age_min = float(df['age'].min()) if not df['age'].isna().all() else 0.0
age_max = float(df['age'].max()) if not df['age'].isna().all() else 100.0
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# Apply filters
filtered_df = df.copy()

if selected_class != 'All':
    filtered_df = filtered_df[filtered_df['pclass'] == selected_class]

if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['sex'] == selected_gender]

if selected_embark != 'All':
    filtered_df = filtered_df[filtered_df['embarked'] == selected_embark]

filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])]

# Key Metrics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

total_passengers = len(filtered_df)
survived = filtered_df['survived'].sum()
survival_rate = (survived / total_passengers * 100) if total_passengers > 0 else 0
avg_age = filtered_df['age'].mean()
avg_fare = filtered_df['fare'].mean()

with col1:
    st.metric("Total Passengers", f"{total_passengers:,}")

with col2:
    st.metric("Survived", f"{int(survived):,}", f"{survival_rate:.1f}%")

with col3:
    st.metric("Average Age", f"{avg_age:.1f}" if not pd.isna(avg_age) else "N/A")

with col4:
    st.metric("Average Fare", f"£{avg_fare:.2f}" if not pd.isna(avg_fare) else "N/A")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Survival by Class
    st.subheader("📊 Survival Rate by Class")
    survival_by_class = filtered_df.groupby('pclass')['survived'].agg(['sum', 'count'])
    survival_by_class['rate'] = (survival_by_class['sum'] / survival_by_class['count'] * 100)
    
    fig1 = px.bar(
        survival_by_class.reset_index(),
        x='pclass',
        y='rate',
        labels={'pclass': 'Passenger Class', 'rate': 'Survival Rate (%)'},
        color='rate',
        color_continuous_scale='RdYlGn',
        text='rate'
    )
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Survival by Gender
    st.subheader("👥 Survival Rate by Gender")
    survival_by_gender = filtered_df.groupby('sex')['survived'].agg(['sum', 'count'])
    survival_by_gender['rate'] = (survival_by_gender['sum'] / survival_by_gender['count'] * 100)
    
    fig2 = px.bar(
        survival_by_gender.reset_index(),
        x='sex',
        y='rate',
        labels={'sex': 'Gender', 'rate': 'Survival Rate (%)'},
        color='rate',
        color_continuous_scale='RdYlGn',
        text='rate'
    )
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Age distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Age Distribution")
    fig3 = px.histogram(
        filtered_df,
        x='age',
        color='survived',
        labels={'age': 'Age', 'survived': 'Survived'},
        nbins=30,
        barmode='overlay',
        color_discrete_map={0: '#FF4B4B', 1: '#00CC96'}
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("💰 Fare Distribution by Class")
    fig4 = px.box(
        filtered_df,
        x='pclass',
        y='fare',
        color='survived',
        labels={'pclass': 'Passenger Class', 'fare': 'Fare (£)', 'survived': 'Survived'},
        color_discrete_map={0: '#FF4B4B', 1: '#00CC96'}
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# Embarkation analysis
st.subheader("🌍 Passengers by Embarkation Port")
embark_data = filtered_df.groupby(['embarked', 'survived']).size().reset_index(name='count')
embark_labels = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
embark_data['port'] = embark_data['embarked'].map(embark_labels)

fig5 = px.bar(
    embark_data,
    x='port',
    y='count',
    color='survived',
    labels={'port': 'Embarkation Port', 'count': 'Number of Passengers', 'survived': 'Survived'},
    barmode='group',
    color_discrete_map={0: '#FF4B4B', 1: '#00CC96'}
)
fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Filtered Data")
st.dataframe(
    filtered_df[['survived', 'pclass', 'sex', 'age', 'fare', 'embarked']].head(100),
    use_container_width=True
)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Data Source: Titanic Dataset | Built with Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)