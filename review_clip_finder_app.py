import streamlit as st
from googletrans import Translator
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
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"},
]

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Review Clip Finder</h1>", unsafe_allow_html=True)

# Session init
if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""
if "translated_terms" not in st.session_state:
    st.session_state["translated_terms"] = {}

# Function to clear all data
def clear_data():
    st.session_state["keyword"] = ""
    st.session_state["translated_terms"] = {}
    st.session_state.clear()  # Clear session state to reset the input fields

def translate_keyword():
    if st.session_state["keyword"].strip() != "":
        for plat in platforms:
            try:
                translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
            except Exception as e:
                translated_text = f"แปลไม่ได้: {e}"
            st.session_state["translated_terms"][plat["name"]] = translated_text

# Input for keyword
st.markdown("### 🔍 คำค้น (ไทย)")
keyword_input = st.text_input("พิมพ์คำค้นหา", value=st.session_state["keyword"], on_change=translate_keyword)

# Add Clear Data button beside Translate button
col_translate, col_clear = st.columns([1, 1])
with col_translate:
    if st.button("แปลคำ"):
        translate_keyword()

with col_clear:
    if st.button("ล้างข้อมูล"):
        clear_data()

# UI per platform
columns = st.columns(2)
half = len(platforms) // 2

for col_idx, start in enumerate([0, half]):
    with columns[col_idx]:
        for i in range(start, start + half):
            if i >= len(platforms): break
            plat = platforms[i]
            with st.expander(plat["name"], expanded=False):
                default_term = st.session_state["translated_terms"].get(plat["name"], "")
                search_term = st.text_input(f"คำค้นหา ({plat['name']})", value=default_term, key=f"term_{plat['name']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("ค้นหา", key=f"search_{plat['name']}"):
                        search_url = plat["search_url"] + search_term
                        js = f"window.open('{search_url}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
                with col2:
                    if st.button("ไปหน้าโหลด", key=f"dl_{plat['name']}"):
                        js = f"window.open('{plat['download']}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
