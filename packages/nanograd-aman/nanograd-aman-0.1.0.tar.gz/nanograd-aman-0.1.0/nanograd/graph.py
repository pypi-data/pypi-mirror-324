from graphviz import Digraph
from .engine import Value

def trace(root):
    # Builds a set of all nodes and edges in the graph
    nodes, edges = set(), set()

    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)

    build(root)
    return nodes, edges

def draw_dot(root):
    # Create a Digraph object with left-to-right layout
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})

    # Trace the graph to get all nodes and edges
    nodes, edges = trace(root)

    for n in nodes:
        uid = str(id(n))
        # Create a rectangular ('record') node for each value in the graph
        dot.node(name=uid,
                 label="{ %s | data %.4f | grad %.4f }" % (n.label,n.data,n.grad),  # Ensure n.data is a float
                 shape='record')

        if n._op:  # If this value is a result of an operation
            # Create an operation node
            op_name = uid + str(n._op)  # Unique operation node name
            dot.node(name=op_name, label=n._op)
            dot.edge(op_name, uid)  # Connect the op node to the value node

    for n1, n2 in edges:
        # Connect n1 to the operation node of n2
        dot.edge(str(id(n1)), str(id(n2)) + (n2._op or ""))

    # Return the dot graph
    return dot

def save_graph(root, filename="graph"):
    dot = draw_dot(root)
    dot.render(filename,format="png")  # Saves the graph and optionally opens it

def show_graph(root):
    from IPython.display import display, SVG
    dot = draw_dot(root)
    display(SVG(dot.pipe(format='svg')))

