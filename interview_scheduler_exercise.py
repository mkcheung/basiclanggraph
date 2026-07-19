from typing import TypedDict
from langgraph.graph import END, START, StateGraph

class JobApplication(TypedDict):
    applicant_name: str
    years_exp: int

def categorize_candidate(request: JobApplication):
    print(f"Received Interview Request: {request}")
    if request["years_exp"] >= 5:
        return "interview_now"
    return "interview_later"

def schedule_interview(application: JobApplication):
    print(f"Candidate {application['applicant_name']} is shortlisted for an interview.")
    return({"status":"interview scheduled"})

def assign_skills_test(application: JobApplication):
    print(f"Candidate {application['applicant_name']} has been assigned a skills test.")
    return({"status":"skills test assigned"})

# create the graph
graph = StateGraph(JobApplication)

graph.add_node("interview", schedule_interview)
graph.add_node("skills_test", assign_skills_test)

graph.add_conditional_edges(START, categorize_candidate, {"interview_now":"interview", "interview_later":"skills_test"})
graph.add_edge("interview", END)
graph.add_edge("skills_test", END)

runnable = graph.compile()

print(runnable.invoke({"applicant_name": "Alex Langley", "years_exp": 5}))
print(runnable.invoke({"applicant_name": "Jon Alex", "years_exp": 2}))