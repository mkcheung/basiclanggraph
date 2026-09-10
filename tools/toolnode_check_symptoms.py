from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver 
from langgraph.graph import MessagesState, StateGraph, START, END

@tool
def check_symptoms(symptom: str):
    """Look up possible conditions associated with a given symptom."""
    conditions = {
        "fever": ["Flu", "COVID-19", "Common Cold"],
        "cough": ["Bronchitus", "Pneumonia", "Common Cold"],
        "headache": ["Migraine", "Tension Headache", "Sinus Infection"]
    }
    return conditions.get(symptom.lower(), ["No specific conditions found. Please consult a"])

@tool
def book_doctor_appointment(speciality: str, date: str, time: str):
    """Book a doctor appointment with the given speciality, date, and time."""
    available_specialites = ["General Physician", "Cardiologist", "Neurologist", "Pediatrician"] 
    if speciality in available_specialites:
        return f"Appointment booked with {speciality} on {date} at {time}."
    else:
        return f"Sorry, no available {speciality} at this time."   

tools = [check_symptoms, book_doctor_appointment]
model = ChatOpenAI().bind_tools(tools)
tool_node = ToolNode(tools)

def call_model(state: MessagesState): 
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": response}

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools":"tools", END:END})
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}

response = graph.invoke(
    {"messages": [HumanMessage(content="I have a fever. Can you tell me what this condition is?")]},
    config
)

conditions = response["messages"][-1].content
print(f"\n ** Symptom Diagnosis: {conditions}")

response = graph.invoke(
    {"messages": [HumanMessage(content=f"Book an appointment for these conditions {conditions} with a General Physician for tomorrow at 10 AM.")]},
    config
)

final_response = response["messages"][-1].content

print("\n **Doctor Appointment Confirmation:**")
print(final_response)
