import streamlit as st
from deep_translator import GoogleTranslator
import json
import os
from datetime import datetime

# ------------------------ Configuration ------------------------
st.set_page_config(page_title="Review Clip Finder", layout="centered")

DATA_FILE = "saved_links.json"
PLATFORMS = ["YouTube", "TikTok", "Facebook", "Instagram", "Twitter"]

def load_saved_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_links(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ------------------------ UI Design ------------------------
st.title("🎬 Review Clip Finder")
st.markdown("### Find and Save Review Clips")

platform = st.selectbox("Platform", PLATFORMS)
user_input = st.text_input("Search Term (Thai or English)")

if user_input:
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(user_input)
    except Exception as e:
        translated = user_input
        st.warning("Translation failed, using original text.")

    editable_translation = st.text_input("English Translation", translated)

    search_query = f"{platform} {editable_translation} review"
    st.markdown(f"🔍 **Final Query:** `{search_query}`")

    if st.button("Search on Web"):
        st.markdown(f"[Click to Search](https://www.google.com/search?q={search_query.replace(' ', '+')})")

    if st.button("Save this Query"):
        data = load_saved_links()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[timestamp] = {
            "platform": platform,
            "original": user_input,
            "translated": editable_translation,
            "query": search_query
        }
        save_links(data)
        st.success("Saved successfully!")

# ------------------------ Link Management ------------------------
st.markdown("---")
st.subheader("📁 Saved Search Queries")

data = load_saved_links()
if not data:
    st.info("No saved queries yet.")
else:
    for key in sorted(data.keys(), reverse=True):
        entry = data[key]
        with st.expander(f"[{entry['platform']}] {entry['original']} → {entry['translated']}"):
            st.code(entry["query"])
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"🌐 Search ({key})", key=f"search_{key}"):
                    search_url = f"https://www.google.com/search?q={entry['query'].replace(' ', '+')}"
                    st.markdown(f"[Open Search]({search_url})", unsafe_allow_html=True)
            with col2:
                if st.button(f"🗑️ Delete ({key})", key=f"delete_{key}"):
                    del data[key]
                    save_links(data)
                    st.warning("Deleted. Please refresh the app.")
                    st.experimental_rerun()
