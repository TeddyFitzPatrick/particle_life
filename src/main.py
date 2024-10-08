from consts import *
import sys
from random import randint, choice
from particle import Particle
from math import *
from button import Button

clock = pygame.time.Clock()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Particle Life by Teddy')

# Simulation Variables
R_MIN = 20
R_MAX = 100
FRICTION = 0.05
NUM_PARTICLES = 300
PARTICLE_RADIUS = 4


def change_selection(selected_button: Button, other_buttons: list[Button]):
    for other_button in other_buttons:
        other_button.update_color(WHITE)
    selected_button.update_color(LIGHT_BLUE)


# Returns a randomly-positioned particle with a color from the P_COLOR selection
def get_random_particle() -> Particle:
    rand_pos = (randint(int(WINDOW_SIZE[0] / 5), WINDOW_SIZE[0]), randint(0, WINDOW_SIZE[1]))
    return Particle(choice(P_COLORS), rand_pos)


# Random mapping of different particle colors on to attraction/repulsion values.
def get_random_matrix() -> dict[tuple[float, float, float], dict]:
    matrix = {}
    for color in P_COLORS:
        matrix[color] = {}
        for other_color in P_COLORS:
            matrix[color][other_color] = choice([-1, -.8, -.6, -.4, -.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
    return matrix


def main():
    global R_MIN, R_MAX, FRICTION, NUM_PARTICLES, PARTICLE_RADIUS

    # Generate particles and attraction/repulsion matrix
    particles = [get_random_particle() for _ in range(NUM_PARTICLES)]
    matrix = get_random_matrix()
    # User Input
    paused, show_radius = False, False
    mouse_clicks = []

    # status buttons
    fps_counter = Button(f'FPS: {int(clock.get_fps())}', 40, 40, 48, GREEN)
    particle_count = Button(f'Particles:  {NUM_PARTICLES}', 40, 112, 42)
    status_buttons = [fps_counter, particle_count]

    # friction buttons
    friction_title = Button('Friction Coefficient:', 40, 220, 32)
    friction_1 = Button('.01', 40, 280, 36)
    friction_5 = Button('.05', 140, 280, 36)
    friction_10 = Button('.1', 240, 280, 36)
    friction_buttons = [friction_title, friction_1, friction_5, friction_10]

    # particle size buttons
    psize_title = Button('Particle Size:', 40, 360, 42)
    psize_small = Button('3PX', 40, 420, 36)
    psize_medium = Button('4PX', 140, 420, 36)
    psize_large = Button('5PX', 240, 420, 36)
    psize_buttons = [psize_title, psize_small, psize_medium, psize_large]

    # DEBUG, PAUSE, RESTART
    debug = Button('DEBUG', 40, 840, 48)
    pause = Button('PAUSE', 40, 920, 48)
    restart = Button('RESTART', 40, 1000, 48)
    controls = [debug, pause, restart]

    # All buttons
    UI = status_buttons + friction_buttons + psize_buttons + controls

    ## SLIDERS
    # R_MIN
    min_slider_box = pygame.rect.Rect(40, 560, 280, 40)
    min_slider_pos = [124, 580]
    min_sliding: bool = False

    # R_MAX
    max_slider_box = pygame.rect.Rect(40, 700, 280, 40)
    max_slider_pos = [60, 720]
    max_sliding: bool = False
    ##

    # Select defaults
    change_selection(friction_5, friction_buttons)
    change_selection(psize_medium, psize_buttons)

    while True:
        # Calculating particle interactions
        if not paused:
            # Apply the attractive/repulsive forces that dictate each particles velocity
            for particle in particles:
                particle.apply_force(particles, matrix, R_MIN, R_MAX)
            # Apply the calculated velocity to generate a new position for all particles
            for particle in particles:
                particle.update(FRICTION)

        # Slider logic for R_MIN and R_MAX
        if min_sliding:
            min_slider_pos[0] = pygame.mouse.get_pos()[0]
            # Bounding
            min_slider_pos[0] = 60 if min_slider_pos[0] < 60 else min_slider_pos[0]
            min_slider_pos[0] = 300 if min_slider_pos[0] > 300 else min_slider_pos[0]
            # Apply slider effects
            percent = (min_slider_pos[0] - 60) / 240
            # Change R_MIN and R_ZENITH values
            R_MIN = int(10 + percent * 40)
        if max_sliding:
            # SLIDER X from 60 -> 300
            max_slider_pos[0] = pygame.mouse.get_pos()[0]
            # Bounding
            max_slider_pos[0] = 60 if max_slider_pos[0] < 60 else max_slider_pos[0]
            max_slider_pos[0] = 300 if max_slider_pos[0] > 300 else max_slider_pos[0]
            # Apply slider effects
            percent = (max_slider_pos[0] - 60) / 240
            # Change R_MAX and R_ZENITH values
            R_MAX = int(80 + percent * 40)

        # Event handler
        for event in pygame.event.get():
            # keydown
            if event.type == pygame.KEYDOWN:
                # reload
                if event.key == pygame.K_r:
                    main()
                    return
                # Pause
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                # Show radius DEBUG
                elif event.key == pygame.K_e:
                    show_radius = not show_radius
                # Quit game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                # Particle size
                elif event.key == pygame.K_1:
                    PARTICLE_RADIUS = 1
                elif event.key == pygame.K_2:
                    PARTICLE_RADIUS = 2
                elif event.key == pygame.K_3:
                    PARTICLE_RADIUS = 3
            # mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # friction buttons
                if friction_1.hovering():
                    FRICTION = .01
                    change_selection(friction_1, friction_buttons)
                elif friction_5.hovering():
                    FRICTION = 0.05
                    change_selection(friction_5, friction_buttons)
                elif friction_10.hovering():
                    FRICTION = 0.1
                    change_selection(friction_10, friction_buttons)
                # particle size buttons
                elif psize_small.hovering():
                    PARTICLE_RADIUS = 3
                    change_selection(psize_small, psize_buttons)
                elif psize_medium.hovering():
                    PARTICLE_RADIUS = 4
                    change_selection(psize_medium, psize_buttons)
                elif psize_large.hovering():
                    PARTICLE_RADIUS = 5
                    change_selection(psize_large, psize_buttons)
                # Universal pull
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > int(WINDOW_SIZE[0] / 5):
                    mouse_clicks.append((mouse_pos, pygame.time.get_ticks()))
                    for particle in particles:
                        delta_x, delta_y = mouse_pos[0] - particle.position[0], mouse_pos[1] - particle.position[1]
                        angle_radians = atan2(delta_y, delta_x)
                        particle.velocity[0] += 10 * cos(angle_radians)
                        particle.velocity[1] += 10 * sin(angle_radians)
                # R_MIN & R_MAX Sliders
                if min_slider_box.collidepoint(pygame.mouse.get_pos()):
                    min_sliding = True
                elif max_slider_box.collidepoint(pygame.mouse.get_pos()):
                    max_sliding = True
                # DEBUG / PAUSE / RESTART
                if debug.hovering():
                    show_radius = not show_radius
                elif pause.hovering():
                    paused = not paused
                elif restart.hovering():
                    main()
                    return
            # Slider release
            if event.type == pygame.MOUSEBUTTONUP:
                min_sliding = False
                max_sliding = False
            # Quit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Rendering
        window.fill(BLACK)

        # Menu Options Bounding Box
        white_bounding_box = pygame.rect.Rect(0, 0, int(WINDOW_SIZE[0] / 5), int(WINDOW_SIZE[1]))
        pygame.draw.rect(window, WHITE, white_bounding_box, 10)

        # Buttons
        fps_counter.update_text(f'FPS: {int(clock.get_fps())}')
        for button in UI:
            button.blit(window)

        # R_MIN Slider
        pygame.draw.rect(window, WHITE, min_slider_box, 2)
        pygame.draw.circle(window, LIGHT_BLUE, min_slider_pos, 20, 5)
        rendered_text = def_font.render('Min Radius:  ' + str(R_MIN), 0, WHITE)
        window.blit(rendered_text, (40, 510))

        # R_MAX Slider
        pygame.draw.rect(window, WHITE, max_slider_box, 2)
        pygame.draw.circle(window, LIGHT_BLUE, max_slider_pos, 20, 5)
        rendered_text = def_font.render('Max Radius: ' + str(R_MAX), 0, WHITE)
        window.blit(rendered_text, (40, 650))

        # Mouse
        for index, (pos, timestamp) in enumerate(mouse_clicks):
            if pos[0] > int(WINDOW_SIZE[0] / 5):
                pygame.draw.circle(window, WHITE, pos, 100, 1)
            if pygame.time.get_ticks() - timestamp > 100:
                mouse_clicks.pop(index)

        # Render particles
        for particle in particles:
            particle.render(window, PARTICLE_RADIUS, show_radius, R_MIN, R_MAX)

        # Update screen
        pygame.display.flip()
        # Wait 17 ms
        clock.tick(60)


if __name__ == '__main__':
    main()
