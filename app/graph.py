"""
Small helper to construct a graph of agents and outputs (for visualization or logging).
This is intentionally lightweight and has no external dependencies other than networkx (optional).
"""

try:
    import networkx as nx
except Exception:
    nx = None

def build_agent_graph():
    """
    Return a simple representation of agent nodes and edges.
    If networkx is available, returns a networkx.DiGraph; otherwise returns a dict.
    """
    nodes = ["Researcher", "Analyst", "Strategist", "Coordinator"]
    edges = [("Researcher", "Analyst"), ("Researcher", "Strategist"), ("Analyst", "Coordinator"), ("Strategist", "Coordinator")]

    if nx:
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G
    else:
        return {"nodes": nodes, "edges": edges}
