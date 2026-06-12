import asyncio
from crawl4ai import AsyncWebCrawler
from youtube_transcript_api import YouTubeTranscriptApi 
import streamlit as st
import logging
import re
logging.basicConfig(
    level=logging.INFO
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_youtube_id(url:str)->str:
        
        pattern = r'(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=)([^#\&\?]+)'
        logging.info(f"Receieved Url :{url}")
        match=re.search(pattern,url)
        return match.group(1) if match else url

async def main(url_input:str,platform_choice:str):
    
    # for You tube
    if platform_choice=="You Tube":
        try:
            video_id=extract_youtube_id(url_input)
            logging.info(f"Extracted Video Id:{video_id}")
            api_instance=YouTubeTranscriptApi()
            raw_transcript = api_instance.fetch(video_id)
            raw_data=raw_transcript.to_raw_data()
            
            # Merge all separate text blocks into a clean paragraph
            clean_text_list = [item['text'] for item in raw_data]
            full_transcript = " ".join(clean_text_list)
            return "You Tube Transcript Extracted", full_transcript
        except Exception as e:
          print(f"Failed to extract transcript. Reason: {e}")
          print("Note: Make sure the video has public English subtitles/captions enabled.")
    else:
        logging.info(f"Initialize platform choice:{platform_choice}")



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