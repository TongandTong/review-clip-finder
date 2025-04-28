import streamlit as st
from googletrans import Translator

translator = Translator()

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

if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

new_keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed")

if new_keyword != st.session_state["keyword"]:
    st.session_state["keyword"] = new_keyword

translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# การจัดเรียงปุ่มให้มีขนาดเท่ากันและอยู่ใน 2 แถว
num_columns = 7
num_rows = (len(platforms) + num_columns - 1) // num_columns
columns = st.columns(num_columns)

selected_platform = None

for i in range(num_rows):
    with st.container():
        for j in range(num_columns):
            index = i * num_columns + j
            if index < len(platforms):
                plat = platforms[index]
                with columns[j]:
                    if st.button(plat["name"], key=f"button_{plat['name']}", use_container_width=True):
                        selected_platform = plat

if selected_platform:
    st.markdown(f"### แพลตฟอร์มที่เลือก: {selected_platform['name']}")
    search_term = st.text_input(f"คำค้นหา ({selected_platform['name']})", value=translated_terms.get(selected_platform["name"], ""), key=f"term_{selected_platform['name']}")

    # ปรับปุ่ม "ค้นหา" และ "ไปหน้าโหลด" ให้ขนาดเท่ากับปุ่มเลือกเวป
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("ค้นหา", key=f"search_{selected_platform['name']}", use_container_width=True):
            search_url = selected_platform["search_url"] + search_term
            # ใช้ st.markdown สำหรับเปิดลิงก์ในแท็บใหม่
            st.markdown(f'<a href="{search_url}" target="_blank">เปิดหน้าค้นหา {selected_platform["name"]}</a>', unsafe_allow_html=True)
    with col2:
        if st.button("ไปหน้าโหลด", key=f"dl_{selected_platform['name']}", use_container_width=True):
            # ใช้ st.markdown สำหรับเปิดลิงก์ในแท็บใหม่
            st.markdown(f'<a href="{selected_platform["download"]}" target="_blank">ไปหน้าโหลด {selected_platform["name"]}</a>', unsafe_allow_html=True)
