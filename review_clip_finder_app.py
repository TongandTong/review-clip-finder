import streamlit as st
from googletrans import Translator

translator = Translator()

platforms = [
    {"name": "FaceBook", "lang": "en", "search_url": "https://www.facebook.com/search/top/?q=", "download": "https://fdown.net/"},
    {"name": "Douyin", "lang": "zh-cn", "search_url": "https://www.douyin.com/search/", "download": "https://savetik.co/en/douyin-downloader"},
    # เพิ่มแพลตฟอร์มอื่นๆ
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

# กดปุ่มเลือกแพลตฟอร์ม
selected_platform = None
for plat in platforms:
    if st.button(plat["name"], key=f"button_{plat['name']}"):
        selected_platform = plat

if selected_platform:
    st.markdown(f"### แพลตฟอร์มที่เลือก: {selected_platform['name']}")
    search_term = st.text_input(f"คำค้นหา ({selected_platform['name']})", value=translated_terms.get(selected_platform["name"], ""))

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("ค้นหา", key=f"search_{selected_platform['name']}"):
            search_url = selected_platform["search_url"] + search_term
            # ใช้ HTML เปิดลิงก์ในแท็บใหม่
            st.markdown(f'<a href="{search_url}" target="_blank">ไปที่หน้าค้นหา {selected_platform["name"]}</a>', unsafe_allow_html=True)
    with col2:
        if st.button("ไปหน้าโหลด", key=f"dl_{selected_platform['name']}"):
            # ใช้ HTML เปิดลิงก์ในแท็บใหม่
            st.markdown(f'<a href="{selected_platform["download"]}" target="_blank">ไปที่หน้าโหลด {selected_platform["name"]}</a>', unsafe_allow_html=True)
