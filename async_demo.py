from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display
import asyncio

# What is the purpose of asynchronous invocation?
# It runs tasks in the background without blocking current options by waiting for the task’s completion
# Note: it’s not about running everything at once. It’s more of coming back to pick up where you left off at


class HelloWorldState(TypedDict):
    message: str

async def hello(state: HelloWorldState):
    print(f"Hello Node: {state['message']}")
    await asyncio.sleep(1)
    return {"message": "Hello "+state['message']}

async def bye(state: HelloWorldState):
    print(f"Bye Node: {state['message']}")
    await asyncio.sleep(1)
    return {"message": "Bye "+state['message']}

graph = StateGraph(HelloWorldState)

graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable = graph.compile()
async def main():
    output = await runnable.ainvoke({"message":"Mars"})
    print(output)

asyncio.run(main())
# display(runnable)
# output = runnable.invoke({"message": "Mars"})
# print(output)