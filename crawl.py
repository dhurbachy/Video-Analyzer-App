import asyncio
from crawl4ai import AsyncWebCrawler
from youtube_transcript_api import YouTubeTranscriptApi 
import streamlit as st
async def main():
    # 1. Target YouTube Video ID
    # (This ID is the letters/numbers at the end of a YouTube URL)
    video_id = "dQw4w9WgXcQ" 
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"[CRAWL] Starting analyzer engine for video link...")

    # 2. Use Crawl4AI to fetch basic site metadata
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=video_url)
        if result.success:
            print("✓ Web crawler connected to YouTube platform successfully.")
        else:
            print("⚠ Direct web connection blocked, switching to internal transcript pipeline.")

    # 3. Use the Transcript API to extract the spoken words
    print(f"[TRANSCRIPT] Fetching audio subtitles for ID: {video_id}...")
    try:
        # Pull the raw transcript data
        api_instance=YouTubeTranscriptApi()
        raw_transcript = api_instance.fetch(video_id)
        raw_data=raw_transcript.to_raw_data()
        
        # Merge all separate text blocks into a clean paragraph
        clean_text_list = [item['text'] for item in raw_data]
        full_transcript = " ".join(clean_text_list)

        # 4. Display the final output
        print("\n🎉 SUCCESS! Full Video Transcript Extracted:")
        print("-" * 50)
        print(full_transcript[:1000]) # Prints the first 1000 characters
        print("\n... [Truncated for preview] ...")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Failed to extract transcript. Reason: {e}")
        print("Note: Make sure the video has public English subtitles/captions enabled.")

# if __name__ == "__main__":
#     asyncio.run(main())

st.set_page_config(page_title="Video Analyzer App", page_icon="🚀", layout="wide",initial_sidebar_state="expanded") # expanded, collapsed,auto
st.title("Video Analayzer App")
st.write("Extract clean Data")

url_input=st.text_input("Enter Social Media Reel and Video Url", placeholder="https://...")
platform_choice=st.selectbox("Select Target Platform",["You Tube","Instagram","Facebook","TikTok"])

if st.button("Generate",type="primary"):
    if not url_input.strip():
        st.error("Please Provide video link here")
    else:
        with st.spinner("Processing Request ... Please Wait ..."):
            header,content=asyncio.run(main(url_input,platform_choice))
        st.subheader(header)
        if "Error" in header:
            st.error(header)
        else:
            st.text_area("Extracted Resulted Data:",value=content,height=400)
            st.success("Extraction Finished Successfylly!")