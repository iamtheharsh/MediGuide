# app.py
import os
import streamlit as st
import requests

# --- Configuration ---
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# --- State Management & Callbacks ---
def init_session_state():
    defaults = {"token": None, "username": None, "messages": [], "conversations": [], "current_conversation_id": None}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def new_chat_callback():
    st.session_state.messages = []
    st.session_state.current_conversation_id = None

def select_conversation_callback(conversation_id):
    try:
        res = requests.get(f"{API_URL}/conversations/{conversation_id}", headers=get_auth_headers())
        res.raise_for_status()
        st.session_state.messages = res.json().get("messages", [])
        st.session_state.current_conversation_id = conversation_id
    except requests.RequestException:
        st.error("Could not load chat history.")

# --- API Functions ---
def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}

# --- UI Views ---
def show_auth_view():
    st.sidebar.title("Welcome")
    auth_choice = st.sidebar.radio("Get Started", ["Login", "Register"])
    with st.form("auth_form"):
        st.subheader(f"{auth_choice} to MediGuide")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button(auth_choice):
            if auth_choice == "Login":
                try:
                    res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
                    res.raise_for_status()
                    st.session_state.token = res.json()['access_token']
                    st.session_state.username = username
                    st.rerun()
                except requests.RequestException as e:
                    st.error(f"Login failed: {e.response.json().get('detail', 'Connection Error')}")
            else:  # Registration
                try:
                    res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
                    res.raise_for_status()
                    st.success("Registration successful! Please login.")
                except requests.RequestException as e:
                    st.error(f"Registration failed: {e.response.json().get('detail', 'Connection Error')}")

def show_chat_view():
    st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.title("Chat History")
    st.sidebar.button("➕ New Chat", use_container_width=True, on_click=new_chat_callback)

    try:
        res = requests.get(f"{API_URL}/conversations", headers=get_auth_headers())
        res.raise_for_status()
        st.session_state.conversations = res.json()
    except requests.RequestException:
        st.session_state.conversations = []

    for convo in st.session_state.conversations:
        convo_id = convo.get("id") or convo.get("_id")  # fallback
        st.sidebar.button(convo['title'], key=convo_id,
                          use_container_width=True,
                          on_click=select_conversation_callback, args=(convo_id,))

    st.markdown("### Conversation")
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    if prompt := st.chat_input("Ask anything medical..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            payload = {"prompt": prompt, "conversation_id": st.session_state.current_conversation_id}
            try:
                res = requests.post(f"{API_URL}/chat", json=payload, headers=get_auth_headers())
                res.raise_for_status()
                data = res.json()
                st.session_state.messages.append({"role": "assistant", "content": data['response']})
                if st.session_state.current_conversation_id is None:
                    st.session_state.current_conversation_id = data['conversation_id']
            except requests.RequestException as e:
                st.error(f"Error: {e}")
        st.rerun()

# --- Main App Controller ---
def main():
    init_session_state()
    st.markdown("<h1 style='text_align: center;'>🩺 MediGuide</h1>", unsafe_allow_html=True)
    if not st.session_state.token:
        show_auth_view()
    else:
        show_chat_view()

if __name__ == "__main__":
    main()
