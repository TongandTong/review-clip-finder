import streamlit as st
import csv
import os
import webbrowser
from googletrans import Translator

translator = Translator()

PLATFORMS = [
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

SAVED_FILE = "saved_links.csv"

# --- Utils ---
def translate_text(text, lang):
    try:
        return translator.translate(text, dest=lang).text
    except:
        return text

def save_link(platform, keyword, link):
    with open(SAVED_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([platform, keyword, link])

def load_saved_links():
    if not os.path.exists(SAVED_FILE):
        return []
    with open(SAVED_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [dict(platform=row[0], keyword=row[1], link=row[2]) for row in reader if row]

def delete_link(index):
    links = load_saved_links()
    if index < len(links):
        links.pop(index)
        with open(SAVED_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for item in links:
                writer.writerow([item['platform'], item['keyword'], item['link']])

# --- UI ---
st.set_page_config(page_title="Review Clip Finder", layout="centered")
st.title("📽️ Review Clip Finder")

query = st.text_input("Search Keyword (Thai)", max_chars=100)
platform_names = [p['name'] for p in PLATFORMS]
selected_platform_name = st.selectbox("Choose Platform", platform_names)
selected_platform = next(p for p in PLATFORMS if p['name'] == selected_platform_name)

mode = st.radio("Search Mode", ["Original (Thai)", "Translated"])

if st.button("🔍 Search"):
    search_term = query
    if mode == "Translated":
        search_term = translate_text(query, selected_platform['lang'])
    search_url = selected_platform['search_url'] + search_term
    st.markdown(f"[🌐 Open Search Link]({search_url})", unsafe_allow_html=True)

    st.session_state['translated'] = search_term

# Auto-translate but editable
if 'translated' in st.session_state:
    edited = st.text_input("Edit Translated (Optional)", value=st.session_state['translated'])
else:
    edited = ""

link_input = st.text_input("Paste the Video Link")

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save Link"):
        if link_input:
            save_link(selected_platform_name, edited or query, link_input)
            st.success("Saved successfully!")
        else:
            st.warning("Please paste a link before saving.")

with col2:
    if st.button("📂 View Saved Links"):
        st.session_state['show_links'] = True

# --- Saved Links ---
if st.session_state.get('show_links'):
    st.subheader("🔗 Saved Links")
    links = load_saved_links()
    if not links:
        st.info("No saved links yet.")
    else:
        for i, entry in enumerate(links):
            st.markdown(f"**Platform:** {entry['platform']}  ")
            st.markdown(f"**Keyword:** {entry['keyword']}  ")
            st.markdown(f"**Link:** {entry['link']}  ")
            search_url = next(p['search_url'] for p in PLATFORMS if p['name'] == entry['platform'])
            download_url = next(p['download'] for p in PLATFORMS if p['name'] == entry['platform'])

            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.markdown(f"[🌐 Search Again]({search_url + entry['keyword']})", unsafe_allow_html=True)
            with col2:
                st.markdown(f"[⬇️ Go to Download Page]({download_url})", unsafe_allow_html=True)
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    delete_link(i)
                    st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ to find your review clips faster")
