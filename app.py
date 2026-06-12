import asyncio
import streamlit as st
from workflow import graph

st.set_page_config(page_title="Langraph Engine",page_icon="🧠",layout="wide")
st.title("LangGraph Enginee")
st.write("Enter Transcript here to build blueprint")
st.markdown("---")

transcript_input=st.text_area("Video Transcript",placeholder="Enter Words ...",height=250)

st.write("")

col1,col2,col3=st.columns()

with col2:
    submit_clicked=st.button("Run",type="primary",use_container_width=True)

if submit_clicked:
    if not transcript_input.strip():
        st.error("Please provide Transcript First !")
    else:
        with st.spinner("Processing ... Please wait ..."):
            initial_state={
                "transcript":transcript_input,
                "psychology_analysis":"",
                "script_blueprint":""
            }

            final_output=asyncio.run(graph.ainvoke(initial_state))
        st.markdown("===")
        st.success("Pipeline Finished PRocessing Successfully!")

        tab1,tab2=st.tabs(["Script Engineering BluePrint","Psychological Profile"])
        with tab1:
            st.markdown("Functional Structural Blueprint Script Formula")
            st.write(final_output.get("script_blueprint","No Blueprint generated."))
        with tab2:
            st.markdown("Audience Engagement Retention Psychology")
            st.write(final_output.get("pyschology_analysis","No psychological report generated"))