import streamlit as st
import webbrowser
import csv
import os
from googletrans import Translator

st.set_page_config(layout="wide", page_title="Review Clip Finder")

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

def translate_text(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except:
        return text

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

def save_link(platform, keyword, link):
    if not link:
        st.warning("กรุณาวางลิงก์ก่อนบันทึก")
        return
    write_header = not os.path.exists(saved_file)
    with open(saved_file, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["แพลตฟอร์ม", "ลิงก์"])
        writer.writerow([platform, link])
    st.success(f"บันทึกลิงก์จาก {platform} แล้ว")

def show_saved_links(filter_platform=None):
    if not os.path.exists(saved_file):
        st.info("ยังไม่มีข้อมูลที่บันทึกไว้")
        return
    with open(saved_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        for idx, row in enumerate(reader):
            if idx == 0 or not row:
                continue
            plat, link = row
            if filter_platform and plat != filter_platform:
                continue
            st.markdown(f"**{plat}** | [{link}]({link})")
            col1, col2 = st.columns(2)
            if col1.button(f"ลบ {idx}", key=f"del_{idx}"):
                del reader[idx]
                with open(saved_file, "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(reader)
                st.rerun()
            download_url = next((p["download"] for p in platforms if p["name"] == plat), "")
            if download_url:
                if col2.button("ไปหน้าโหลด", key=f"dl_{idx}"):
                    webbrowser.open(download_url)

st.markdown("""
    <style>
    .stTextInput > div > input {
        background-color: #fffbe6;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
    }
    .stButton > button:hover {
        background-color: #125a8c;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Review Clip Finder")
query = st.text_input("คำค้น (ไทย)", "")
col1, col2, col3 = st.columns([1,1,2])
use_trans = col1.checkbox("ใช้คำแปล", value=True)

if col2.button("แปลทั้งหมด"):
    save_recent_keyword(query)

st.markdown("### 🕘 คำค้นล่าสุด")
recent_keywords = get_recent_keywords()
st.write(recent_keywords)

left_col, right_col = st.columns(2)

for idx, platform in enumerate(platforms):
    target_col = left_col if idx % 2 == 0 else right_col
    with target_col.container():
        st.markdown(f"#### {platform['name']}")
        trans = ""
        if use_trans:
            trans = translate_text(query, platform['lang'])
        else:
            trans = query
        st.text_input("คำค้น (แปลแล้ว)", value=trans, key=f"trans_{idx}")
        c1, c2 = st.columns(2)
        if c1.button("ค้นหา", key=f"search_{idx}"):
            url = platform['search_url'] + trans
            webbrowser.open(url)
        if c2.button("ไปหน้าโหลด", key=f"download_{idx}"):
            webbrowser.open(platform['download'])
        link = st.text_input("วางลิงก์ที่นี่", key=f"link_{idx}")
        if st.button("บันทึกลิงก์", key=f"save_{idx}"):
            save_link(platform['name'], query, link)
        if st.button("ดูลิงก์ที่บันทึกไว้", key=f"view_{idx}"):
            show_saved_links(platform['name'])
