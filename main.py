import openai 
import streamlit as st

# pip install streamlit-chat  
from streamlit_chat import message

openai.api_key = st.secrets["openai_key"]

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message 

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def show_chat_history():
    if len(st.session_state['chat_history'])>0:
        for i in range(len(st.session_state['chat_history'])//2):
            message(st.session_state['chat_history'][i*2], is_user=True, key=str(i*2) + '_user')
            message(st.session_state['chat_history'][i*2+1], key=str(i*2+1))

# st.session_state['chat_history'].append('message1')
# st.session_state['chat_history'].append('message2')


show_chat_history()

with st.form("user_input"):
    # user_input = st.text_input(label='What is your question?')

    user_input = st.text_input(
        "Enter some text 👇",
        placeholder='enter text here'
    )

    user_input_submitted = st.form_submit_button("Submit")

if user_input_submitted:
    st.session_state['chat_history'].append(user_input)
    st.session_state['chat_history'].append(user_input * 2)


# st.subheader('History')
# st.write(st.session_state['chat_history'])

# #Creating the chatbot interface
# st.title("chatBot : Streamlit + openAI")

# # Storing the chat
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []

# if 'past' not in st.session_state:
#     st.session_state['past'] = []

# # Display the chat history in reverse order
# if st.session_state['generated']:
    
#     for i in range(len(st.session_state['generated'])-1):
#         message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
#         message(st.session_state["generated"][i], key=str(i))

# # We will get the user's input by calling the get_text function
# def get_text():
#     input_text = st.text_input("You: ","Hello, how are you?", key="input")
#     return input_text

# # Place the text input below the chat history display
# user_input = get_text()

# if user_input:
#     output = generate_response(user_input)
#     # store the output 
#     st.session_state.past.append(user_input)
#     st.session_state.generated.append(output)
