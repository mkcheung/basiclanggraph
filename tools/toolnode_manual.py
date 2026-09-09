from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool 
def get_restaurant_recommendations(location:str):
    """Provides a list of top restaurant recomendations for a given location."""
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
    }
    return recommendations.get(location.lower(), ["No recommendations available for this location"])

tools = [get_restaurant_recommendations]
tool_node = ToolNode(tools)

message_with_tool_call = AIMessage(content="", tool_calls=[{'name': 'get_restaurant_recommendations', 'args':{'location':'Munich'}, 'id':'call_INMvRXjl4IOPMlX3UnNihZYk', 'type':'tool_call'}])

result = tool_node.invoke(messages)

print(result)
# llm = ChatOpenAI()


# llm_with_tools = llm.bind_tools(tools)

# messages = [
#     HumanMessage("Recommend some restaurants in Munich")
# ]

# llm_output = llm_with_tools.invoke(messages)
# print(llm_output)