import streamlit as st
import requests

# Streamlit app title
st.title('Message Testing App')

# Backend API endpoint
api_endpoint = "http://localhost:5555"

# User input
user_input = st.text_input("Enter your message:", "")

# Button to send the message
if st.button("Send Message"):
    # Ensure there is user input before sending the request
    if user_input:
        try:
            # Encode the user input for URL and send the GET request
            response = requests.get(f"{api_endpoint}/?user_input={user_input}")

            # Check if the response is successful
            if response.status_code == 200:
                # Display the response
                st.success("Response received from the server:")
                st.json(response.json())
            else:
                st.error(f"Error: Received response code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a message before sending.")
