import streamlit as st
import pickle
import pandas as pd
import base64
import plotly.graph_objects as go


import plotly.express as px
# Load the dataset
file_path = "matches.csv"  # Ensure correct file path
matches_df = pd.read_csv(file_path)
cities = matches_df['city'].dropna().unique().tolist()

# Set page config
st.set_page_config(page_title="IPL Win Predictor", layout="wide")

# Custom CSS for background color
st.markdown(
    """
    <style>
        .stApp {
            background-color: #1D3D8D;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style="
        text-align: center; 
        color: #1D3D8D; 
        background-color: #5091CD;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    ">
        🏏 IPL Win Predictor 🏆
    </h1>
    """,
    unsafe_allow_html=True
)


teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'Ahmedabad', 'Nagpur', 'Visakhapatnam', 'Pune']

# Load trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Input Selection
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

selected_city = st.selectbox('Select Host City', sorted(cities))

target = st.number_input('Target Runs', min_value=1)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Balls Completed', min_value=0, max_value=120, step=1, format="%d")  # Changed to integer
with col5:
    wickets_out = st.number_input('Wickets Fallen', min_value=0, max_value=10)
    
    
    
    

# Prediction Button
if st.button(' Predict Winning Probability'):
    if score > target:
        st.error("Error: Current score cannot be greater than the target!")
    else:
        runs_left = target - score
        balls_left = 120 - overs  # Overs is now an integer
        wickets = 10 - wickets_out
        crr = score / (overs/6) if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                                 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets],
                                 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        # Define colors for teams
        team_colors = {
            'Chennai Super Kings': '#FFD700',  # Yellow
            'Mumbai Indians': '#004BA0',  # Blue
            'Royal Challengers Bangalore': '#EC1C24',  # Red
            'Kolkata Knight Riders': '#3A225D',  # Purple
            'Sunrisers Hyderabad': '#FF6F00',  # Orange
            'Delhi Capitals': '#2561ae',  # Dark Blue
            'Kings XI Punjab': '#DD1F2D',  # Dark Red
            'Rajasthan Royals': '#E60693'  # Pink
        }

        batting_color = team_colors.get(batting_team, '#FFFFFF')
        bowling_color = team_colors.get(bowling_team, '#FFFFFF')

        # Custom Progress Bars
        st.markdown(
            f"""
            <style>
                .progress-bar-container {{
                    width: 100%;
                    background-color: #ddd;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    height: 30px;
                    position: relative;
                    overflow: hidden;
                }}
                .progress-bar {{
                    height: 100%;
                    border-radius: 10px;
                    font-weight: bold;
                    line-height: 30px;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: width 0.5s ease-in-out;
                }}
                .win-bar {{
                    width: {win * 100}%;
                    background-color: {batting_color};
                    min-width: 10%;
                }}
                .loss-bar {{
                    width: {loss * 100}%;
                    background-color: {bowling_color};
                    min-width: 10%;
                }}
                .text-overlay {{
                    position: absolute;
                    width: 100%;
                    text-align: center;
                    font-weight: bold;
                    z-index: 10;
                    line-height: 30px;
                    color:  'white'
                }}
            </style>

            <div class="progress-bar-container">
                <div class="text-overlay">{batting_team} Winning Probability: {round(win * 100)}%</div>
                <div class="progress-bar win-bar"></div>
            </div>

            <div class="progress-bar-container">
                <div class="text-overlay">{bowling_team} Winning Probability: {round(loss * 100)}%</div>
                <div class="progress-bar loss-bar"></div>
            </div>
            """,
            unsafe_allow_html=True
        )



        
        # Pie Chart for Probability
        st.subheader('Winning Probability Distribution')
        fig = go.Figure(data=[go.Pie(
            labels=[batting_team, bowling_team],
            values=[win * 100, loss * 100],
            textinfo='percent+label',
            marker=dict(colors=[batting_color, bowling_color])
        )])

        fig.update_layout(
            height=400,
            width=350,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(255, 255, 255, 0.5)',  # Light transparent white background
            plot_bgcolor='rgba(255, 255, 255, 0.0)',  # Fully transparent plot background
            legend_font=dict(color="black")  # Ensures legend text is black
        )



        # Display Results in same row
        col6, col7 = st.columns([2, 1])

        with col6:
            st.plotly_chart(fig)
        
        with col7:
            st.markdown(
                f"""
                <div style="display:flex; flex-direction:column; align-items:center; gap:10px;">
                    <div style="border:2px solid #ffffff; padding:64px; border-radius:15px; background-color:#5091CD; 
                                color:#1D3D8D; text-align:center; font-size:20px; width:100%; min-height:80px;">
                        <b>Current Run Rate</b><br> {round(crr, 2)}
                    </div>
                    <div style="border:2px solid #ffffff; padding:64px; border-radius:15px; background-color:#5091CD; 
                                color:#1D3D8D; text-align:center; font-size:20px; width:100%; min-height:80px;">
                        <b>Required Run Rate</b><br> {round(rrr, 2)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        
        
        def head_to_head_win_percentage(df, team1, team2):
            matches = df[((df["team1"] == team1) & (df["team2"] == team2)) |
                        ((df["team1"] == team2) & (df["team2"] == team1))]
            total_matches = matches.shape[0]
            if total_matches == 0:
                return None
            team1_wins = matches[matches["winner"] == team1].shape[0]
            team2_wins = matches[matches["winner"] == team2].shape[0]
            return round((team1_wins / total_matches) * 100, 2), round((team2_wins / total_matches) * 100, 2)

        def city_win_percentage(df, team, city):
            matches_in_city = df[df["city"] == city]
            total_matches = matches_in_city[matches_in_city["team1"].eq(team) | matches_in_city["team2"].eq(team)].shape[0]
            if total_matches == 0:
                return None
            team_wins = matches_in_city[matches_in_city["winner"] == team].shape[0]
            return round((team_wins / total_matches) * 100, 2)

        # Calculate Insights
        head_to_head_result = head_to_head_win_percentage(matches_df, batting_team, bowling_team)
        city_win_result = city_win_percentage(matches_df, batting_team, selected_city)
        

        # Display Results in same row
        col1, col2 = st.columns([2, 1])

        with col1:
        
            if head_to_head_result:
                st.subheader("Head-to-Head Win Percentage")
                fig = go.Figure(data=[go.Pie(
                    labels=[batting_team, bowling_team],
                    values=head_to_head_result,
                    textinfo='percent+label',
                    marker=dict(colors=[team_colors.get(batting_team, '#FFFFFF'), team_colors.get(bowling_team, '#FFFFFF')])
                )])
                fig.update_layout(
                height=400,
                width=350,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor='rgba(255, 255, 255, 0.5)',  # Light transparent white background
                plot_bgcolor='rgba(255, 255, 255, 0.0)',  # Fully transparent plot background
                legend_font=dict(color="black")  # Ensures legend text is black
            )
                st.plotly_chart(fig)
            else:
                st.warning("No past matches between these teams.")
                
        with col2:
            # Ensure text contrast for better visibility
            st.subheader("Batting Team's Win Percentage in this City")

            if city_win_result is not None:
                st.markdown(f"""
                    <div style="border:4px solid #ffffff; padding:150px; border-radius:20px; background-color:#5091CD; 
                                color:#1D3D8D; text-align:center; font-size:20px; width:100%; min-height:80px;">
                        {batting_team} has won <b>{city_win_result}%</b> of matches played in {selected_city}.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"No past matches for {batting_team} in {selected_city}.")

