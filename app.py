
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "あなたは優秀なアシスタントAIです。"}]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# チャットメッセージのスクロール可能なコンテナを作成
with st.container():
    st.markdown("""
        <style>
        .chat-container {
            height: 600px;  # 高さを調整可能
            overflow-y: scroll;
        }
        </style>
        <div class="chat-container">
    """, unsafe_allow_html=True)

    if st.session_state["messages"]:
        messages = st.session_state["messages"]
        for message in messages:  # メッセージを上から下に表示
            speaker = "🙂" if message["role"] == "user" else "🤖"
            st.write(speaker + ": " + message["content"])
    
    st.markdown("</div>", unsafe_allow_html=True)

# ユーザー入力
user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
