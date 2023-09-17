import streamlit as st


# Page title
st.title("Get financial advice")


# Create a form to take user input
with st.form("Enter details"):
    # Add a text input field for the user to enter some data
    user_input = st.text_area("Tell us what you'd like in your ideal credit card")

    # Add a button to submit the form
    submit_button = st.form_submit_button(label="Find my credit card")


# Check if the form is submitted
if submit_button:
    if user_input:
        st.info("Finding your ideal credit card...")
    else:
        st.warning("Please tell us more about your ideal credit card.")
