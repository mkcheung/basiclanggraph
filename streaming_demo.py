from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display
import asyncio

# What is the purpose of streaming?
# Streaming is what allows the process of a workflow to show it’s results as it walks through it’s process incrementally. Rather than wait until it walks from beginning to end, it reports it’s results as it walks step by step.
# Useful for debugging OR observing partial results for a user to respond to


class HelloWorldState(TypedDict):
    message: str

def hello(state: HelloWorldState):
    print(f"Hello Node: {state['message']}")
    return {"message": "Hello "+state['message']}

def bye(state: HelloWorldState):
    print(f"Bye Node: {state['message']}")
    return {"message": "Bye "+state['message']}

graph = StateGraph(HelloWorldState)

graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable = graph.compile()

for chunk in runnable.stream({"message": "Mars"}, stream_mode="debug"):
    print(chunk)