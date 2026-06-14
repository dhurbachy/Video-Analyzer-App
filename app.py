import asyncio
import streamlit as st
from workflow import graph
from crawl import main as crawl_main
st.set_page_config(page_title="Langraph Engine",page_icon="🧠",layout="wide")
st.title("LangGraph Enginee")
st.write("Enter Transcript here to build blueprint")
st.markdown("---")
col_url, col_platform,col_btn=st.columns([5,2,2],vertical_alignment="bottom")
st.write("")

# transcript_input=st.text_area("Video Transcript",placeholder="Enter Words ...",height=250)

with col_url:
    url_input=st.text_input("",placeholder="https://...",label_visibility="collapsed")
with col_platform:
    platform_choice=st.selectbox('',["You Tube","Instagram","Facebook","Tiktok"])

with col_btn:
    submit_clicked=st.button("Genenrate",type="primary",use_container_width=True)
    



if submit_clicked:
    if not url_input.strip():
        st.error("Please provide video link First !")
    else:
        with st.spinner("Processing ... Please wait ..."):
            header,content=asyncio.run(crawl_main(url_input,platform_choice))
        
            # initial_state={
            #     "transcript":transcript_input,
            #     "psychology_analysis":"",
            #     "script_blueprint":""
            # }

            # final_output=asyncio.run(graph.ainvoke(initial_state))
        st.markdown("Extracted Resulted Data")
        st.success("Pipeline Finished PRocessing Successfully!")
        if "Error" in header:
            st.error(content)
        else:
            with st.spinner("Running AI Engineering Analysis..."):
                initial_state={
                "transcript":content,
                "psychology_analysis":"",
                "script_blueprint":""
                }
                final_output=asyncio.run(graph.ainvoke(initial_state))
            
            with st.container(border=True):
                st.markdown("### Transcript Extracted")
                st.text_area(
                    label="The Details of Transcript generated with timestamp.",
                    value=content,
                    height=150
                )
            st.write("")

            with st.container(border=True):
                st.markdown("### Final Psycholocial Decode")
                tab1, tab2,tab3=st.tabs(["Script Blueprint","Psychological Technique","Psychological Profile"])
                with tab1:
                    st.markdown(final_output.get("script_blueprint","No BluePrint Generated"))
                with tab2:
                    st.markdown(final_output.get("psychology_analysis","No techniocal brakdown generated."))
                with tab3:
                    st.markdown("### Platform Extraction Summary")
                    st.write(f"Psychology analysis and extraction completed successfully for: **{platform_choice}**")       
                 