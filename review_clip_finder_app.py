import streamlit as st
from googletrans import Translator

translator = Translator()

# รายการแพลตฟอร์ม
platforms = sorted([
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
], key=lambda x: x["name"].lower())

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Review Clip Finder</h1>", unsafe_allow_html=True)

# คำค้นหา
if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

new_keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed")

if new_keyword != st.session_state["keyword"]:
    st.session_state["keyword"] = new_keyword

# แปลคำค้นหา
translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            translated_text = translator.translate(st.session_state["keyword"], dest=plat["lang"]).text
        except Exception as e:
            translated_text = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated_text

# แสดงทุกแพลตฟอร์มใน 2 คอลัมน์แนวตั้ง
col1, col2 = st.columns(2)

for i, plat in enumerate(platforms):
    col = col1 if i % 2 == 0 else col2
    with col:
        with st.container():
            st.markdown(f"#### {plat['name']}")
            st.write("---")
            search_term = st.text_input(f"คำค้นหา ({plat['name']})", value=translated_terms.get(plat["name"], ""), key=f"term_{plat['name']}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("ค้นหา", key=f"search_{plat['name']}", use_container_width=True):
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;URL={plat["search_url"] + search_term}">', 
                        unsafe_allow_html=True
                    )
            with c2:
                if st.button("ไปหน้าโหลด", key=f"dl_{plat['name']}", use_container_width=True):
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;URL={plat["download"]}">', 
                        unsafe_allow_html=True
                    )
            st.markdown("---")
