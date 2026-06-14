import asyncio
import streamlit as st
from workflow import graph
import memory as mem
from crawl import main as crawl_main
st.set_page_config(page_title="Langraph Engine",page_icon="🧠",layout="wide")
st.title("LangGraph Enginee")
st.sidebar.title("History Analaysis")
history_files=mem.get_history_list()
st.write("Enter Transcript here to build blueprint")
st.markdown("---")
selected_history_data=None
if history_files:
    history_options={}
    for f in history_files:
        try:
            file_data=mem.load_history_file(f)
            display_name=f"[{file_data['platform']}]-{file_data['timestamp']}"
            history_options[display_name]=file_data

        except Exception:
            continue
    selected_option=st.sidebar.selectbox("Load Previous run:",['-- Select History--']+list(history_options.keys()))
    if selected_option!="-Select History-":
        selected_history_data=history_options[selected_option]
        if st.sidebar.button("Clear",type="secondary"):
            st.rerun()
else:
    st.sidebar.info("No saved data yet.")
st.write("")
col_url, col_platform,col_btn=st.columns([5,2,2],vertical_alignment="bottom")
st.write("")
default_url=selected_history_data['url'] if selected_history_data else ""
platforms=["You Tube","Instagram","Facebook","Tiktok"]
default_platform_idx=platforms.index(selected_history_data['platform']) if selected_history_data and selected_history_data['platform'] in platforms else 0
# transcript_input=st.text_area("Video Transcript",placeholder="Enter Words ...",height=250)

content=""
blueprint_out=""
pyschology_out=""
show_results=False

with col_url:
    url_input=st.text_input("",value=default_url, placeholder="https://...",label_visibility="collapsed")
with col_platform:
    platform_choice=st.selectbox('',platforms,index=default_platform_idx,label_visibility="collapsed")

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
                blueprint_out=final_output.get("script_blueprint","")
                pyschology_out=final_output.get("Psychology_analysis","")
                show_results=True
                mem.save_to_memory(url_input,platform_choice,content,blueprint_out,pyschology_out)
                st.success("Extracted and Saved Successfully")
                st.rerun()

elif selected_history_data:
    content=selected_history_data["transcript"]
    blueprint_out=selected_history_data["blueprint"]
    psychology_out=selected_history_data["psychology"]
    show_results=True    

if show_results:
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
                    st.markdown(blueprint_out if blueprint_out else "No Blueprint Generated")
                with tab2:
                    # st.markdown(final_output.get("psychology_analysis","No techniocal brakdown generated."))
                    st.markdown(psychology_out if psychology_out else "No technical breakdown generated.")
                with tab3:
                    st.markdown("### Platform Extraction Summary")
                    st.write(f"Psychology analysis and extraction completed successfully for: **{platform_choice}**")   

                 