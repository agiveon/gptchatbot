import openai
import toml
import streamlit as st


def show_messages(text):
    # messages_str = [f"{a['role']}: {a['content']}" for a in st.session_state["messages"][1:]]
    messages_str = [f"USER: {a['content']} \n" if a['role']=="user" else f"JANE: {a['content']} \n" for a in st.session_state["messages"][1:]]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=200)

openai.api_key = st.secrets["openai_key"]
BASE_PROMPT = [{"role": "system", "content": "You are my astrologer. Answer my questions about my horoscope"}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""


st.header("STREAMLIT GPT-3 CHATBOT")

text = st.empty()
show_messages(text)

with st.form("user_input"):
    prompt = st.text_input("Prompt",value="")

    user_input_submitted = st.form_submit_button("Submit")

if user_input_submitted:
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system", "content": message_response}
        ]
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)








# import openai 
# import streamlit as st

# # pip install streamlit-chat  
# from streamlit_chat import message

# openai.api_key = st.secrets["openai_key"]

# def generate_response(prompt):
#     completions = openai.Completion.create(
#         engine = "text-davinci-003",
#         prompt = prompt,
#         max_tokens = 1024,
#         n = 1,
#         stop = None,
#         temperature=0.5,
#     )
#     message = completions.choices[0].text
#     return message 

# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# def show_chat_history():
#     if len(st.session_state['chat_history'])>0:
#         for i in range(len(st.session_state['chat_history'])//2):
#             message(st.session_state['chat_history'][i*2], is_user=True, key=str(i*2) + '_user')
#             message(st.session_state['chat_history'][i*2+1], key=str(i*2+1))

# # st.session_state['chat_history'].append('message1')
# # st.session_state['chat_history'].append('message2')


# show_chat_history()

# with st.form("user_input"):
#     # user_input = st.text_input(label='What is your question?')

#     user_input = st.text_input(
#         "Enter some text 👇",
#         placeholder='enter text here'
#     )

#     user_input_submitted = st.form_submit_button("Submit")

# if user_input_submitted:
#     st.session_state['chat_history'].append(user_input)
#     st.session_state['chat_history'].append(user_input * 2)


# st.subheader('History')
# st.write(st.session_state['chat_history'])

