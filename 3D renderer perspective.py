import pygame
from dataclasses import dataclass
from cmath import tan, sin, cos

@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class Object:
    def __init__(self):
        self.position = Point(0, 0, 400)
        self.rotation = Point(0, 0, 0)
        self.points = []

        self.points.append(Point(-200, -200, -200))
        self.points.append(Point(-200, 200, -200))
        self.points.append(Point(200, 200, -200))
        self.points.append(Point(200, -200, -200))
        self.points.append(Point(-200, -200, 200))
        self.points.append(Point(-200, 200, 200))
        self.points.append(Point(200, 200, 200))
        self.points.append(Point(200, -200, 200))

    def Draw(self):        
        self.drawPoints = [Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point()]

        # Rotate
        for i in range(8):
             self.drawPoints[i] = Rotate(self.points[i], self.rotation)

        # Translate
        for i in range(8):
             self.drawPoints[i] = Translate(self.drawPoints[i], self.position)
             self.drawPoints[i] = Translate(self.drawPoints[i], camera_pos)

        # Apply perspective
        for i in range(8):
             self.drawPoints[i] = ApplyPerspective(self.drawPoints[i])

        # Center screen
        for i in range(8):
             self.drawPoints[i] = CenterScreen(self.drawPoints[i])

        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[0].x, self.drawPoints[0].y), (self.drawPoints[1].x, self.drawPoints[1].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[1].x, self.drawPoints[1].y), (self.drawPoints[2].x, self.drawPoints[2].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[2].x, self.drawPoints[2].y), (self.drawPoints[3].x, self.drawPoints[3].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[3].x, self.drawPoints[3].y), (self.drawPoints[0].x, self.drawPoints[0].y), 5)

        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[4].x, self.drawPoints[4].y), (self.drawPoints[5].x, self.drawPoints[5].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[5].x, self.drawPoints[5].y), (self.drawPoints[6].x, self.drawPoints[6].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[6].x, self.drawPoints[6].y), (self.drawPoints[7].x, self.drawPoints[7].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[7].x, self.drawPoints[7].y), (self.drawPoints[4].x, self.drawPoints[4].y), 5)

        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[0].x, self.drawPoints[0].y), (self.drawPoints[4].x, self.drawPoints[4].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[1].x, self.drawPoints[1].y), (self.drawPoints[5].x, self.drawPoints[5].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[2].x, self.drawPoints[2].y), (self.drawPoints[6].x, self.drawPoints[6].y), 5)
        pygame.draw.aaline(screen, (0, 0, 0), (self.drawPoints[3].x, self.drawPoints[3].y), (self.drawPoints[7].x, self.drawPoints[7].y), 5)


def Translate(original, translation):
    toReturn = Point()
    toReturn.x = (original.x + translation.x).real
    toReturn.y = (original.y + translation.y).real
    toReturn.z = (original.z + translation.z).real
    return toReturn


def Rotate(original, rotation):
    toReturn = Point()
    toReturn.x = (original.x * (cos(rotation.z) * cos(rotation.y)) + original.y * (cos(rotation.z) * sin(rotation.y) * sin(rotation.x) - sin(rotation.z) * cos(rotation.x)) + original.z * (cos(rotation.z) * sin(rotation.y) * cos(rotation.x) + sin(rotation.z) * sin(rotation.x))).real
    toReturn.y = (original.x * (sin(rotation.z) * cos(rotation.y)) + original.y * (sin(rotation.z) * sin(rotation.y) * sin(rotation.x) + cos(rotation.z) * cos(rotation.x)) + original.z * (sin(rotation.z) * sin(rotation.y) * cos(rotation.x) - cos(rotation.z) * sin(rotation.x))).real
    toReturn.z = (original.x * (- sin(rotation.y)) + original.y * (cos(rotation.y) * sin(rotation.x)) + original.z * (cos(rotation.y) * cos(rotation.x))).real
    return toReturn


def ApplyPerspective(original):
    toReturn = Point()
    toReturn.x = (original.x * Z0 / (Z0 + original.z)).real
    toReturn.y = (original.y * Z0 / (Z0 + original.z)).real
    toReturn.z = (original.z).real
    return toReturn


def CenterScreen(original):
    toReturn = Point()
    toReturn.x = (original.x + res_x / 2).real
    toReturn.y = (original.y + res_y / 2).real
    toReturn.z = (original.z).real
    return toReturn


# General variable inits
res_x = 1200
res_y = 800
camera_pos = Point(0, 0, 0)
camera_rot = Point(0, 0, 0)
FOV = 45
Z0 = (res_x / 2.0) / tan((FOV / 2.0) * 3.14159265 / 180.0)  # The distance from the "eye" to the camera plane
objects = []
speed = 10

# Pygame inits
pyramid = Object()
objects.append(pyramid)
clock = pygame.time.Clock()
background_colour = (255, 255, 255)
screen = pygame.display.set_mode((res_x, res_y))  
pygame.display.set_caption('3D Renderer')
running = True


while running:
    screen.fill(background_colour)      # Erase Screen

    for event in pygame.event.get():      
        if event.type == pygame.QUIT:
            running = False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_pos.x += speed
    if keys[pygame.K_RIGHT]:
        camera_pos.x -= speed
    if keys[pygame.K_UP]:
        camera_pos.z -= speed
    if keys[pygame.K_DOWN]:
        camera_pos.z += speed
    if keys[pygame.K_SPACE]:
        camera_pos.y += speed
    if keys[pygame.K_LCTRL]:
        camera_pos.y -= speed

    for object in objects:
        object.Draw()
        object.rotation.x += 0.01
        object.rotation.y += 0.01
        object.rotation.z += 0.01

    pygame.display.flip()   # Update the screen
    clock.tick(60)          # Set FPS to 60
