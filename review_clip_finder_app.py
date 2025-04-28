import streamlit as st
from googletrans import Translator
import json
import os

translator = Translator()

platforms = [
    {"name": "FaceBook", "lang": "en", "search_url": "https://www.facebook.com/search/top/?q=", "download": "https://fdown.net/"},
    {"name": "Douyin", "lang": "zh-cn", "search_url": "https://www.douyin.com/search/", "download": "https://savetik.co/en/douyin-downloader"},
    {"name": "Xiaohongshu", "lang": "zh-cn", "search_url": "https://www.xiaohongshu.com/search_result/", "download": "https://bravedown.com/xiaohongshu-downloader"},
    {"name": "Pinterest", "lang": "en", "search_url": "https://www.pinterest.com/search/pins/?q=", "download": "https://pinterestdownloader.com/"},
    {"name": "Bilibili", "lang": "zh-cn", "search_url": "https://search.bilibili.com/all?keyword=", "download": "https://bravedown.com/th/bilibili-downloader"},
    {"name": "Weibo", "lang": "zh-cn", "search_url": "https://s.weibo.com/weibo?q=", "download": "https://bravedown.com/th/weibo-video-downloader"},
    {"name": "YouTube", "lang": "en", "search_url": "https://www.youtube.com/results?search_query=", "download": "https://en1.savefrom.net/1-youtube-video-downloader-8jH/"},
    {"name": "TikTok", "lang": "th", "search_url": "https://www.tiktok.com/search?q=", "download": "https://snaptik.app/en2"},
    {"name": "Instagram", "lang": "en", "search_url": "https://www.instagram.com/explore/tags/", "download": "https://snapins.ai/"},
    {"name": "Zhihu", "lang": "zh-cn", "search_url": "https://www.zhihu.com/search?q=", "download": "https://www.videofk.com/zhihu-video-download"},
    {"name": "Youku", "lang": "zh-cn", "search_url": "https://so.youku.com/search_video/q_", "download": "https://www.locoloader.com/youku-video-downloader/"},
    {"name": "Dailymotion", "lang": "en", "search_url": "https://www.dailymotion.com/search/", "download": "https://www.savethevideo.com/dailymotion-downloader"},
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"},
]

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Review Clip Finder</h1>", unsafe_allow_html=True)

st.markdown("""

""", unsafe_allow_html=True)

if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

st.markdown("<div class='boxed-section'>", unsafe_allow_html=True)
st.markdown("### 🔍 คำค้น (ไทย)")

new_keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed")

if new_keyword != st.session_state["keyword"]:
    st.session_state["keyword"] = new_keyword

st.markdown("</div>", unsafe_allow_html=True)

translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# การจัดเรียงปุ่มให้มีขนาดเท่ากัน
num_columns = 7  # กำหนดจำนวนคอลัมน์ในแต่ละแถว
num_rows = (len(platforms) + num_columns - 1) // num_columns  # คำนวณจำนวนแถว

# สร้างคอลัมน์ตามจำนวนที่คำนวณ
columns = st.columns(num_columns)

# ใช้คอลัมน์เพื่อจัดเรียงปุ่มในแถวเดียว
selected_platform = None

for i in range(num_rows):
    with st.container():  # ใช้ container เพื่อรวมปุ่มในแถวเดียวกัน
        for j in range(num_columns):
            index = i * num_columns + j
            if index < len(platforms):  # เช็คว่า index อยู่ในขอบเขตของ platforms
                plat = platforms[index]
                with columns[j]:
                    # ปรับปุ่มให้ไม่มีสีพื้นหลังและขนาดเท่ากัน
                    button = st.button(plat["name"], key=f"button_{plat['name']}", help=plat["name"])
                    if button:
                        selected_platform = plat

if selected_platform:
    # แสดงผลเฉพาะเมื่อกดปุ่ม
    st.markdown(f"### แพลตฟอร์มที่เลือก: {selected_platform['name']}")
    search_term = st.text_input(f"คำค้นหา ({selected_platform['name']})", value=translated_terms.get(selected_platform["name"], ""), key=f"term_{selected_platform['name']}")

    # ใช้ container เพื่อจัดปุ่มให้อยู่กลางหน้า
    col1, col2 = st.columns([1, 1])  # กำหนดความกว้างของคอลัมน์ให้เท่ากัน

    with col1:
        search_url = selected_platform["search_url"] + search_term
        # ปรับสไตล์ของปุ่ม "ค้นหา" ให้ไม่มีกรอบและพื้นหลัง
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{search_url}" target="_blank" style="
                display: inline-block;
                width: 100%;
                padding: 10px;
                background-color: transparent;
                color: inherit;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
                font-size: 14px;
                border: none;
                box-sizing: border-box;
            ">ค้นหาบน {selected_platform['name']}</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        download_url = selected_platform["download"]
        # ปรับสไตล์ของปุ่ม "ไปหน้าโหลด" ให้ไม่มีกรอบและพื้นหลัง
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{download_url}" target="_blank" style="
                display: inline-block;
                width: 100%;
                padding: 10px;
                background-color: transparent;
                color: inherit;
                text-align: center;
                border-radius: 5px;
                text-decoration: none;
                font-size: 14px;
                border: none;
                box-sizing: border-box;
            ">ไปหน้าโหลด {selected_platform['name']}</a>
        </div>
        """, unsafe_allow_html=True)
