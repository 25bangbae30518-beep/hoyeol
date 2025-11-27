import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="YouTube 검색 사이트", page_icon="📺")
st.title("📺 YouTube 검색 사이트")

# 🔒 Secrets 안전하게 불러오기
api_key = st.secrets.get("YOUTUBE_API_KEY", None)

if api_key is None:
    st.error(
        "❌ YOUTUBE_API_KEY가 설정되어 있지 않습니다.\n"
        "Streamlit Cloud → Settings → Secrets 에 아래처럼 입력하세요:\n\n"
        "YOUTUBE_API_KEY = \"YOUR_API_KEY\""
    )
    st.stop()

# YouTube API 클라이언트 생성
youtube = build("youtube", "v3", developerKey=api_key)

st.write("검색어를 입력하면 YouTube API를 사용해 영상을 불러옵니다!")

# 검색 입력
query = st.text_input("🔍 검색어를 입력하세요")

if st.button("검색하기"):
    if not query:
        st.warning("검색어를 입력하세요!")
    else:
        # YouTube API 호출
        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=10
        ).execute()

        st.markdown("---")
        st.subheader(f"🔎 검색 결과 : {query}")

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            title = snippet["title"]
            desc = snippet["description"]
            thumb = snippet["thumbnails"]["high"]["url"]

            st.image(thumb, width=320)
            st.write(f"### {title}")
            st.write(desc)
            st.write(f"[▶ YouTube에서 보기](https://www.youtube.com/watch?v={video_id})")
            st.markdown("---")
