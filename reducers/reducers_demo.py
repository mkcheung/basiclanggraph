from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


class ChatBotState(TypedDict):
    messages: Annotated[list[AnyMessage], add]
    discount: Annotated[int,add]

def connect_to_sales(state: ChatBotState):
    return {"messages": [AIMessage(content="Great! Let me connect you with our sales team!")], "discount":10}

def sales_response(state: ChatBotState):
    return {"messages": [AIMessage(content="We have the best offer for you")], "discount":20}

graph = StateGraph(ChatBotState)

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

print("Final Discount: ", messages['discount'], '%')