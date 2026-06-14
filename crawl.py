import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from youtube_transcript_api import YouTubeTranscriptApi 
import streamlit as st
import logging
import re
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_youtube_id(url:str)->str:
        
        pattern = r'(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=)([^#\&\?]+)'
        logging.info(f"Receieved Url :{url}")
        match=re.search(pattern,url)
        return match.group(1) if match else url

async def main(url_input:str,platform_choice:str):
    platform_clean=platform_choice.lower().replace(" ","")
    # for You tube
    if platform_clean=="youtube":
        try:
            video_id=extract_youtube_id(url_input)
            logging.info(f"Extracted Video Id:{video_id}")
            api_instance=YouTubeTranscriptApi()
            # raw_transcript = api_instance.fetch(video_id)
            transcript_list = api_instance.list(video_id)
            raw_transcript = transcript_list.find_generated_transcript(transcript_list._generated_transcripts.keys())
            # raw_data=raw_transcript.to_raw_data()
            raw_data=raw_transcript.fetch()
            
            # Merge all separate text blocks into a clean paragraph
            clean_text_list = [item.text for item in raw_data]
            full_transcript = " ".join(clean_text_list)
            return "You Tube Transcript Extracted", full_transcript
        except Exception as e:
            logging.error(f"Failed to extract transcript. Reason: {e}")
            # FIXED: Always return two values on failure to prevent NoneType crash
            return "Error", f"Failed to extract transcript: {e}\nNote: Make sure the video has public subtitles/captions enabled."
    else:
        logging.info(f"Initialize platform choice:{platform_choice}")
        try:
            # configure advanced anti-blocking header & human like fingerprint
            browser_config=BrowserConfig(
                headless=True,
                enable_stealth=True,
                user_agent_mode="random",
                text_mode=True
            )
            # configure live request instruction
            run_config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                page_timeout=60000
            )

            async with AsyncWebCrawler as crawler:
                result=await crawler.arun(url=url_input,config=run_config)
                if result.success:
                   if result.markdown:
                       return f"{platform_choice} Extracted Layout Data",result.markdown
                   else:
                       return f"{platform_choice} Clean text output",result.cleaned_html
                else:
                    return "Error", f"Crawler restricted on {platform_choice}. Reason: {result.error_message}"
        except Exception as e:
            return "Error", f"An unexpected system exception occurred: {e}"




# st.set_page_config(page_title="Video Analyzer App", page_icon="🚀", layout="wide",initial_sidebar_state="expanded") # expanded, collapsed,auto
# st.title("Video Analayzer App")
# st.write("Extract clean Data")

# col1,col2,col3=st.columns([5,2,2],vertical_alignment="bottom")
# with col1:
#     url_input=st.text_input("Enter Social Media Reel and Video Url", placeholder="https://...")
# with col2:
#     platform_choice=st.selectbox("Select Target Platform",["You Tube","Instagram","Facebook","TikTok"])
# with col3:
#   submit_clicked=st.button("Generate",type="primary")

# if submit_clicked:
#     if not url_input.strip():
#         st.error("Please Provide video link here")
#     else:
#         with st.spinner("Processing Request ... Please Wait ..."):
#             header,content=asyncio.run(main(url_input,platform_choice))
#         st.subheader(header)
#         if "Error" in header:
#             st.error(header)
#         else:
            st.text_area("Extracted Resulted Data:",value=content,height=400)
            st.success("Extraction Finished Successfylly!")