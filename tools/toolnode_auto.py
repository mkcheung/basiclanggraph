from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver 
from IPython.display import display

@tool 
def get_restaurant_recommendations(location:str):
    """Provides a list of top restaurant recomendations for a given location."""
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
    }
    return recommendations.get(location.lower(), ["No recommendations available for this location"])

@tool
def book_table(restaurant: str, time: str):
    """Books a restaurant for a specific time."""
    return f"Table booked at {restaurant} for {time}."

tools = [get_restaurant_recommendations, book_table]
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

graph = workflow.compile()

display(graph)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}

response = graph.invoke(
    {"messages": [HumanMessage(content="Can you recommend just one top restaurant in Munich? "
                                       "The response should contain just the restaurant name")]},
    config
)

recommended_restaurant = response["messages"][-1].content
print(recommended_restaurant)

response = graph.invoke(
    {"messages": [HumanMessage(content="Please book a table at this restaurant ")]},
    config
)

recommended_restaurant = response["messages"][-1].content
print(recommended_restaurant)


# display(graph)

