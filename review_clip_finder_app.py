import streamlit as st
import csv
import os
import webbrowser
from googletrans import Translator

st.set_page_config(page_title="Review Clip Finder", layout="wide")
translator = Translator()

saved_file = "saved_links.csv"
recent_file = "recent_keywords.txt"

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

def translate_text(text, lang):
    try:
        return translator.translate(text, dest=lang).text
    except Exception as e:
        return f"แปลไม่ได้: {e}"

def save_link(platform, link):
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

def get_recent_keywords():
    if not os.path.exists(recent_file):
        return []
    with open(recent_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

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

st.title("📹 Review Clip Finder")

query = st.text_input("🔍 คำค้น (ไทย)", "")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    use_trans = st.checkbox("ค้นหาด้วยคำแปล", value=True)
with col2:
    if st.button("แปลทั้งหมด"):
        save_recent_keyword(query)

with col3:
    recent = get_recent_keywords()
    if recent:
        st.caption("🕘 คำค้นล่าสุด:")
        st.write(" | ".join(recent))

# แบ่งเป็น 2 คอลัมน์แนวตั้ง
left_col, right_col = st.columns(2)

for i, platform in enumerate(platforms):
    col = left_col if i % 2 == 0 else right_col
    with col:
        with st.container():
            st.markdown(f"### {platform['name']}")
            trans = translate_text(query, platform['lang']) if use_trans else query
            st.text_input("คำค้นแปลแล้ว", trans, key=f"trans_{platform['name']}")
            if st.button("ค้นหา", key=f"search_{platform['name']}"):
                search_url = platform["search_url"] + trans
                st.markdown(f"[🔗 ค้นหาใน {platform['name']}]({search_url})", unsafe_allow_html=True)
                st.markdown(f'<meta http-equiv="refresh" content="0; url={search_url}">', unsafe_allow_html=True)
            link = st.text_input("🔗 วางลิงก์", key=f"link_{platform['name']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("บันทึกลิงก์", key=f"save_{platform['name']}"):
                    save_link(platform['name'], link)
            with col2:
                if st.button("ไปหน้าโหลด", key=f"download_{platform['name']}"):
                    st.markdown(f"[🔗 ไปที่หน้าโหลด]({platform['download']})", unsafe_allow_html=True)
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={platform["download"]}">', unsafe_allow_html=True)
            with col3:
                if os.path.exists(saved_file):
                    with open(saved_file, newline='', encoding='utf-8') as f:
                        rows = list(csv.reader(f))
                        links = [r[1] for r in rows if len(r) > 1 and r[0] == platform['name']]
                        if links:
                            st.caption("🔗 ลิงก์ที่บันทึกไว้:")
                            for l in links[-3:]:
                                st.markdown(f"- [{l}]({l})")
