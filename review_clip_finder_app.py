import streamlit as st
import csv
import webbrowser
import os
from googletrans import Translator

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

st.set_page_config(layout="wide")
st.title("🔍 Review Clip Finder")

# ------------------ Input Area ------------------ #
with st.container():
    with st.container():
        st.markdown("### 📌 คำค้น")
        search_keyword = st.text_input("กรอกคำค้นหาภาษาไทย", "")
        if "translations" not in st.session_state:
            st.session_state.translations = {}

        if st.button("แปลทั้งหมด"):
            for plat in platforms:
                lang = plat["lang"]
                try:
                    translated = translator.translate(search_keyword, dest=lang).text
                except Exception as e:
                    translated = f"[แปลไม่ได้: {e}]"
                st.session_state.translations[plat["name"]] = translated
            st.success("แปลสำเร็จแล้ว")

# ------------------ Platforms Area ------------------ #
cols = st.columns(2)
half = len(platforms) // 2 + len(platforms) % 2

for col_idx, plat_list in enumerate([platforms[:half], platforms[half:]]):
    with cols[col_idx]:
        for plat in plat_list:
            with st.expander(plat["name"], expanded=False):
                translated_text = st.session_state.translations.get(plat["name"], "")
                st.write("🔁 คำที่แปล:", translated_text)

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"ค้นหาใน {plat['name']}", key=f"search_{plat['name']}"):
                        final_query = translated_text if translated_text else search_keyword
                        search_url = plat["search_url"] + final_query
                        js = f"window.open('{search_url}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)

                with col2:
                    if st.button(f"ไปหน้าโหลด {plat['name']}", key=f"download_{plat['name']}"):
                        download_url = plat["download"]
                        js = f"window.open('{download_url}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
