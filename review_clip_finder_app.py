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

    def delete_line(index):
        with open(saved_file, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        if index < len(rows):
            del rows[index]
            with open(saved_file, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            st.experimental_rerun()

    st.subheader("ลิงก์ที่บันทึกไว้")
    saved_links = []
    with open(saved_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        for idx, row in enumerate(reader):
            if idx == 0 or not row:
                continue
            plat, link = row
            if filter_platform and plat != filter_platform:
                continue
            saved_links.append((plat, link))

    if not saved_links:
        st.info("ยังไม่มีลิงก์บันทึกไว้")
    for plat, link in saved_links:
        st.text(f"{plat} | {link}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"ลบ {plat}", key=f"delete_{plat}"):
                delete_line(saved_links.index((plat, link)))
        with col2:
            download_url = next((p["download"] for p in platforms if p["name"] == plat), "")
            if download_url:
                if st.button(f"ไปหน้าโหลด {plat}", key=f"download_{plat}"):
                    webbrowser.open(download_url)


def search_platform(platform, keyword, use_translation=True):
    lang = platform['lang']
    search_term = keyword if not use_translation else translate_text(keyword, lang)
    url = platform['search_url'] + search_term
    if use_translation:
        st.session_state.search_term = search_term
    webbrowser.open(url)


def copy_to_clipboard(text):
    st.text_area("คัดลอกข้อความนี้:", text, height=50)
    st.button("คัดลอก", on_click=lambda: st.text(text))


def build_gui():
    st.title("Review Clip Finder")
    st.subheader("🔍 คำค้น (ไทย)")
    
    query_entry = st.text_input("คำค้น (Search Keyword)", "", key="search_query")
    use_trans_var = st.checkbox("ค้นหาด้วยคำแปล", value=True)

    st.button("แปลทั้งหมด", on_click=lambda: translate_all(query_entry))

    st.subheader("🕘 คำค้นล่าสุด")
    recent_keywords = get_recent_keywords()
    for kw in recent_keywords:
        if st.button(kw):
            st.session_state.search_query = kw

    platform_widgets = []
    for platform in platforms:
        col1, col2, col3 = st.columns(3)

        with col1:
            trans_entry = st.text_input(f"{platform['name']} (แปล)", "", key=f"trans_{platform['name']}")
        with col2:
            if st.button(f"ค้นหา {platform['name']}", key=f"search_{platform['name']}"):
                search_platform(platform, query_entry, use_trans_var)
        with col3:
            link_entry = st.text_input(f"{platform['name']} (ลิงก์)", "", key=f"link_{platform['name']}")
            if st.button(f"บันทึกลิงก์ {platform['name']}", key=f"save_{platform['name']}"):
                save_link(platform['name'], query_entry, link_entry)

    st.button("ดูลิงก์ที่บันทึกไว้", on_click=lambda: show_saved_links())


if __name__ == "__main__":
    build_gui()
