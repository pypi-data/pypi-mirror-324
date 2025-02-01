import matplotlib.pyplot as plt
from typing import List, Union, Optional


def plot_tsp_route_matplot(route: List[Union[int, str]], 
                   node_names: List[str], 
                   node_coordinates: dict, 
                   start_node: Optional[Union[str, int]]=None, 
                   cycle: bool=True):
    """
    Plots the TSP route with arrows indicating the travel direction, highlights the starting node,
    and optionally connects the last node back to the starting node to form a cycle.
    """
    # Extract x and y coordinates for each node in the route
    x_coords = [node_coordinates[node_names[i]][0] for i in route]
    y_coords = [node_coordinates[node_names[i]][1] for i in route]
    
    # If cycle is True, complete the loop bye returning to the starting point
    if cycle:
        x_coords.append(x_coords[0])
        y_coords.append(y_coords[0])
    
    plt.figure(figsize=(8, 6))
    
    # Plot each segment with an arrow and label the order
    for i in range(len(route) - (0 if cycle else 1)):
        plt.plot(
            [x_coords[i], x_coords[i + 1]], 
            [y_coords[i], y_coords[i + 1]], 
            marker='o', 
            color='b', 
            markersize=8
        )
        plt.annotate(
            f'{i+1}', 
            (x_coords[i], y_coords[i]), 
            textcoords="offset points", 
            xytext=(5, 5), 
            ha='center', 
            fontsize=10, 
            color='red'
        )
    
    # Add arrows to show direction between nodes
    for i in range(len(route) - (0 if cycle else 1)):
        plt.arrow(
            x_coords[i], y_coords[i], 
            x_coords[i + 1] - x_coords[i], y_coords[i + 1] - y_coords[i],
            head_width=0.05, length_includes_head=True, color='blue'
        )
    
    # Highlight the starting node with a different color if specified
    if start_node is not None:
        start_x, start_y = node_coordinates[node_names[start_node]]
        plt.plot(start_x, start_y, marker='o', color='green', markersize=10, label="Start Node")
        plt.annotate(
            'Start', 
            (start_x, start_y), 
            textcoords="offset points", 
            xytext=(5, 5), 
            ha='center', 
            fontsize=12, 
            color='green'
        )
    
    # Label each node with its name
    for i in range(len(route)):
        label = node_names[route[i]]
        plt.text(node_coordinates[label][0], node_coordinates[label][1], label, fontsize=12, ha='right')
    
    plt.title("TSP Route")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid()
    plt.show()
    plt.close()