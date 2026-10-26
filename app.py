"""Mobile-first family GPT chat, built with Streamlit.

Start with: python -m streamlit run app.py
Set secrets in .streamlit/secrets.toml (local) or Streamlit Cloud Secrets.
"""
import hmac

import streamlit as st
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError

st.set_page_config(
    page_title="家庭 AI 助手",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Responsive design: works in iPhone Safari without a separate iOS app.
st.markdown(
    """
    <style>
    :root { color-scheme: light dark; }
    .block-container { max-width: 760px; padding-top: 1rem; padding-bottom: 7rem; }
    h1 { letter-spacing: -.025em; }
    [data-testid="stChatMessage"] { border-radius: 17px; padding: 1rem; }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
        overflow-wrap: anywhere; line-height: 1.55;
    }
    [data-testid="stChatMessage"] pre { overflow-x: auto; max-width: 100%; }
    [data-testid="stChatInput"] textarea { font-size: 16px !important; }
    button { min-height: 42px; }
    @media (max-width: 640px) {
        .block-container {
            max-width: 100%;
            padding-left: .8rem;
            padding-right: .8rem;
            padding-top: .4rem;
            padding-bottom: calc(7rem + env(safe-area-inset-bottom));
        }
        h1 { font-size: 1.6rem !important; }
        [data-testid="stChatMessage"] {
            padding: .7rem .75rem;
            border-radius: 15px;
            margin-bottom: .35rem;
        }
        [data-testid="stChatMessage"] p { font-size: 0.99rem; }
        [data-testid="stChatInput"] { padding-bottom: env(safe-area-inset-bottom); }
        [data-testid="stChatInput"] textarea { font-size: 16px !important; }
        /* Ensure very long code and links can scroll instead of widening the phone. */
        .stMarkdown, .stMarkdown > div { min-width: 0; overflow-wrap: anywhere; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    family_password = st.secrets.get("FAMILY_PASSWORD", "")
    model = st.secrets.get("OPENAI_MODEL", "gpt-6-luna")
except Exception:
    st.error("尚未设置应用密钥。请根据 README.md 配置 Secrets。")
    st.stop()

if not api_key or not family_password:
    st.error("缺少 OPENAI_API_KEY 或 FAMILY_PASSWORD。请联系管理员设置。")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if not st.session_state.authenticated:
    st.title("🏡 家庭 AI 助手")
    st.write("欢迎回家！输入家庭密码即可开始聊天。")
    with st.form("login", clear_on_submit=True):
        password = st.text_input("家庭密码", type="password", placeholder="请输入家庭密码")
        submit = st.form_submit_button("进入家庭聊天", use_container_width=True)
    if submit:
        if st.session_state.login_attempts >= 5:
            st.error("本次会话尝试次数过多，请关闭后重新打开，或联系管理员。")
        elif hmac.compare_digest(password.encode("utf-8"), family_password.encode("utf-8")):
            st.session_state.authenticated = True
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.session_state.login_attempts += 1
            st.error("家庭密码不正确，请重试。")
    st.caption("📱 支持 iPhone Safari。建议使用 Safari 的「分享 → 添加到主屏幕」。")
    st.caption("仅供受邀家人使用。不要公开网页链接和家庭密码。")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

with st.sidebar:
    st.subheader("🏡 家庭设置")
    st.caption(f"当前模型：{model}")
    st.caption(f"本次会话调用：{st.session_state.request_count}/40")
    if st.button("🧹 新对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🔒 退出登录", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.session_state.request_count = 0
        st.rerun()
    st.info("聊天历史只在当前网页会话保存，不跨设备同步。")
    st.caption("提醒：这里的 40 次限制只针对当前浏览器会话，无法代替后台预算控制。")

st.title("🏡 家庭 AI 助手")
st.caption("📱 iPhone 友好 · 家庭专属 · 轻松聊天")

if not st.session_state.messages:
    st.info("你好！可以问我：今天做什么菜？帮孩子讲解一道数学题？或翻译一段英文？")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# At the page root st.chat_input is pinned at the bottom, including on phones.
prompt = st.chat_input("发送消息给家庭 AI…", max_chars=2000)
if prompt:
    if st.session_state.request_count >= 40:
        st.warning("本次会话已达到 40 次请求上限。可稍后再试。")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)

    inputs = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages[-12:]
    ]
    inputs.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            with st.spinner("正在回答…"):
                client = OpenAI(api_key=api_key, timeout=60.0)
                response = client.responses.create(
                    model=model,
                    instructions=(
                        "你是适合家庭日常使用的友善 AI 助手，"
                        "优先使用中文，回答清晰、准确、简洁。"
                    ),
                    input=inputs,
                    max_output_tokens=1200,
                    store=False,
                )
            answer = response.output_text or "这次未生成文本，请重试。"
            st.markdown(answer)
        st.session_state.messages.extend(
            [{"role": "user", "content": prompt}, {"role": "assistant", "content": answer}]
        )
        st.session_state.request_count += 1
    except AuthenticationError:
        st.error("API Key 无效，请联系管理员检查配置。")
    except RateLimitError:
        st.error("API 余额不足或触发速率限制，请联系管理员。")
    except APIConnectionError:
        st.error("暂时无法连接 AI 服务，请检查网络再试。")
    except APIError:
        st.error("AI 服务暂不可用，请稍后重试。")
    except Exception:
        st.error("发生未知错误，请管理员查看部署日志。")
