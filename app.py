import streamlit as st
from PIL import Image
from google import genai

# 設定網頁標題
st.set_page_config(page_title="木材小管家", page_icon="🪵")

st.title("🪵 木材小管家 - 廢料變身設計師")
st.write("拍下你剩下的木料廢料，輸入大約尺寸，讓 AI 幫你想想可以做什麼實用小物件！")

# 側邊欄設定 API 金鑰
st.sidebar.header("設定")
api_key = st.sidebar.text_input("請輸入你的 Gemini API Key", type="password")

# 介面：上傳照片與輸入尺寸
uploaded_file = st.file_uploader("上傳木材廢料照片", type=["jpg", "jpeg", "png"])
wood_type = st.text_input("木材種類（例如：胡桃木、台灣檜木，若不確定可留空）")
dimensions = st.text_input("大約尺寸（例如：長 15cm x 寬 5cm）")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="你的木材廢料", use_container_width=True)

# 分析按鈕
if st.button("開始分析木料靈感"):
    if not api_key:
        st.error("請先在側邊欄輸入你的 Gemini API Key！")
    elif uploaded_file is None:
        st.error("請先上傳一張木材廢料的照片！")
    else:
        with st.spinner("木材小管家正在思考設計中..."):
            try:
                # 初始化 Gemini Client
                client = genai.Client(api_key=api_key)
                
                # 提示詞
                prompt = f"這是一塊木材廢料的照片。種類：{wood_type if wood_type else '未知'}，尺寸：{dimensions if dimensions else '未知'}。請提供 3 個實用的木工小物手作點子，並附上簡單的製作步驟。"
                
                # 呼叫模型
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                
                st.success("分析完成！")
                st.markdown("### 💡 設計師建議")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"發生錯誤：{e}")
