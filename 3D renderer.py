import pygame
from dataclasses import dataclass
from cmath import tan, sin, cos, pi

@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

@dataclass
class Triangle:
    a: Point
    b: Point
    c: Point

@dataclass
class Mesh:
    polygons: list

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def TranslatePoint(original, input):
    output = Point()
    output.x = original.x + input.x
    output.y = original.y + input.y
    output.z = original.z + input.z
    return output

def MultipyMatrixVector3x3(input, matrix):
    output = Point()

    output.x = input.x * matrix[0][0] + input.y * matrix[1][0] + input.z * matrix[2][0]
    output.y = input.x * matrix[0][1] + input.y * matrix[1][1] + input.z * matrix[2][1]
    output.z = input.x * matrix[0][2] + input.y * matrix[1][2] + input.z * matrix[2][2]
    return output

def MultipyMatrixVector(input, matrix):
    output = Point()

    output.x = input.x * matrix[0][0] + input.y * matrix[1][0] + input.z * matrix[2][0] +  matrix[3][0]
    output.y = input.x * matrix[0][1] + input.y * matrix[1][1] + input.z * matrix[2][1] +  matrix[3][1]
    output.z = input.x * matrix[0][2] + input.y * matrix[1][2] + input.z * matrix[2][2] +  matrix[3][2]
    w        = input.x * matrix[0][3] + input.y * matrix[1][3] + input.z * matrix[2][3] +  matrix[3][3]

    if w != 0:
        output.x /= w
        output.y /= w
        output.z /= w
    return output

def DrawTriangle(input):
    pygame.draw.aaline(screen, (0, 0, 0), (input[0].x, input[0].y), (input[1].x, input[1].y))
    pygame.draw.aaline(screen, (0, 0, 0), (input[1].x, input[1].y), (input[2].x, input[2].y))
    pygame.draw.aaline(screen, (0, 0, 0), (input[2].x, input[2].y), (input[0].x, input[0].y))


### Pygame variables ###
(res_x, res_y) = (1920, 1080)
screen = pygame.display.set_mode((res_x, res_y),  pygame.FULLSCREEN)
background_colour = (255,255,255)
running = True
clock = pygame.time.Clock()

### Projection Variables ###
fov = 90.0
z_far = 1000.0
z_near = 0.1
a = float(res_y/res_x)                                          # aspect_ratio
fov_rad = float(1.0 / tan(fov * 0.5 / 180 * pi).real)           # Degree to Radians and vice versa fuckery, how does it work?
q = z_far/(z_far-z_near)
projection_matrix =[[a*fov_rad, 0, 0, 0],
                    [0, fov_rad, 0, 0],
                    [0, 0, q, 1],
                    [0, 0, (-z_far * z_near) / (z_far - z_near), 0]]

Cube = Mesh([
            
            # South
            Triangle( Point(0, 0, 0), Point(0, 1, 0), Point(1, 1, 0) ),
            Triangle( Point(0, 0, 0), Point(1, 1, 0), Point(1, 0, 0) ),

            # East
            Triangle( Point(1, 0, 0), Point(1, 1, 0), Point(1, 1, 1) ),
            Triangle( Point(1, 0, 0), Point(1, 1, 1), Point(1, 0, 1) ),

            # North
            Triangle( Point(1, 0, 1), Point(1, 1, 1), Point(0, 1, 1) ),
            Triangle( Point(1, 0, 1), Point(0, 1, 1), Point(0, 0, 1) ),

            # West
            Triangle( Point(0, 0, 1), Point(0, 1, 1), Point(0, 1, 0) ),
            Triangle( Point(0, 0, 1), Point(0, 1, 0), Point(0, 0, 0) ),

            # Top
            Triangle( Point(0, 1, 0), Point(0, 1, 1), Point(1, 1, 1) ),
            Triangle( Point(0, 1, 0), Point(1, 1, 1), Point(1, 1, 0) ),

            # Bottom
            Triangle( Point(1, 0, 1), Point(0, 0, 1), Point(0, 0, 0) ),
            Triangle( Point(1, 0, 1), Point(0, 0, 0), Point(1, 0, 0) )
])

### Misc Variables ###
theta = 0


### Main Loop ###
while running:
        for event in pygame.event.get():        # Handling events
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   # Escaping with ESC
                running = False
            
        pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
        theta += clock.get_time()*0.001
        x_rotation_matrix =[[1, 0, 0],                                                          # These are the rotation matrices, I'm a bit confused about them,
                            [0, cos(theta*0.5).real, -sin(theta*0.5).real],                     # but they are a good blackbox.
                            [0, sin(theta*0.5).real, cos(theta*0.5).real]]
                                                                                                # Also the x matrix is halved so the gimbal lock doesn't become a problem.
        z_rotation_matrix =[[cos(theta).real, -sin(theta).real, 0],                             # These matrices should be placed in a rotation function.
                            [sin(theta).real, cos(theta).real, 0],
                            [0, 0, 1]]

        screen.fill(background_colour)          # Drawing starts here

        for triangle in Cube.polygons:
            rotated_triangle    = [Point, Point, Point]
            translated_triangle = [Point, Point, Point]
            projected_triangle  = [Point, Point, Point]

            # Rotating
            rotated_triangle[0] = MultipyMatrixVector3x3(triangle.a, z_rotation_matrix)
            rotated_triangle[1] = MultipyMatrixVector3x3(triangle.b, z_rotation_matrix)
            rotated_triangle[2] = MultipyMatrixVector3x3(triangle.c, z_rotation_matrix)

            rotated_triangle[0] = MultipyMatrixVector3x3(rotated_triangle[0], x_rotation_matrix)
            rotated_triangle[1] = MultipyMatrixVector3x3(rotated_triangle[1], x_rotation_matrix)
            rotated_triangle[2] = MultipyMatrixVector3x3(rotated_triangle[2], x_rotation_matrix)

            # Translating, I had so many problems with this, I think I burnt through a few braincells.
            translated_triangle[0] = TranslatePoint(rotated_triangle[0], Point(0, 0, 3))
            translated_triangle[1] = TranslatePoint(rotated_triangle[1], Point(0, 0, 3))
            translated_triangle[2] = TranslatePoint(rotated_triangle[2], Point(0, 0, 3))

            # Projecting
            projected_triangle[0] = MultipyMatrixVector(translated_triangle[0], projection_matrix)
            projected_triangle[1] = MultipyMatrixVector(translated_triangle[1], projection_matrix)
            projected_triangle[2] = MultipyMatrixVector(translated_triangle[2], projection_matrix)

            # Scaling
            projected_triangle[0].x += 1.0; projected_triangle[0].y += 1.0          # Get these normalized values to be between 1 and 2
            projected_triangle[1].x += 1.0; projected_triangle[1].y += 1.0
            projected_triangle[2].x += 1.0; projected_triangle[2].y += 1.0

            projected_triangle[0].x *= 0.5*float(res_x); projected_triangle[0].y *= 0.5*float(res_y)    # Scale them to the resolution
            projected_triangle[1].x *= 0.5*float(res_x); projected_triangle[1].y *= 0.5*float(res_y)
            projected_triangle[2].x *= 0.5*float(res_x); projected_triangle[2].y *= 0.5*float(res_y)

            DrawTriangle(projected_triangle)


        pygame.display.flip()                   # Drawing stops here
        clock.tick()