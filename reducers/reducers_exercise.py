from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import END, START, StateGraph, MessagesState
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage

class OrderState(TypedDict):
    message: Annotated[list[AnyMessage], add]
    order_id: Annotated[int,add]

def take_order(state:OrderState):
    return {"messages": [AIMessage(content="Processing your order?")]}

def confirm_order(state:OrderState):
    return {"messages": [AIMessage(content="Your order has been placed")], "order_id":1}

graph = StateGraph(OrderState)

graph.add_node("take_order", take_order)
graph.add_node("confirm_order", confirm_order)


graph.add_edge(START, "take_order")
graph.add_edge("take_order", "confirm_order")
graph.add_edge("confirm_order", END)

chatbot = graph.compile()
test_input = "I want to buy a burger"

messages = chatbot.invoke({"messages": [HumanMessage(content=test_input)]})

for message in messages['messages']:
    print(f"**Bot:** {message.content}")

print("Total Ordrs: ", messages['order_id'])