import pygame
import numpy as np

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
scalar = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")
clock = pygame.time.Clock()

# Original array of cube vertices
unit_cube_vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [-1, 1, -1],
    [1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1]
])

cube_vertices = unit_cube_vertices*scalar

#Function for calculating intersection
def intersection(plane, viewing_point, point):
    x_v = point[0] - viewing_point[0]
    y_v = point[1] - viewing_point[1]
    z_v = point[2] - viewing_point[2]
    #Vars for better readability
    x_0 = viewing_point[0]
    y_0 = viewing_point[1]
    z_0 = viewing_point[2]
    #Parameter t is sovled via z coord
    t = (plane - z_0) / z_v
    #Now solve for x and y where it is intersected
    x = x_0 + (x_v * t)
    y = y_0 + (y_v * t)
    z = plane
    return [x, y, z]


#Function to project matrix onto 2D plane (Orthogonal projection)
def project_cube(vertices):
    projection_matrix = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    projected_vertices = np.dot(vertices, projection_matrix)
    return projected_vertices

#Function to rotate cube vertices around all three axes

def rotate_cube(vertices, angles):
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(angles[0]), -np.sin(angles[0])],
        [0, np.sin(angles[0]), np.cos(angles[0])]
    ])
    rotation_matrix_y = np.array([
        [np.cos(angles[1]), 0, np.sin(angles[1])],
        [0, 1, 0],
        [-np.sin(angles[1]), 0, np.cos(angles[1])]
    ])
    rotation_matrix_z = np.array([
        [np.cos(angles[2]), -np.sin(angles[2]), 0],
        [np.sin(angles[2]), np.cos(angles[2]), 0],
        [0, 0, 1]
    ])
    rotated_vertices = np.dot(vertices, rotation_matrix_x.T)
    rotated_vertices = np.dot(rotated_vertices, rotation_matrix_y.T)
    rotated_vertices = np.dot(rotated_vertices, rotation_matrix_z.T)
    return rotated_vertices

# Function to draw lines between cube vertices
def draw_cube_lines(vertices):
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),
        (4, 5), (5, 7), (7, 6), (6, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    sides = [
        (0,1,2,3),
        (4,5,6,7),
        (0,1,4,5),
        (2,3,6,7),
        (0,4,2,6),
        (1,5,3,7)
    ]

    #Empty np.array to be changed to new intersected vertices
    intersected_vertices = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])

    #VARS
    z_plane = 0
    viewing_point = (0, 0, 250)

    for i in range(len(vertices)):
        intersected_vertices[i] = intersection(z_plane, viewing_point, vertices[i])
    projected_vertices = project_cube(intersected_vertices)
    #projected_vertices = project_cube(vertices)


    for side in sides:
        top_left = (int(projected_vertices[side[0]][0] + WIDTH // 2), int(projected_vertices[side[0]][1] + HEIGHT // 2))
        top_right = (int(projected_vertices[side[1]][0] + WIDTH // 2), int(projected_vertices[side[1]][1] + HEIGHT // 2))
        bottom_right = (int(projected_vertices[side[2]][0] + WIDTH // 2), int(projected_vertices[side[2]][1] + HEIGHT // 2))
        bottom_left = (int(projected_vertices[side[3]][0] + WIDTH // 2), int(projected_vertices[side[3]][1] + HEIGHT // 2))
    for edge in edges:
        start = (int(projected_vertices[edge[0]][0] + WIDTH // 2), int(projected_vertices[edge[0]][1] + HEIGHT // 2))
        end = (int(projected_vertices[edge[1]][0] + WIDTH // 2), int(projected_vertices[edge[1]][1] + HEIGHT // 2))
        pygame.draw.line(screen, (0, 0, 0), start, end, 1) #Zero line thickness

# Main game loop
angles = [0, 0, 0]
rotate_speed = 1
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of the arrow keys
    keys = pygame.key.get_pressed()
    
    # Update rotation angles based on arrow key input
    angles[0] += rotate_speed # Y-axis rotation
    angles[1] += rotate_speed # X-axis rotation

    # Limit the rotation angles to avoid excessive spinning
    # Rotate the cube vertices around all three axes
    rotated_cube_vertices = rotate_cube(cube_vertices, np.radians(angles))

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw lines between cube vertices
    draw_cube_lines(rotated_cube_vertices)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
