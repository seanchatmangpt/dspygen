# import streamlit as st
# import paho.mqtt.client as mqtt
# from threading import Thread
#
# from paho.mqtt.enums import CallbackAPIVersion
#
#
# # Function to handle incoming MQTT messages
# def on_message(client, userdata, message):
#     # Decode message
#     decoded_message = message.payload.decode("utf-8")
#     # Use Streamlit's session state to store the latest message
#     st.session_state.latest_message = decoded_message
#
# # Function to start MQTT client
# def start_mqtt_client():
#     # Create and configure the client
#     client = mqtt.Client(CallbackAPIVersion.VERSION2)
#     client.on_message = on_message
#     client.connect("localhost", 1883)
#     client.subscribe("actor_system/publish")
#     # Start the loop
#     client.loop_start()
#     return client
#
# # Initialize session state for storing messages
# if 'latest_message' not in st.session_state:
#     st.session_state.latest_message = "No messages yet."
#
# # Create a button to connect and start listening to MQTT messages
# if st.button("Subscribe") or 'mqtt_client' not in st.session_state:
#     # Start MQTT client in a separate thread to prevent blocking
#     st.session_state.mqtt_client = Thread(target=start_mqtt_client)
#     st.session_state.mqtt_client.start()
#     st.write("Subscribed to MQTT topic.")
#
# # Display the latest message
# st.write("Latest message:", st.session_state.latest_message)
