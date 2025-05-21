import pygame

def process_input(event, obj2d, obj3d):
    # Tangani keyboard & mouse events
    if event.type == pygame.KEYDOWN:
        if obj2d:
            if event.key == pygame.K_LEFT:
                obj2d.translate(-0.1, 0)
            elif event.key == pygame.K_RIGHT:
                obj2d.translate(0.1, 0)
            elif event.key == pygame.K_UP:
                obj2d.translate(0, 0.1)
            elif event.key == pygame.K_DOWN:
                obj2d.translate(0, -0.1)
            elif event.key == pygame.K_r:
                obj2d.rotate(5)
            elif event.key == pygame.K_s:
                if hasattr(obj2d, "scale_obj"):
                    obj2d.scale_obj(1.1)
                else:
                    obj2d.scale(1.1)

        if obj3d:
            if event.key == pygame.K_a:
                obj3d.translate(-0.1, 0, 0)
            elif event.key == pygame.K_d:
                obj3d.translate(0.1, 0, 0)
            elif event.key == pygame.K_w:
                obj3d.translate(0, 0.1, 0)
            elif event.key == pygame.K_x:
                obj3d.translate(0, -0.1, 0)
            elif event.key == pygame.K_q:
                obj3d.rotate(5)
            elif event.key == pygame.K_e:
                # Gunakan scale_obj jika ada, fallback ke scale
                if hasattr(obj3d, "scale_obj"):
                    obj3d.scale_obj(1.1)
                else:
                    obj3d.scale(1.1)
