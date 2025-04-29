import streamlit as st
from googletrans import Translator

translator = Translator()

# รายการแพลตฟอร์ม
platforms = [
    {"name": "FaceBook", "lang": "en", "search_url": "https://www.facebook.com/search/top/?q=", "download": "https://fdown.net/"},
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

# เก็บ keyword
if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

new_keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed")

if new_keyword != st.session_state["keyword"]:
    st.session_state["keyword"] = new_keyword

# แปล keyword ไปหลายภาษา
translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# แสดงปุ่มแพลตฟอร์มเป็น 2 แถว ขนาดเท่ากัน
num_columns = 7
num_rows = 2
columns = st.columns(num_columns)

selected_platform = None

for i in range(num_rows):
    for j in range(num_columns):
        index = i * num_columns + j
        if index < len(platforms):
            plat = platforms[index]
            with columns[j]:
                if st.button(plat["name"], key=f"button_{plat['name']}", use_container_width=True):
                    selected_platform = plat
                    st.session_state["selected_platform"] = plat
                    st.session_state["translated_search"] = translated_terms.get(plat["name"], "")

# แสดงปุ่มค้นหาและดาวน์โหลดเมื่อเลือกแพลตฟอร์ม
if st.session_state.get("selected_platform") is not None:
    selected_platform = st.session_state["selected_platform"]
    translated_search = st.session_state.get("translated_search", "")

    st.markdown(f"### แพลตฟอร์มที่เลือก: {selected_platform['name']}")
    search_term = st.text_input(f"คำค้นหา ({selected_platform['name']})", value=translated_search, key=f"term_{selected_platform['name']}")

    search_url = selected_platform["search_url"] + search_term
    download_url = selected_platform["download"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<a href="{search_url}" target="_blank" style="text-decoration: none;">'
            f'<button style="width: 100%; padding: 0.75em; font-size: 1em;">ค้นหา</button></a>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<a href="{download_url}" target="_blank" style="text-decoration: none;">'
            f'<button style="width: 100%; padding: 0.75em; font-size: 1em;">ไปหน้าโหลด</button></a>',
            unsafe_allow_html=True
        )
