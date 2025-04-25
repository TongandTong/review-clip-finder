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
    {"name": "Dailymotion", "lang": "en", "search_url": "https://www.dailymotion.com/search/", "download": "https://www.savethevideo.com/dailymotion-downloader"}
]

saved_file = "saved_links.csv"

def translate_text(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except Exception as e:
        return f"แปลไม่ได้: {e}"

def save_link(platform, keyword, link):
    if not link:
        st.warning("กรุณาวางลิงก์ก่อนบันทึก")
        return
    with open(saved_file, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([platform, keyword, link])
    st.success(f"บันทึกข้อมูลจาก {platform} แล้ว")

def show_saved_links(filter_platform=None):
    if not os.path.exists(saved_file):
        st.info("ยังไม่มีข้อมูลที่บันทึกไว้")
        return
    with open(saved_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            plat, keyword, link = row
            if filter_platform and plat != filter_platform:
                continue
            st.markdown(f"**{plat}** | _{keyword}_ | [เปิดลิงก์]({link})")

st.title("📹 Review Clip Finder")
query = st.text_input("🔍 คำค้น (ไทย)", "")

if st.button("แปลทั้งหมด"):
    for platform in platforms:
        lang = platform['lang']
        translated = translate_text(query, lang)
        st.session_state[f"trans_{platform['name']}"] = translated

cols = st.columns(3)
for i, platform in enumerate(platforms):
    with cols[i % 3]:
        st.subheader(platform['name'])
        key = f"trans_{platform['name']}"
        if key not in st.session_state:
            st.session_state[key] = ""
        st.session_state[key] = st.text_input("คำแปล", st.session_state[key], key=key)

        if st.button(f"ค้นหา - {platform['name']}"):
            url = platform['search_url'] + st.session_state[key]
            st.markdown(f"[เปิดการค้นหา]({url})", unsafe_allow_html=True)

        link = st.text_input(f"ลิงก์จาก {platform['name']}", key=f"link_{platform['name']}")
        if st.button(f"บันทึกลิงก์ - {platform['name']}"):
            save_link(platform['name'], query, link)
        if st.button(f"ดูทั้งหมด - {platform['name']}"):
            show_saved_links(platform['name'])
        st.markdown(f"[ไปหน้าโหลด]({platform['download']})", unsafe_allow_html=True)
