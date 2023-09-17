import streamlit as st


# Page title
st.title("Plan my financial roadmap")

url = 'http://127.0.0.1:8080'
# st.write(f'<a href="{url}" target="_blank">Click here to visit the website</a>', unsafe_allow_html=True)
# Create a form to take user input
with st.form("Enter details"):
    submit_button = st.form_submit_button(label="Start Financial Roadmapping", use_container_width=True)


# Check if the form is submitted
if submit_button:
    st.write(f'<a href="{url}" target="_blank">Click here to visit the finance planning platform</a>', unsafe_allow_html=True)