import pygame
import sys
import math
from pygame.locals import *

def rotate_point(point, angle_x, angle_y, angle_z):
    """Rotate a point around the origin."""
    x, y, z = point

    # Rotation around X-axis
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotation around Y-axis
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z

    # Rotation around Z-axis
    new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
    new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = new_x, new_y

    return x, y, z

def project_point(point):
    """Project a 3D point onto a 2D screen."""
    x, y, z = point
    return x * WIDTH / (z + 4) + WIDTH / 2, y * HEIGHT / (z + 4) + HEIGHT / 2

def draw_cube(screen, angle_x, angle_y, angle_z):
    """Draw a rotating cube with three visible faces."""
    screen.fill(BLACK)

    rotated_vertices = [rotate_point(v, angle_x, angle_y, angle_z) for v in vertices]

    for face in visible_faces:
        # Calculate the normal vector for each face
        normal = [0, 0, 0]
        for v in face:
            normal[0] += rotated_vertices[v][0]
            normal[1] += rotated_vertices[v][1]
            normal[2] += rotated_vertices[v][2]
        normal = [n / len(face) for n in normal]

        # Calculate the intensity based on the dot product with each light source
        intensity = [max(sum(a * b for a, b in zip(normal, light)), 0) for light in light_sources]

        # Draw the face with the corresponding intensity
        color = (
            int(RED[0] * intensity[0]),
            int(GREEN[1] * intensity[1]),
            int(BLUE[2] * intensity[2])
        )

        projected_face = [project_point(rotated_vertices[v]) for v in face]
        pygame.draw.polygon(screen, color, projected_face)

    for edge in edges:
        start = project_point(rotated_vertices[edge[0]])
        end = project_point(rotated_vertices[edge[1]])
        pygame.draw.line(screen, WHITE, start, end, 1)

    pygame.display.flip()

def update_visible_faces(angle_x, angle_y, angle_z):
    """Update the visible faces based on the rotation angles."""
    global visible_faces

    # Faces visible from the front, side, and top
    front_face = [0, 1, 2, 3]
    side_face = [4, 5, 6, 7]
    top_face = [0, 1, 5, 4]

    # Determine the visible faces based on the rotation angles
    if -math.pi / 4 < angle_y % (2 * math.pi) < math.pi / 4:
        visible_faces = [front_face]
    elif math.pi / 4 < angle_y % (2 * math.pi) < 3 * math.pi / 4:
        visible_faces = [side_face]
    else:
        visible_faces = [top_face]

def main():
    """Main function for the rotating cube program."""
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0

    # Set up Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rotating Cube with Light Sources")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        update_visible_faces(angle_x, angle_y, angle_z)
        draw_cube(screen, angle_x, angle_y, angle_z)
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.03

        clock.tick(FPS)

if __name__ == "__main__":
    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Cube vertices
    vertices = [
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, 1],
        [-1, 1, 1],
        [1, 1, 1],
        [1, -1, 1]
    ]

    # Cube edges (connecting vertices)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    # Cube faces (connecting vertices)
    visible_faces = []  # Initially empty

    # Light sources
    light_sources = [
        (1, 0, 0),  # Red light
        (0, 1, 0),  # Green light
        (0, 0, 1)   # Blue light
    ]

    main()
