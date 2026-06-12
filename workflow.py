from state import AgentState
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


def analyze_psychology(state: AgentState):
    llm = ChatOpenAI(model="gpt-40-mini", api_key=" ")
    prompt = f"""
       Analyze the viral psychology of this script transcript. Identify:
        1. The core emotional trigger used (fear of missing out, curiosity, etc.).
        2. Retaining techniques used in the first 5 seconds to prevent users from scrolling.
        3. Pacing and audience engagement patterns.
        
        Transcript: {state['transcript']}
     """
    response=llm.invoke(prompt)
    return {"psychology_analysis":response.content}

def generate_blueprint(state:AgentState):
    llm=ChatOpenAI(model="gpt-40-mini", api_key=" ")
    prompt=f"""  
      Based on the following psychological profile, turn this video structure into an explicit copywriting blueprint formula.
      Provide a step-by-step structural template (e.g., Hook -> Problem -> Open Loop -> Secret -> CTA) so a writer can easily draft a completely new script.

     psychology Profile:{state['psychology_analysis']}
    """
    response=llm.invoke(prompt)
    return {"script_blueprint":response.content}

workflow=StateGraph(AgentState)

workflow.add_node("analyze_psychology",analyze_psychology)
workflow.add_node("generate_blueprint",generate_blueprint)

workflow.set_entry_point("analyze_psychology")
workflow.add_edge("analyze_psychology","generate_psychology")
workflow.add_edge("generate_blueprint",END)

graph=workflow.compile()