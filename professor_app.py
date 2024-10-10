import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# Define the rating criteria
rating_criteria = [
    "Clarity",
    "Engagement",
    "Course Structure",
    "Responsiveness",
    "Overall Effectiveness",
]

# Collect feedback and ratings
def collect_feedback():
    feedback_data = []
    for criterion in rating_criteria:
        st.header(f"Rate {criterion}")
        rating = st.slider(f"Rating for {criterion}:", 1, 5)
        feedback = st.text_area(f"Feedback for {criterion}:")
        sentiment = TextBlob(feedback).sentiment.polarity
        feedback_data.append({"Criterion": criterion, "Rating": rating, "Feedback": feedback, "Sentiment": sentiment})
    return pd.DataFrame(feedback_data)

# Display quantitative evaluation
def display_quantitative_evaluation(feedback_data):
    st.header("Quantitative Evaluation")
    average_ratings = feedback_data["Rating"].mean()
    st.metric("Average Rating", average_ratings)

    # Visualize ratings
    st.subheader("Rating Distribution")
    plt.figure(figsize=(10, 5))
    plt.bar(rating_criteria, feedback_data["Rating"])
    plt.xlabel("Rating Criteria")
    plt.ylabel("Rating")
    plt.title("Rating Distribution")
    st.pyplot()

# Provide suggestions for improvement and automated feedback responses
def provide_suggestions(feedback_data):
    st.header("Suggestions for Improvement")
    low_rated_criteria = feedback_data[feedback_data["Rating"] < 3]["Criterion"].tolist()
    if low_rated_criteria:
        st.warning("Consider addressing the following criteria:")
        for criterion in low_rated_criteria:
            st.markdown(f"- **{criterion}**: {feedback_data[feedback_data['Criterion'] == criterion]['Feedback'].iloc[0]}")

    # Sentiment analysis and automated feedback responses
    positive_feedback = feedback_data[feedback_data["Sentiment"] > 0]["Feedback"].tolist()
    negative_feedback = feedback_data[feedback_data["Sentiment"] < 0]["Feedback"].tolist()
    neutral_feedback = feedback_data[feedback_data["Sentiment"] == 0]["Feedback"].tolist()

    st.subheader("Sentiment Analysis")
    st.markdown("**Positive Feedback:**")
    for feedback in positive_feedback:
        st.markdown(f"- {feedback}")

    st.markdown("**Negative Feedback:**")
    for feedback in negative_feedback:
        st.markdown(f"- {feedback}")

    st.markdown("**Neutral Feedback:**")
    for feedback in neutral_feedback:
        st.markdown(f"- {feedback}")


st.title("Professor Rating System")

feedback_data = collect_feedback()
display_quantitative_evaluation(feedback_data)
provide_suggestions(feedback_data)