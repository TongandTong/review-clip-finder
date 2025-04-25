import streamlit as st
import webbrowser
from googletrans import Translator
import json
import os
import openai

translator = Translator()

HISTORY_FILE = "search_history.json"

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
.suggestion-btn {
    display: inline-block;
    background-color: #eee;
    border: none;
    border-radius: 10px;
    padding: 5px 10px;
    margin: 5px 5px 0 0;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

if "suggestions" not in st.session_state:
    st.session_state["suggestions"] = []

# GPT API Key (replace this with your actual key)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-xxx")  # Replace 'sk-xxx' with your key or use environment variable

def get_ai_suggestions(keyword):
    try:
        prompt = f"แนะนำคำค้นเพิ่มเติมที่เกี่ยวข้องกับ '{keyword}' อย่างสั้นๆ 3 คำ"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.7,
        )
        suggestions = response['choices'][0]['message']['content'].strip().split(',')
        return [s.strip() for s in suggestions if s.strip()]
    except Exception as e:
        return []

def on_input_change():
    keyword = st.session_state["keyword_input"]
    st.session_state["suggestions"] = get_ai_suggestions(keyword)

with st.container():
    st.markdown("<div class='boxed-section'>", unsafe_allow_html=True)
    st.markdown("### 🔍 คำค้น (ไทย)")
    keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed", key="keyword_input", on_change=on_input_change)
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state["keyword"] = keyword

translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# แสดงปุ่มคำแนะนำเป็นแนวนอน
if st.session_state["suggestions"]:
    st.markdown("<div style='margin-top: -10px;'>", unsafe_allow_html=True)
    sugg_cols = st.columns(len(st.session_state["suggestions"]))
    for idx, s in enumerate(st.session_state["suggestions"]):
        if sugg_cols[idx].button(s, key=f"sugg_{s}"):
            st.session_state["keyword_input"] += " " + s
            st.session_state["suggestions"] = []
            st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

columns = st.columns(2)
half = len(platforms) // 2

for col_idx, start in enumerate([0, half]):
    with columns[col_idx]:
        for i in range(start, start + half):
            if i >= len(platforms): break
            plat = platforms[i]
            with st.expander(plat["name"], expanded=False):
                search_term = st.text_input(f"คำค้นหา ({plat['name']})", value=translated_terms.get(plat["name"], ""), key=f"term_{plat['name']}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("ค้นหา", key=f"search_{plat['name']}"):
                        search_url = plat["search_url"] + search_term
                        js = f"window.open('{search_url}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
                with col2:
                    if st.button("ไปหน้าโหลด", key=f"dl_{plat['name']}"):
                        js = f"window.open('{plat['download']}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
