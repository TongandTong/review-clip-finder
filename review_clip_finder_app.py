import streamlit as st
import csv
import os
import webbrowser
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
    {"name": "Dailymotion", "lang": "en", "search_url": "https://www.dailymotion.com/search/", "download": "https://www.savethevideo.com/dailymotion-downloader"}
]

saved_file = "saved_links.csv"
recent_file = "recent_keywords.txt"

def translate_text(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except Exception as e:
        return f"แปลไม่ได้: {e}"

def save_recent_keyword(keyword):
    if not keyword.strip():
        return
    recent = []
    if os.path.exists(recent_file):
        with open(recent_file, "r", encoding="utf-8") as f:
            recent = [line.strip() for line in f if line.strip()]
    if keyword in recent:
        recent.remove(keyword)
    recent.insert(0, keyword)
    recent = recent[:5]
    with open(recent_file, "w", encoding="utf-8") as f:
        for kw in recent:
            f.write(kw + "\n")

def get_recent_keywords():
    if not os.path.exists(recent_file):
        return []
    with open(recent_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def translate_all(keyword):
    for platform in platforms:
        lang = platform["lang"]
        translated = translate_text(keyword, lang)
        st.session_state[f"trans_{platform['name']}"] = translated

def build_gui():
    st.title("Review Clip Finder")

    query_entry = st.text_input("\U0001F50D คำค้น (ไทย)", "")

    if st.button("แปลทั้งหมด"):
        translate_all(query_entry)
        save_recent_keyword(query_entry)

    st.markdown("---")
    st.write("\U0001F553 คำค้นล่าสุด:")
    cols = st.columns(5)
    for i, kw in enumerate(get_recent_keywords()):
        with cols[i % 5]:
            if st.button(kw):
                st.session_state["query"] = kw

    for platform in platforms:
        with st.expander(platform["name"]):
            trans_key = f"trans_{platform['name']}"
            trans_value = st.session_state.get(trans_key, "")
            trans_entry = st.text_input(f"คำแปลสำหรับ {platform['name']}", value=trans_value, key=trans_key)

            if st.button(f"ค้นหา {platform['name']}"):
                search_term = trans_entry
                url = platform['search_url'] + search_term
                st.write(f"[ไปที่ลิงก์ค้นหา]({url})")

            if st.button(f"ไปหน้าโหลด {platform['name']}"):
                st.write(f"[ลิงก์ดาวน์โหลด]({platform['download']})")

if __name__ == "__main__":
    build_gui()
