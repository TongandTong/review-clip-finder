import streamlit as st
import webbrowser
from googletrans import Translator
import json
import os

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

st.markdown("""
<style>
.boxed-section {
    border: 2px solid #ccc;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Session state setup
if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

# Input field
with st.container():
    st.markdown("<div class='boxed-section'>", unsafe_allow_html=True)
    st.markdown("### 🔍 คำค้น (ไทย)")
    keyword_input = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed", key="keyword_input")
    st.markdown("</div>", unsafe_allow_html=True)

# Only update if changed (and not empty)
if keyword_input.strip() and keyword_input != st.session_state["keyword"]:
    st.session_state["keyword"] = keyword_input

# Translation logic
translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# Show platform sections
columns = st.columns(2)
half = len(platforms) // 2

for col_idx, start in enumerate([0, half]):
    with columns[col_idx]:
        for i in range(start, start + half):
            if i >= len(platforms): break
            plat = platforms[i]
            with st.expander(plat["name"], expanded=False):
                search_term = st.text_input(f"คำค้นหา ({plat['name']})", value=translated_terms.get(plat["name"], ""), key=f"term_{plat['name']}")
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
