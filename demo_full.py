import streamlit as st
import os
import time
from dotenv import load_dotenv

from openai import OpenAI
from template import (
    call_openai, 
    call_openai_mini, 
    compare_models,
    chat_with_system_prompt,
    count_tokens,
    estimate_cost,
    OPENAI_MODEL
)

# Nạp biến môi trường
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cấu hình UI cơ bản
st.set_page_config(page_title="AI API Demo - Full Lab 1", page_icon="🚀", layout="wide")
st.title("🚀 AI API Demo - Full Lab 1")

# Sidebar
st.sidebar.header("Cài đặt API chung")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider("Max Tokens", min_value=10, max_value=2048, value=256, step=10)

# Khởi tạo Tabs
tab1, tab2, tab3 = st.tabs(["📊 So Sánh Model (Part 1)", "🎭 System Prompt & Chi Phí (Part 2)", "💬 Trợ Lý Ảo Chatbot (Part 3&4)"])

# ==========================================
# TAB 1: SO SÁNH MODEL
# ==========================================
with tab1:
    st.subheader("So sánh GPT-4o và GPT-4o-mini")
    user_prompt_1 = st.text_area("Nhập Prompt cần kiểm tra:", key="prompt_tab1")
    if st.button("So Sánh", type="primary", key="btn_run1"):
        if user_prompt_1.strip():
            with st.spinner("Đang chạy cả hai model..."):
                try:
                    result = compare_models(user_prompt_1)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### 🟢 GPT-4o")
                        st.metric("Latency", f"{result['gpt4o_time']:.2f}s")
                        if 'gpt4o_cost' in result:
                            st.metric("Cost", f"${result['gpt4o_cost']:.6f}")
                        st.markdown("**Trả lời:**")
                        st.write(result["gpt4o_answer"])
                    with col2:
                        st.markdown("### 🔵 GPT-4o-mini")
                        st.metric("Latency", f"{result['mini_time']:.2f}s")
                        st.markdown("**Trả lời:**")
                        st.write(result["mini_answer"])
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập prompt!")

# ==========================================
# TAB 2: SYSTEM PROMPT & TÍNH CHI PHÍ
# ==========================================
with tab2:
    st.subheader("Trò chuyện có kịch bản (System Prompt)")
    col_sys, col_user = st.columns(2)
    with col_sys:
        sys_prompt = st.text_area("System Prompt (Vai trò của AI):", value="Bạn là một giáo viên tiểu học. Hãy giải thích mọi thứ thật đơn giản.", key="sys_tab2")
    with col_user:
        user_prompt_2 = st.text_area("User Prompt (Câu hỏi của bạn):", key="user_tab2")
        
    if st.button("Hỏi AI", type="primary", key="btn_run2"):
        if user_prompt_2.strip() and sys_prompt.strip():
            with st.spinner("Đang xử lý..."):
                try:
                    answer, latency = chat_with_system_prompt(
                        sys_prompt, user_prompt_2, 
                        temperature=temperature, max_tokens=max_tokens
                    )
                    cost_info = estimate_cost(sys_prompt + " " + user_prompt_2, answer)
                    
                    st.success(f"Phản hồi sau {latency:.2f} giây")
                    st.markdown("**Kết quả:**")
                    st.info(answer)
                    
                    st.markdown("### 💰 Thống kê chi phí thực tế (bằng Token)")
                    ccol1, ccol2, ccol3 = st.columns(3)
                    ccol1.metric("Token Đầu Vào (Prompt)", cost_info["prompt_tokens"])
                    ccol2.metric("Token Đầu Ra (Completion)", cost_info["completion_tokens"])
                    ccol3.metric("Tổng Chi Phí", f"${cost_info['total_cost']:.6f}")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập đủ System Prompt và User Prompt!")

# ==========================================
# TAB 3: TRỢ LÝ ẢO CHATBOT (STREAMING)
# ==========================================
with tab3:
    st.subheader("Chatbot AI có trí nhớ (Streaming)")
    
    chat_sys_prompt = st.text_input("System Prompt cho Chatbot:", value="Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.total_cost = 0.0
        st.session_state.total_tokens = 0
        
    if st.button("Xóa Lịch Sử Chat"):
        st.session_state.messages = []
        st.session_state.total_cost = 0.0
        st.session_state.total_tokens = 0
        st.rerun()

    # Hiển thị thống kê tổng
    st.markdown(f"**Tổng Token:** {st.session_state.total_tokens} | **Tổng Chi Phí:** ${st.session_state.total_cost:.6f}")
    
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Xử lý input mới (Streaming UI)
    if prompt := st.chat_input("Nhắn gì đó..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Xây dựng mảng messages gọi API (System + History gần nhất)
            api_messages = [{"role": "system", "content": chat_sys_prompt}] + st.session_state.messages[-8:]
            
            try:
                # Gọi API dạng Stream
                stream = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=api_messages,
                    stream=True,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Cập nhật UI liên tục từng chunk
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                # Cập nhật UI cuối cùng
                message_placeholder.markdown(full_response)
                
                # Lưu vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Tính chi phí chạy ngầm
                prompt_text = chat_sys_prompt + " " + " ".join([m["content"] for m in st.session_state.messages[-9:-1]]) + " " + prompt
                c_info = estimate_cost(prompt_text, full_response)
                st.session_state.total_tokens += c_info["prompt_tokens"] + c_info["completion_tokens"]
                st.session_state.total_cost += c_info["total_cost"]
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Lỗi: {e}")
