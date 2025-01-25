import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def draw_chair():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define chair dimensions
    seat_height = 0.5
    seat_width = 1
    seat_depth = 1
    leg_height = 1
    backrest_height = 0.5
    backrest_thickness = 0.1
    leg_thickness = 0.1

    # Create seat
    seat = np.array([[0, 0, seat_height],
                     [seat_width, 0, seat_height],
                     [seat_width, seat_depth, seat_height],
                     [0, seat_depth, seat_height],
                     [0, 0, seat_height]])

    # Create legs
    leg1 = np.array([[0, 0, 0],
                     [0, 0, leg_height],
                     [leg_thickness, 0, leg_height],
                     [leg_thickness, 0, 0],
                     [0, 0, 0]])
    
    leg2 = leg1 + np.array([[seat_width, 0, 0], [seat_width, 0, 0], [seat_width, 0, 0], [seat_width, 0, 0]])
    leg3 = leg1 + np.array([[0, seat_depth, 0], [0, seat_depth, 0], [0, seat_depth, 0], [0, seat_depth, 0]])
    leg4 = leg2 + np.array([[0, seat_depth, 0], [0, seat_depth, 0], [0, seat_depth, 0], [0, seat_depth, 0]])

    # Create backrest
    backrest = np.array([[0, seat_depth, seat_height],
                         [seat_width, seat_depth, seat_height],
                         [seat_width, seat_depth + backrest_thickness, seat_height + backrest_height],
                         [0, seat_depth + backrest_thickness, seat_height + backrest_height],
                         [0, seat_depth, seat_height]])

    # Plot seat
    ax.add_collection3d(plt.Polygon(seat, color='brown', alpha=0.5))
    
    # Plot legs
    ax.add_collection3d(plt.Polygon(leg1, color='saddlebrown', alpha=0.5))
    ax.add_collection3d(plt.Polygon(leg2, color='saddlebrown', alpha=0.5))
    ax.add_collection3d(plt.Polygon(leg3, color='saddlebrown', alpha=0.5))
    ax.add_collection3d(plt.Polygon(leg4, color='saddlebrown', alpha=0.5))
    
    # Plot backrest
    ax.add_collection3d(plt.Polygon(backrest, color='brown', alpha=0.5))
    
    # Set limits and labels
    ax.set_xlim([0, seat_width + 0.5])
    ax.set_ylim([-0.5, seat_depth + 0.5])
    ax.set_zlim([0, leg_height + seat_height])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    plt.show()

draw_chair()