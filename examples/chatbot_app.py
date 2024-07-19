import streamlit as st
from chatbot import chatbot, extract_instructions
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

st.header("Chatbot")

st.markdown("""
    <style>
    .message-box {
        max-width: 40%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #D3D3D3;
        text-align: left;
    }
    .bot-message {
        background-color: #D3D3D3;
        text-align: right;
        margin-left: auto;
    }
    </style>
    """, unsafe_allow_html=True)

openai_api_key = st.text_input("Enter OpenAI API Key:", type="password")
api_key = st.text_input("Enter API Key:", type="password")
email = st.text_input("Enter Email:")

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

def display_conversation():
    for idx, entry in enumerate(st.session_state.conversation):
        user_message = entry["user_message"]
        bot_message = entry["bot_message"]
        detector_response = entry["detector_response"]

        st.markdown(f"<div class='message-box user-message'><strong>User:</strong> {user_message['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='message-box bot-message'><strong>Chatbot:</strong> {bot_message['content']}</div>", unsafe_allow_html=True)

        with st.expander(f'Detector Responses for Query {idx + 1}'):
            st.header('Aimon Rely - Hallucination Detector Response')
            if 'hallucination' in detector_response:
                st.json(detector_response['hallucination'])
            else:
                st.write("Hallucination data is not available.")

            st.header('Aimon Rely - Model Conciseness Detector Response')
            if 'conciseness' in detector_response:
                st.json(detector_response['conciseness'])
            else:
                st.write("Conciseness data is not available.")

            st.header('Aimon Rely - Model Completeness Detector Response')
            if 'completeness' in detector_response:
                st.json(detector_response['completeness'])
            else:
                st.write("Completeness data is not available.")

            st.header('Aimon Rely - Toxicity Detector Response')
            if 'toxicity' in detector_response:
                st.json(detector_response['toxicity']['results'])
            else:
                st.write("Toxicity data is not available.")
            
            st.header('Adherence Detector Response')
            if 'instruction_adherence' in detector_response:
                st.json(detector_response['instruction_adherence'])
            else:
                st.write("Instruction adherence data is not available.")

# Display previous conversation
display_conversation()

def reset_input():
    st.session_state.new_user_query = ""
    st.session_state.new_system_prompt = ""

user_query = st.text_area("User Query", height=100, key="new_user_query")
system_prompt = st.text_area("System Prompt", height=100, key="new_system_prompt")

if st.button("Chat with Chatbot"):
    if not user_query.strip():
        st.write("Please enter a user query.")
    elif not openai_api_key.strip() or not api_key.strip() or not email.strip():
        st.write("Please enter both API keys and email.")
    elif not system_prompt.strip():
        st.write("Please enter a system prompt.")
    else:
        start_time = time.time()

        user_message = {"role": "user", "content": user_query}
        instructions = extract_instructions(system_prompt)
        st.session_state["system_prompt"] = system_prompt

        try:
            (
                chatbot_response, hallucination_score, toxicity, conciseness, 
                adherence_details, completeness, detection_response
            ) = chatbot(user_query, instructions, openai_api_key, api_key, email)
        except Exception as e:
            st.write(f"Error occurred: {e}")
            chatbot_response = "Error occurred while processing your request."

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Time taken for response: {elapsed_time:.2f} seconds")

        if chatbot_response == "Error occurred while processing your request.":
            st.write(chatbot_response)
        else:
            bot_message = {"role": "bot", "content": chatbot_response}
            st.session_state.conversation.append({
                "user_message": user_message,
                "bot_message": bot_message,
                "detector_response": detection_response
            })
            st.experimental_rerun()  # Rerun to update the display with the new conversation entry

st.button("Reset", on_click=reset_input)
