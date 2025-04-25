import streamlit as st
from googletrans import Translator
import csv
import os
import webbrowser

translator = Translator()

platforms = [
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
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"}
]

saved_file = "saved_links.csv"

def translate_text(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except Exception as e:
        return f"แปลไม่ได้: {e}"

st.set_page_config(page_title="Review Clip Finder", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .input-container {
            border: 1px solid #ccc;
            padding: 1rem;
            border-radius: 10px;
            background-color: #fafafa;
            margin-bottom: 2rem;
        }
        .platform-box {
            border: 1px solid #ccc;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            background-color: #ffffff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .stButton>button {
            margin: 0.2rem 0.2rem 0.2rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- Input Section ---
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown("### 🔍 คำค้น (ไทย)")
    query_text = st.text_input("ใส่คำค้น", key="main_query", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Platform Grid ---
col1, col2 = st.columns(2)

for i, platform in enumerate(platforms):
    with (col1 if i % 2 == 0 else col2):
        with st.container():
            with st.expander(platform["name"]):
                st.markdown('<div class="platform-box">', unsafe_allow_html=True)

                lang = platform["lang"]
                translated_text = translate_text(query_text, lang) if query_text else ""
                trans_input = st.text_input(f"คำค้นสำหรับ {platform['name']}", value=translated_text, key=f"trans_{i}")

                col_search, col_download = st.columns(2)

                with col_search:
                    if st.button("🔎 ค้นหา", key=f"search_{i}"):
                        search_url = platform["search_url"] + trans_input
                        st.markdown(f"[🔗 เปิดลิงก์ค้นหา]({search_url})", unsafe_allow_html=True)

                with col_download:
                    if st.button("⬇️ ไปหน้าโหลด", key=f"download_{i}"):
                        download_url = platform["download"]
                        st.markdown(f"[🔗 เปิดหน้าโหลด]({download_url})", unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
