import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="YouTube 검색 사이트", page_icon="📺")
st.title("📺 YouTube 검색 사이트")

# 🔍 디버그: secrets에 뭐가 들어있는지 확인
st.write("### 🔧 Secrets Debug")
st.json(st.secrets)

# 🔒 유튜브 API 키 확인
api_key = st.secrets.get("YOUTUBE_API_KEY", None)

if api_key is None:
    st.error(
        "❌ `YOUTUBE_API_KEY`가 Streamlit Secrets에서 인식되지 않았습니다.\n\n"
        "Streamlit Cloud → Settings → Secrets에 반드시 아래처럼 입력하세요:\n\n"
        "```\nYOUTUBE_API_KEY = \"YOUR_API_KEY\"\n```"
    )
    st.stop()

# YouTube API 클라이언트 생성
youtube = build("youtube", "v3", developerKey=api_key)

query = st.text_input("🔍 검색어를 입력하세요", "")

if st.button("검색하기"):
    if not query:
        st.warning("검색어를 입력하세요!")
    else:
        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=10
        ).execute()

        st.write(f"### '{query}' 검색 결과")

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            title = snippet["title"]
            desc = snippet["description"]
            thumb = snippet["thumbnails"]["high"]["url"]

            st.image(thumb, width=300)
            st.write(f"**{title}**")
            st.write(desc)
            st.write(f"[▶ 영상 보기](https://www.youtube.com/watch?v={video_id})")
            st.markdown("---")
