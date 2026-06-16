import os

import httpx
import streamlit as st

# Streamlit app title
st.title('Message Testing App')

# Backend API endpoint
api_endpoint = os.environ.get("API_BASE_URL", "http://localhost:5555")

# User input
user_input = st.text_input("Enter your message:", "")

# Button to send the message
if st.button("Send Message"):
    # Ensure there is user input before sending the request
    if user_input:
        try:
            # Encode the user input for URL and send the GET request
            response = httpx.get(f"{api_endpoint}/?user_input={user_input}", timeout=10)

            # Check if the response is successful
            if response.status_code == 200:
                # Display the response
                st.success("Response received from the server:")
                st.json(response.json())
            else:
                st.error(f"Error: Received response code {response.status_code}")
        except httpx.ConnectError as e:
            st.error(f"Connection error: could not reach {api_endpoint}. Is the server running?")
        except httpx.TimeoutException as e:
            st.error(f"Request timed out connecting to {api_endpoint}.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a message before sending.")
