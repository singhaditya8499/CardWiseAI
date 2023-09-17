import streamlit as st
import openai
import pandas as pd
import os

# Page title
st.title("Find my credit card")

# OpenAI API model
GPT_MODEL = "gpt-3.5-turbo"

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load prompt
credit_card_data = pd.read_csv("../data/credit_card_data.csv")
prompt_context = "These are the details about the available credit cards: \n"

# Collate all the details about the credit cards
for index, row in credit_card_data.iterrows():
    row = row.astype(str)
    card_context = ""
    card_context += " Credit card name is: " + row["CreditCardsName"]
    card_context += " and it is offered by " + row["Company"]
    card_context += ". The company rating is " + row["CompanyRating"]
    card_context += " and the rating of card offered is " + row["CardRating"]
    card_context += ". The required credit score range is " + row["CreditScoreRange"]
    card_context += (
        ". The card recommendation percentage is " + row["RecomendationPercentage"]
    )
    card_context += ". Annual fee for the card is " + row["AnnualFee"]
    card_context += (
        ". Additional fees associated to the card are " + row["AdditionalFees"]
    )
    card_context += " and some of the benefits offered are " + row["Benefits"]
    card_context += ". The average APR for the card is " + row["AverageAPR"]
    card_context += " and the Credit card limit is " + row["CreditCardLimit"]
    card_context += "\n\n\n"

    prompt_context += card_context

# Create a form to take user input
with st.form("Enter details"):
    # Add a text input field for the user to enter some data
    user_input = st.text_area("Tell us what you'd like in your ideal credit card")

    # Add a button to submit the form
    submit_button = st.form_submit_button(label="Find my credit card")


# Check if the form is submitted
if submit_button:
    if user_input:
        # Create a query using the user input
        query = f"""Use the below article to know about different credit card and to answer the subsequent question. Always try to give the best possible option. If you cant decide or if there is any confusion , write "I don't know."

Article:
\"\"\"
{prompt_context}
\"\"\"

Question: {user_input} Which card should I go for?"""
        # Use the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions about the best credit card option.",
                },
                {"role": "user", "content": query},
            ],
            model=GPT_MODEL,
            temperature=0,
        )["choices"][0]["message"]["content"]
        # Display the response
        st.write(response)
    else:
        # Display a warning if the user input is empty
        st.warning("Please tell us more about your ideal credit card.")
