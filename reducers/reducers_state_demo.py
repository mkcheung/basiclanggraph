from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import END, START, StateGraph, MessagesState
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


def connect_to_sales(state: MessagesState):
    return {"messages": [AIMessage(content="Great! Let me connect you with our sales team!")]}

def sales_response(state: MessagesState):
    return {"messages": [AIMessage(content="We have the best offer for you")]}

graph = StateGraph(MessagesState)

graph.add_node("connect_to_sales", connect_to_sales)
graph.add_node("sales_response", sales_response)

graph.add_edge(START, "connect_to_sales")
graph.add_edge("connect_to_sales", "sales_response")
graph.add_edge("sales_response", END)

chatbot = graph.compile()
test_inputs = "I want to buy your product"

messages = chatbot.invoke({"messages": [HumanMessage(content=test_inputs)]})

for message in messages['messages']:
    print(f"**Bot:** {message.content}")
