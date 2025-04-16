# IPL-Win-Probability-Predictor

An interactive machine learning-powered web application that predicts the winning probability of IPL  matches. Built using **Streamlit**, **scikit-learn**, and **Plotly**, this project uses historical match data to make real-time win predictions and provide match insights.


---

##  Features

- Predicts real-time win probability based on:
  - Batting team
  - Bowling team
  - Target runs
  - Current score
  - Balls completed
  - Wickets fallen
  - Match city
- Dynamic progress bars for win/loss visualization
- Pie charts showing:
  - Head-to-head stats
  - Batting team performance in selected city
- Beautiful UI styled with HTML & CSS inside Streamlit

---

##  Models Used

- **Random Forest Classifier** (for deployment)
- Also experimented with **XGBoost** for performance comparison
- Evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-Score

---

##  Tech Stack

- **Frontend/UI**: Streamlit, HTML, CSS
- **ML Model**: scikit-learn (Random Forest), XGBoost
- **Visualization**: Plotly
- **Data Handling**: Pandas, NumPy




