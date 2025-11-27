import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="YouTube 검색 사이트", page_icon="📺")

st.title("📺 YouTube 검색 사이트")
st.write("검색어를 입력하면 YouTube API를 사용해 유튜브 영상을 불러옵니다!")

# 🔒 Secrets 확인
if "YOUTUBE_API_KEY" not in st.secrets:
    st.error("❌ YOUTUBE_API_KEY가 secrets에 설정되어 있지 않습니다.\n\n"
             "Streamlit Cloud → Settings → Secrets 에 아래 내용을 추가하세요:\n\n"
             "```\nYOUTUBE_API_KEY = \"YOUR_KEY_HERE\"\n```")
    st.stop()

# 유튜브 API 키 로드
API_KEY = st.secrets["YOUTUBE_API_KEY"]

# 유튜브 클라이언트 생성
youtube = build("youtube", "v3", developerKey=API_KEY)

query = st.text_input("🔍 검색어를 입력하세요", "")

if st.button("검색하기"):
    if not query:
        st.warning("검색어를 입력하세요!")
    else:
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=10
        ).execute()

        st.markdown("---")
        st.subheader(f"🔎 검색 결과: {query}")

        for item in search_response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

            st.image(thumbnail, width=350)
            st.write(f"### {title}")
            st.write(description)
            st.write(f"[👉 YouTube에서 보기](https://www.youtube.com/watch?v={video_id})")
            st.markdown("---")
