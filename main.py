import openai
import toml
import streamlit as st
from horoscope import get_horoscope_content
import datetime

def get_zodiac_sign(dob):
    month = dob.month
    day = dob.day

    if month == 1:
        return 'Capricorn' if day <= 19 else 'Aquarius'
    elif month == 2:
        return 'Aquarius' if day <= 18 else 'Pisces'
    elif month == 3:
        return 'Pisces' if day <= 20 else 'Aries'
    elif month == 4:
        return 'Aries' if day <= 19 else 'Taurus'
    elif month == 5:
        return 'Taurus' if day <= 20 else 'Gemini'
    elif month == 6:
        return 'Gemini' if day <= 20 else 'Cancer'
    elif month == 7:
        return 'Cancer' if day <= 22 else 'Leo'
    elif month == 8:
        return 'Leo' if day <= 22 else 'Virgo'
    elif month == 9:
        return 'Virgo' if day <= 22 else 'Libra'
    elif month == 10:
        return 'Libra' if day <= 22 else 'Scorpio'
    elif month == 11:
        return 'Scorpio' if day <= 21 else 'Sagittarius'
    elif month == 12:
        return 'Sagittarius' if day <= 21 else 'Capricorn'


def show_messages(text):
    # messages_str = [f"{a['role']}: {a['content']}" for a in st.session_state["messages"][1:]]
    if len(st.session_state["messages"])>3:
        messages_str = [f"🧑: {a['content']} \n" if a['role']=="user" else f"🔮: {a['content']} \n" for a in st.session_state["messages"][3:]]
    else:
        messages_str = ''
    text.text_area("Messages", value=str("\n".join(messages_str)), height=200)

openai.api_key = st.secrets["openai_key"]

st.header("STEP 1: Name & DOB")

if "horoscope" not in st.session_state:
    st.session_state["horoscope"] = ''

if "messages" not in st.session_state:
    st.session_state["messages"] = ''


with st.form("name_dob", clear_on_submit=True):
        user_name = st.text_input("What is your name?")
        user_dob = st.date_input('What is your dob?',min_value = datetime.date(1950, 1, 1))
        user_loc = st.text_input('Where were you born?')
        name_dob_submit = st.form_submit_button(label="Submit")

if name_dob_submit:
    zodiac_sign = get_zodiac_sign(user_dob)
    st.session_state["horoscope"] = get_horoscope_content(day='today', week = 'current', month = 'current', sign=zodiac_sign)
    st.write(f'✅ Hi {user_name}, got your horoscope - you can proceed to chat.')
    # st.write(st.session_state["horoscope"])
    BASE_PROMPT = [{"role": "system", "content": f"My name is {user_name} and I was born on {str(user_dob)} in {user_loc}. You are an astrology chatbot named Jane, created by a group of engineers from Los Angeles. Answer questions regarding my horoscope."}]
    BASE_PROMPT += [{"role": "user", "content": f"My horoscope: {st.session_state['horoscope']}"}]
    BASE_PROMPT += [{"role": "system", "content": f"Answer my questions strictly based only on my horoscope in the voice of my astrologer, named Jane and refer to me by my name."}]
    st.session_state["messages"] = BASE_PROMPT

# BASE_PROMPT = [{"role": "system", "content": "You are my astrologer. Answer my questions about my horoscope"}]

st.header("STEP 2: CHATBOT")

text = st.empty()
show_messages(text)

with st.form("myform", clear_on_submit=True):
        prompt = st.text_input("Prompt")
        submit = st.form_submit_button(label="Submit")


if submit:
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": f'Answer the question: "{prompt}" without apologies, reservations or desclaimers'}]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        
        st.session_state["messages"].pop()
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        st.session_state["messages"] += [{"role": "assistant", "content": message_response}]

        # response_clean = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo", 
        #     messages=[{'role':'user', 'content': f'Write the following without apologies, reservations or desclaimers: {message_response}'}]
        # )
        # message_response_clean = response_clean["choices"][0]["message"]["content"]
        
        # st.session_state["messages"] += [{"role": "assistant", "content": message_response}]
        show_messages(text)

# if st.button("Reset Conversation"):
#     st.session_state["messages"] = ''
#     show_messages(text)


# if name_dob_submit:
#     st.subheader('History')
#     st.write(st.session_state["messages"])






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

