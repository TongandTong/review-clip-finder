
import streamlit as st
import csv
import os
import webbrowser
from deep_translator import GoogleTranslator

def translate_text(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except Exception as e:
        return f"แปลไม่ได้: {e}"

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

LINKS_FILE = "saved_links.csv"
TERMS_FILE = "search_terms.csv"

def translate_text(text, lang):
    try:
        result = translator.translate(text, dest=lang)
        return result.text
    except:
        return text

def save_link(platform, keyword, link):
    if not link:
        st.warning("Please paste a link before saving.")
        return
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Platform", "Keyword", "Link"])
    with open(LINKS_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([platform, keyword, link])
    st.success(f"Link saved for {platform}.")

def save_search_term(term):
    if not os.path.exists(TERMS_FILE):
        with open(TERMS_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Search Term"])
    terms = get_recent_terms()
    if term not in terms:
        with open(TERMS_FILE, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([term])

def get_recent_terms(n=5):
    if not os.path.exists(TERMS_FILE):
        return []
    with open(TERMS_FILE, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))[1:]
    return [row[0] for row in reader][-n:]

def load_links():
    if not os.path.exists(LINKS_FILE):
        return []
    with open(LINKS_FILE, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))[1:]

def delete_link(index):
    rows = load_links()
    if index < len(rows):
        del rows[index]
        with open(LINKS_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Platform", "Keyword", "Link"])
            writer.writerows(rows)

def main():
    st.set_page_config(page_title="Review Clip Finder", layout="centered")
    st.markdown("<h2 style='text-align: center;'>🎬 Review Clip Finder</h2>", unsafe_allow_html=True)

    st.markdown("### 🔍 Enter your search term (Thai)")
    keyword = st.text_input("Search Term", key="search_term")

    if keyword:
        save_search_term(keyword)

    platform_names = [p["name"] for p in PLATFORMS]
    selected_platform = st.selectbox("Platform", platform_names)
    selected = next((p for p in PLATFORMS if p["name"] == selected_platform), PLATFORMS[0])

    auto_translate = st.checkbox("Auto-translate (editable)", value=True)
    use_original = st.checkbox("Use original Thai term", value=False)

    translated_text = translate_text(keyword, selected["lang"]) if auto_translate else keyword
    if auto_translate:
        translated_text = st.text_input("Translated Term", translated_text, key="translated")

    search_term = keyword if use_original else translated_text
    search_url = selected["search_url"] + search_term

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Search"):
            st.markdown(f"[Open Search Page]({search_url})", unsafe_allow_html=True)
    with col2:
        if st.button("Copy Term"):
            st.write("Copied to clipboard: ", search_term)

    st.markdown("---")
    st.markdown("### 📎 Link Management")
    paste_link = st.text_input("Paste your link here")
    if st.button("Save Link"):
        save_link(selected["name"], keyword, paste_link)

    st.markdown("### 🔗 Saved Links")
    links = load_links()
    for idx, row in enumerate(links):
        plat, key, link = row
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"**{plat}** | {key}")
            st.markdown(f"[{link}]({link})")
        with col2:
            if st.button(f"Open Downloader {idx}", key=f"open{idx}"):
                webbrowser.open(next((p["download"] for p in PLATFORMS if p["name"] == plat), "#"))
        with col3:
            if st.button(f"Delete {idx}", key=f"delete{idx}"):
                delete_link(idx)
                st.experimental_rerun()

    st.markdown("---")
    st.markdown("### 🕘 Recent Search Terms")
    for term in reversed(get_recent_terms()):
        st.write(f"• {term}")

if __name__ == "__main__":
    main()
