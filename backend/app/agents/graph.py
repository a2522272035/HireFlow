from __future__ import annotations

from langgraph.graph import StateGraph

from app.agents.state import AgentState


def create_agent_graph() -> StateGraph:
    """Create and compile the LangGraph agent workflow."""
    # TODO: Define agent workflow graph
    # TODO: Add nodes for each agent
    # TODO: Define edges and conditional routing

    workflow = StateGraph(AgentState)

    # Add nodes
    # workflow.add_node("resume_analyzer", resume_analyzer_node)
    # workflow.add_node("question_generator", question_generator_node)
    # workflow.add_node("credibility_assessor", credibility_assessor_node)

    # Add edges
    # workflow.add_edge("resume_analyzer", "question_generator")

    # Set entry point
    # workflow.set_entry_point("resume_analyzer")

    return workflow.compile()


# Global compiled graph instance
agent_graph = create_agent_graph()
