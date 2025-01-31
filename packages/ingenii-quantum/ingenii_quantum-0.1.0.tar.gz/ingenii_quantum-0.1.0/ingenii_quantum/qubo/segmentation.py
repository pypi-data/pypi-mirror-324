import gurobipy as gp
from gurobipy import GRB
import time
import numpy as np

def decode_binary_string(x, height, width):
    """
    Decode a binary string into a binary segmentation mask.

    Args:
        x (list): Binary string representing the segmentation.
        height (int): Height of the image.
        width (int): Width of the image.

    Returns:
        numpy.ndarray: Segmentation mask.
    """
    mask = np.zeros([height, width])
    for index, segment in enumerate(x):
        mask[index // width, index % width] = segment
    return mask

def QUBO_formulation(G, alpha=10, height=32):
    ''' 
    Function that provides the QUBO formulation for quantum and simulated annealing. It provides the linear and quadratic constraints.

    Args:
        G (networkx.Graph): Weighted graph encoding the input image
        alpha (float): hyperparameter controlling the importance of the smoothness constraint.

    Returns:
        linear (dict): linear constraints of QUBO model
        quadratic (dict): quadratic constraints of QUBO model
        problem_formulation_time (float): Problem formulation time
    '''
    # Problem formulation
    node_dict = {list(G.nodes())[i]:i for i in range(len(G.nodes()))}
    linear = {i:0 for i in range(len(node_dict))}
    quadratic1 = {(node_dict[i],node_dict[j]):0 for (i,j) in G.edges()}
    quadratic2 = {(i,i):0 for i in range(len(node_dict))}
    quadratic = {**quadratic1, **quadratic2}
    start_time = time.time()
    for edge in G.edges():
        node1, node2 = edge[0], edge[1]
        w = G.get_edge_data(node1, node2)['weight']
        node1_idx, node2_idx = node1[0]*height + node1[1], node2[0]*height + node2[1]
        # Min-cut constraints w_{ij}*x_i(1- x_j)
        linear[node1_idx] += w 
        linear[node2_idx] += w 
        quadratic[(node1_idx, node2_idx)] += -2*w
        # Smootheness constraints  S = alpha*w_{ij}(q- delta(xi, xj)) = alpha*w_{ij}(1-(xi + xj - 1)^2) = alpha*w_{ij}(2xi + 2xj -2xixj -xi^2 - xj^2)
        linear[node1_idx] += alpha*2*w 
        linear[node2_idx] += alpha*2*w 
        quadratic[(node1_idx, node2_idx)] += -alpha*2*w
        quadratic[(node1_idx, node1_idx)] += -alpha*w
        quadratic[(node2_idx, node2_idx)] += -alpha*w
    problem_formulation_time = time.time() - start_time
    return linear, quadratic, problem_formulation_time




def gurobi_qubo_solver(G, alpha=10, height=32, width=32):
    ''' 
    Gurobi solver.

    Args
        G (networkx.Graph): Weighted graph encoding the input image
        alpha (float): hyperparameter controlling the importance of the smoothness constraint.
        
    Returns:
        segmentation_mask (np.array): Segmentation mask
        gurobi_qubo_value (float): QUBO value of segmentation mask
    '''
    # Problem formulation
    model = gp.Model()
    n = len(G.nodes())
    x = model.addVars(n, vtype=GRB.BINARY)
    obj_expr = 0 
    model.update()
    for edge in G.edges():
        node1, node2 = edge[0], edge[1]
        w = G.get_edge_data(node1, node2)['weight']
        node1_idx, node2_idx = node1[0]*height + node1[1], node2[0]*height + node2[1]
        obj_expr += w*(x[node1_idx] + x[node2_idx] - 2*x[node1_idx]*x[node2_idx]) + alpha*w*(1-(x[node1_idx] + x[node2_idx] - 1)**2)
    model.setObjective(obj_expr)
    model.setParam('OutputFlag', 0)

    model.optimize()
    model.update()
    if model.status == GRB.OPTIMAL:
        solution = [int(x[i].X) for i in range(n)]
        binary_string = ''.join(str(bit) for bit in solution)
        gurobi_qubo_solution, gurobi_qubo_value = binary_string, model.objVal

        segmentation_mask = decode_binary_string(gurobi_qubo_solution, height, width)
        return segmentation_mask, gurobi_qubo_value
    else:
        print('No solution found')
        return None, None