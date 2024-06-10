# streamlit_app.py
import streamlit as st
from llm import UniversalLLM

# 创建 UniversalLLM 实例
llm = UniversalLLM()

# 设置 Streamlit 页面布局
st.title("LLM Chat Interface")
st.sidebar.title("Model Configuration")

# 用于存储模型配置的列表
if 'config_list' not in st.session_state:
    st.session_state.config_list = []

model_names = ["hunyuan_lite", "spark_lite_llm", "wenxin_lite"]

# 模型配置
model_name = st.sidebar.selectbox("Choose models", model_names)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=1024, value=256)
priority = st.sidebar.number_input("Priority", min_value=0, max_value=10, value=0)
stream = st.sidebar.checkbox("Stream", value=True)

# 添加模型配置到列表
if st.sidebar.button("Add Model Configuration"):
    # for model_name in selected_models:
    config = {
        "model_name": model_name,
        "top_p": top_p,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
        "priority": priority
    }
    # 仅在配置不为空时添加
    if config:
        st.session_state.config_list.append(config)

# 显示当前的模型配置列表
st.sidebar.subheader("Current Model Configurations")
for idx, config in enumerate(st.session_state.config_list):
    try:
        st.sidebar.text(f"Model {idx + 1}: {config['model_name']}")
        st.sidebar.text(f"  Top P: {config['top_p']}")
        st.sidebar.text(f"  Temperature: {config['temperature']}")
        st.sidebar.text(f"  Max Tokens: {config['max_tokens']}")
        st.sidebar.text(f"  Priority: {config['priority']}")
        st.sidebar.text(f"  Stream: {config['stream']}")
    except KeyError as e:
        st.sidebar.error(f"Configuration {idx + 1} is missing key: {e}")

# 配置 UniversalLLM 实例
config_list = st.session_state.config_list
print(config_list)
llm.set_parameters(config_list=st.session_state.config_list)

# 输入提示词
prompt = st.text_input("Enter your prompt here:")

if st.button("Generate Response"):
    if prompt:
        response = llm.generate_text(prompt)
        for line in response:
            st.write(line['content'])
    else:
        st.error("Please enter a prompt.")
