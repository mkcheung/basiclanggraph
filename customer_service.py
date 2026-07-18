from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# How to use conditional routing/branching
# set up a method with the routing/branching conditions
# Set up the methods to be associated with the nodes that will act on the selected conditions
###### Note that the return values MUST be the node names that the conditions will react on.
# declare the graph
# add_node the nodes - be sure the node names match what you set up in the me
# add_conditional_edges the edge method
# add_edge to the other node methods
# compile the graph
# execute by invoking an object selecting one of the conditions


class SupportRequest(TypedDict):
    message: str
    priority: int #1 (high) #2 (medium) #3 (;pw)

def categorize_request(request: SupportRequest):
    print(f"Received request: {request}")
    if "urgent" in request['message'].lower() or request['priority'] == 1:
        # return "urgent" 
        return "high"  # use for path_map in add_conditional_edges
    # return "standard"
    return "low" # use for path_map in add_conditional_edges

def handle_urgent(request: SupportRequest):
    print(f"Routing to Urgent Support Team: {request}")
    return request

def handle_standard(request: SupportRequest):
    print(f"Routing to Standard Support Queue: {request}")
    return request

# create the state graph
graph = StateGraph(SupportRequest)

# next, create the graph - add the nodes
graph.add_node("urgent", handle_urgent)
graph.add_node("standard", handle_standard)

# graph.add_conditional_edges(START, categorize_request) # if we want to use node names, leave as is
graph.add_conditional_edges(START, categorize_request, {"high":"urgent", "low":"standard"})
graph.add_edge("urgent", END)
graph.add_edge("standard", END)

runnable = graph.compile()

print(runnable.invoke({"message": "My account was hacked! Urgent help needed.", "priority": 1}))
print(runnable.invoke({"message": "I need help with password reset.", "priority": 3}))