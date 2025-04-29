import streamlit as st
from googletrans import Translator

translator = Translator()

# รายชื่อแพลตฟอร์มเรียงตามตัวอักษร
platforms = sorted([
    {"name": "Bilibili", "lang": "zh-cn", "search_url": "https://search.bilibili.com/all?keyword=", "download": "https://bravedown.com/th/bilibili-downloader"},
    {"name": "Dailymotion", "lang": "en", "search_url": "https://www.dailymotion.com/search/", "download": "https://www.savethevideo.com/dailymotion-downloader"},
    {"name": "Douyin", "lang": "zh-cn", "search_url": "https://www.douyin.com/search/", "download": "https://savetik.co/en/douyin-downloader"},
    {"name": "FaceBook", "lang": "en", "search_url": "https://www.facebook.com/search/top/?q=", "download": "https://fdown.net/"},
    {"name": "Instagram", "lang": "en", "search_url": "https://www.instagram.com/explore/tags/", "download": "https://snapins.ai/"},
    {"name": "Pinterest", "lang": "en", "search_url": "https://www.pinterest.com/search/pins/?q=", "download": "https://pinterestdownloader.com/"},
    {"name": "TikTok", "lang": "th", "search_url": "https://www.tiktok.com/search?q=", "download": "https://snaptik.app/en2"},
    {"name": "Weibo", "lang": "zh-cn", "search_url": "https://s.weibo.com/weibo?q=", "download": "https://bravedown.com/th/weibo-video-downloader"},
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"},
    {"name": "Xiaohongshu", "lang": "zh-cn", "search_url": "https://www.xiaohongshu.com/search_result/", "download": "https://bravedown.com/xiaohongshu-downloader"},
    {"name": "YouTube", "lang": "en", "search_url": "https://www.youtube.com/results?search_query=", "download": "https://en1.savefrom.net/1-youtube-video-downloader-8jH/"},
    {"name": "Youku", "lang": "zh-cn", "search_url": "https://so.youku.com/search_video/q_", "download": "https://www.locoloader.com/youku-video-downloader/"},
    {"name": "Zhihu", "lang": "zh-cn", "search_url": "https://www.zhihu.com/search?q=", "download": "https://www.videofk.com/zhihu-video-download"},
], key=lambda x: x["name"])

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Review Clip Finder</h1>", unsafe_allow_html=True)

# คำค้นหาหลัก
keyword = st.text_input("🔍 พิมพ์คำค้นหาหลัก แล้วกด Enter", value="", label_visibility="visible")

# แปลคำค้นหาตามภาษาของแต่ละแพลตฟอร์ม
translated_terms = {}
if keyword:
    for plat in platforms:
        try:
            translated = translator.translate(keyword, dest=plat["lang"]).text
        except Exception as e:
            translated = f"แปลไม่ได้: {e}"
        translated_terms[plat["name"]] = translated

# สร้าง 2 คอลัมน์แนวตั้ง
left_col, right_col = st.columns(2)

# วนลูปแสดงผลทีละแพลตฟอร์ม
for idx, plat in enumerate(platforms):
    container = left_col if idx % 2 == 0 else right_col
    with container:
        with st.container(border=True):
            st.markdown(f"### {plat['name']}")
            
            # คำค้นหาที่แปลแล้ว (หากมี)
            search_term = translated_terms.get(plat["name"], "") if keyword else ""
            search_input = st.text_input(
                f"คำค้นหา ({plat['name']})",
                value=search_term,
                key=f"input_{plat['name']}"
            )

            search_url = plat["search_url"] + search_input
            download_url = plat["download"]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <a href="{search_url}" target="_blank">
                        <button style="
                            width: 100%;
                            padding: 0.6em 1em;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 1em;
                        ">🔎 ค้นหา</button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <a href="{download_url}" target="_blank">
                        <button style="
                            width: 100%;
                            padding: 0.6em 1em;
                            background-color: #2196F3;
                            color: white;
                            border: none;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 1em;
                        ">⬇️ ไปหน้าโหลด</button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
