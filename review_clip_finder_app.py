import streamlit as st
from google.cloud import translate_v2 as translate

# ตั้งค่า Google Cloud Translation API
translate_client = translate.Client()

def translate_text(text, target_language):
    """แปลข้อความโดยใช้ Google Cloud Translation API"""
    try:
        translation = translate_client.translate(text, target_language=target_language)
        return translation['translatedText']
    except Exception as e:
        return f"Error: {e}"

# รายชื่อแพลตฟอร์มและข้อมูลที่เกี่ยวข้อง
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
    {"name": "X", "lang": "en", "search_url": "https://www.x.com/search?q=", "download": "https://ssstwitter.com/th"},
    {"name": "Facebook", "lang": "en", "search_url": "https://www.facebook.com/search/top?q=", "download": "https://fdown.net/"},
]

# ตั้งค่าหน้าต่างของ Streamlit
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Review Clip Finder</h1>", unsafe_allow_html=True)

# เก็บค่า keyword ใน session state
if "keyword" not in st.session_state:
    st.session_state["keyword"] = ""

# ฟอร์มให้กรอกคำค้น
st.markdown("<div class='boxed-section'>", unsafe_allow_html=True)
st.markdown("### 🔍 คำค้น (ไทย)")

new_keyword = st.text_input("พิมพ์คำค้นหาแล้วกด Enter", value=st.session_state["keyword"], label_visibility="collapsed")

if new_keyword != st.session_state["keyword"]:
    st.session_state["keyword"] = new_keyword

st.markdown("</div>", unsafe_allow_html=True)

# เลือกภาษาสำหรับแปล
language = st.selectbox("เลือกภาษา", ["en", "th", "zh-cn", "es", "fr"])

# แปลคำค้นหา
translated_terms = {}
if st.session_state["keyword"]:
    for plat in platforms:
        try:
            # ใช้ Google Cloud Translation API เพื่อแปล
            translated_text = translate_text(st.session_state["keyword"], plat["lang"])
        except Exception as e:
            translated_text = f"ไม่สามารถแปลคำค้นหาได้: {e}"
        translated_terms[plat["name"]] = translated_text

# แสดงผลลัพธ์การค้นหา
columns = st.columns(2)
half = len(platforms) // 2

for col_idx, start in enumerate([0, half]):
    with columns[col_idx]:
        for i in range(start, start + half):
            if i >= len(platforms): break
            plat = platforms[i]
            with st.expander(plat["name"], expanded=False):
                search_term = st.text_input(f"คำค้นหา ({plat['name']})", value=translated_terms.get(plat["name"], ""), key=f"term_{plat['name']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("ค้นหา", key=f"search_{plat['name']}"):
                        search_url = plat["search_url"] + search_term
                        st.markdown(f"[ค้นหา {plat['name']}]({search_url})", unsafe_allow_html=True)
                with col2:
                    if st.button("ไปหน้าโหลด", key=f"dl_{plat['name']}"):
                        st.markdown(f"[ไปที่หน้าโหลด {plat['name']}]({plat['download']})", unsafe_allow_html=True)
