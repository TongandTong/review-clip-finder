# review_clip_finder_app.py

import streamlit as st
import csv
import webbrowser
from googletrans import Translator
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
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"}
]

saved_file = "saved_links.csv"
recent_file = "recent_keywords.txt"

st.set_page_config(layout="wide", page_title="Review Clip Finder")
st.markdown("""
    <style>
    .platform-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    .stTextInput>div>div>input {
        background-color: #FAFAFA;
        color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📽️ Review Clip Finder")

query = st.text_input("🔍 คำค้น (ไทย)", "")
use_translate = st.checkbox("ค้นหาด้วยคำแปล", value=True)

if st.button("แปลทั้งหมด"):
    for p in platforms:
        lang = p["lang"]
        try:
            translated = translator.translate(query, dest=lang).text
        except Exception as e:
            translated = f"แปลไม่ได้: {e}"
        st.session_state[f"translated_{p['name']}"] = translated

cols = st.columns(6)
for i, platform in enumerate(platforms):
    with cols[i % 6]:
        with st.container():
            st.markdown(f"<div class='platform-card'><h4>{platform['name']}</h4>", unsafe_allow_html=True)
            key = f"translated_{platform['name']}"
            default_value = st.session_state.get(key, "")
            translated = st.text_input(f"คำแปล ({platform['lang']})", value=default_value, key=key)

            search_url = platform['search_url'] + (translated if use_translate else query)
            download_url = platform['download']

            st.link_button("ค้นหา", search_url, use_container_width=True)
            st.link_button("ไปหน้าโหลด", download_url, use_container_width=True)

            link_key = f"link_{platform['name']}"
            link_input = st.text_input("ลิงก์วางที่นี่", key=link_key)

            if st.button(f"บันทึกลิงก์จาก {platform['name']}", key=f"save_{platform['name']}"):
                if not link_input:
                    st.warning("กรุณาวางลิงก์ก่อนบันทึก")
                else:
                    write_header = not os.path.exists(saved_file)
                    with open(saved_file, "a", newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        if write_header:
                            writer.writerow(["แพลตฟอร์ม", "ลิงก์"])
                        writer.writerow([platform['name'], link_input])
                    st.success(f"✅ บันทึกลิงก์จาก {platform['name']} แล้ว")

            st.markdown("</div>", unsafe_allow_html=True)

if st.button("🔗 ดูลิงก์ทั้งหมด"):
    if not os.path.exists(saved_file):
        st.info("ยังไม่มีข้อมูลที่บันทึกไว้")
    else:
        with open(saved_file, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
            for row in rows[1:]:
                st.write(f"{row[0]} | {row[1]}")
