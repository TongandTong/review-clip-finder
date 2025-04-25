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

HISTORY_FILE = "search_history.json"
SUGGESTION_MAP = {
    "เสื้อ": ["เสื้อผ้าแฟชั่น", "เสื้อยืดเกาหลี", "แฟชั่นหน้าร้อน"],
    "รองเท้า": ["รองเท้าผ้าใบ", "รีวิวรองเท้า", "รองเท้าออกกำลังกาย"],
    "เที่ยว": ["สถานที่ท่องเที่ยว", "รีวิวที่เที่ยว", "ที่เที่ยวธรรมชาติ"]
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(term):
    history = load_history()
    if term not in history:
        history.insert(0, term)
        if len(history) > 20:
            history.pop()
        save_history(history)

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
.tag {
    display: inline-block;
    background-color: #eee;
    padding: 5px 10px;
    margin: 5px;
    border-radius: 15px;
    cursor: pointer;
}
.tag:hover {
    background-color: #ddd;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='boxed-section'>", unsafe_allow_html=True)
    st.markdown("### 🔍 คำค้น (ไทย)")
    keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state.get("keyword", ""), label_visibility="collapsed", key="main_input")

    history = load_history()
    if keyword:
        add_to_history(keyword)

    if history:
        st.markdown("**📜 คำค้นที่ผ่านมา:**")
        cols = st.columns([1, 1, 1])
        for idx, tag in enumerate(history):
            if cols[idx % 3].button(tag, key=f"tag_{tag}"):
                st.session_state["main_input"] = tag
                st.experimental_rerun()
        if st.button("🗑 ลบทั้งหมด"):
            save_history([])
            st.experimental_rerun()

    if keyword in SUGGESTION_MAP:
        st.markdown("**🎯 คำแนะนำ:**")
        sug_cols = st.columns(len(SUGGESTION_MAP[keyword]))
        for i, sug in enumerate(SUGGESTION_MAP[keyword]):
            if sug_cols[i].button(sug, key=f"sug_{sug}"):
                st.session_state["main_input"] = sug
                st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

translated_terms = {}
if keyword:
    for plat in platforms:
        try:
            translated_text = translator.translate(keyword, dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

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
