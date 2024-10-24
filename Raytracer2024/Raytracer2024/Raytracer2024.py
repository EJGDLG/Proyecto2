import pygame
from pygame.locals import *
from gl import RendererRT
from figure import *
from material import *
from lights import *
from texture import Texture

#width = 1500
#height = 500

width = 350
height = 220

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/aventure.bmp")

# Materiales
texture1  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/portal_1.bmp"))
texture2  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/nuves.bmp"))
texture3  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/rojo2.bmp"))
texture4  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/Texture2.bmp"), spec=128, ks=0.8, matType=REFLECTIVE)

Lock1  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/Lock1.bmp"))
Lock2  = Material(texture=Texture("C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/Recursos/Lock2.bmp"), spec=128, ks=0.8, matType=REFLECTIVE)

mirror = Material(diffuse=[0.9, 0.9, 0.6], spec=128, ks=0.2, matType=REFLECTIVE)
blueMirror = Material(diffuse=[0.1, 0.9, 0.9], spec=128, ks=0.2, matType=TRANSPARENT)
brick = Material(diffuse=[0.9, 0.9, 0.9], spec=128, ks=0.2 )
grass = Material(diffuse=[0.9, 0.2, 0.9], spec=128, ks=0.2, )
white_material = Material(diffuse=[1, 1, 1], spec=128, ks=0.2)
# Luces
rt.light.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.8))
rt.light.append(DirectionalLight(direction=[0.5, -0.5, -1], intensity=0.8, color=[1, 1, 1]))
rt.light.append(AmbientLight(intensity=0.1))

#rt.scene.append(Cylinder(position=[0, -2.5, -5], radius=0.5, height=2, material=mirror))

# Añadir elipsoides
rt.scene.append(Sphere(position=[0, 3, -25], radius=0.5, material=mirror))
rt.scene.append(Ellipsoid(position=[0, 7, -50], radii=[2, 1.5, 1.5], material=white_material))

# boca
#rt.scene.append(Ellipsoid(position=[0, 2, -120], radii=[2, 1.5, 1.5], material=grass))

# Añadir cilindros
rt.scene.append(Cylinder(position=[3, -5, -10], radius=0.5, height=1, material=texture1))
rt.scene.append(Cylinder(position=[2.5, -5, -10], radius=0.5, height=1.5, material=blueMirror))
rt.scene.append(Cylinder(position=[2, -5, -10], radius=0.5, height=0.5, material=texture1))
rt.scene.append(Cylinder(position=[1.5, -5, -10], radius=0.5, height=2, material=texture1))
rt.scene.append(Cylinder(position=[1, -5, -10], radius=0.5, height=1, material=texture1))
rt.scene.append(Cylinder(position=[0, -5, -10], radius=0.5, height=2.5, material=blueMirror))
rt.scene.append(Cylinder(position=[-1, -5, -10], radius=0.5, height=0.5, material=texture1))
rt.scene.append(Cylinder(position=[-1.5, -5, -10], radius=0.5, height=1, material=blueMirror))
rt.scene.append(Cylinder(position=[-2, -5, -10], radius=0.5, height=1, material=texture1))
rt.scene.append(Cylinder(position=[-2.5, -5, -10], radius=0.5, height=1.5, material=blueMirror))
rt.scene.append(Cylinder(position=[-3, -5, -10], radius=0.5, height=0.5, material=texture1))
# Añadir triángulos
rt.scene.append(Triangle(A=[-2.5, -1, -10], B=[2.5, -1, -10], C=[0, 2, -6], material=texture4))

#cajas y disco
rt.scene.append(Disk(position = [0,1.5,-5], normal = [0,1,0], radius = 1.5, material = texture1))
rt.scene.append(Disk(position = [0,1.5,-5], normal = [0,1,0], radius = 2.2, material = texture2))
#cajas
rt.scene.append(AABB(position = [1,3,-10],sizes = [0.5,0.5,1.2], material=texture3))
rt.scene.append(AABB(position = [-1,-3,-10],sizes = [0.5,0.5,1.2], material = texture3))

#esferas:
rt.scene.append(Sphere(position=[6, 2, -15], radius=1, material=Lock1))
rt.scene.append(Sphere(position=[5, 2, -14], radius=0.5, material=texture1))
rt.scene.append(Sphere(position=[-5, 2, -10], radius=0.5, material=mirror))

rt.scene.append(Sphere(position=[-3.5, -1.5, -12], radius=0.5, material=Lock2))
rt.scene.append(Sphere(position=[4, -1, -11], radius=0.5, material=texture2))
rt.scene.append(Sphere(position=[2, -2, -10], radius=0.5, material=blueMirror))

# Renderizar la escena
rt.glRender()

# Guardar la imagen como output.bmp
pygame.image.save(screen, "C:/Users/DeLeon/Documents/GitHub/Proyecto2/Raytracer2024/Raytracer2024/output3.bmp")

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
