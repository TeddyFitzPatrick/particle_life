from consts import *
import sys
from random import randint, choice
from particle import Particle
from math import *
from button import Button

clock = pygame.time.Clock()
window = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)


def change_selection(selected_button: Button, other_buttons: list[Button]):
    for other_button in other_buttons:
        other_button.change_text_color(WHITE)
    selected_button.change_text_color(LIGHT_BLUE)


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
    # Simulation Variables
    R_MAX = 100
    R_MIN = 20
    R_ZENITH = (R_MIN + R_MAX) / 2
    friction = 0.05
    NUM_PARTICLES = 300
    particle_radius = 2

    # Generate particles and attraction/repulsion matrix
    particles = [get_random_particle() for _ in range(NUM_PARTICLES)]
    matrix = get_random_matrix()
    # User Input
    paused, show_radius = False, False
    mouse_clicks = []

    # status buttons
    fps_counter = Button(f'FPS: {int(clock.get_fps())}', 40, 40)
    particle_count = Button(f'Particles: {NUM_PARTICLES}', 40, 120)
    status_buttons = [fps_counter, particle_count]

    # friction buttons
    friction_title = Button('Friction Coefficient:', 40, 220, 42)
    friction_1 = Button('.01', 40, 280, 36)
    friction_5 = Button('.05', 140, 280, 36)
    friction_10 = Button('.1', 240, 280, 36)
    friction_buttons = [friction_title, friction_1, friction_5, friction_10]

    # particle size buttons
    psize_title = Button('Particle Size:', 40, 360, 42)
    psize_1 = Button('1PX', 40, 420, 36)
    psize_2 = Button('2PX', 140, 420, 36)
    psize_3 = Button('3PX', 240, 420, 36)
    psize_buttons = [psize_title, psize_1, psize_2, psize_3]

    # UI buttons
    UI = status_buttons + friction_buttons + psize_buttons

    # Select defaults
    change_selection(friction_5, friction_buttons)
    change_selection(psize_2, psize_buttons)

    while True:
        if not paused:
            # Data Manipulation (Model)
            # Apply the attractive/repulsive forces that dictate each particles velocity
            for particle in particles:
                particle.apply_force(particles, matrix, R_MIN, R_ZENITH, R_MAX)
            # Apply the calculated velocity to generate a new position for all particles
            for particle in particles:
                particle.update(friction)
        # Event handler (Controller)
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
                    particle_radius = 1
                elif event.key == pygame.K_2:
                    particle_radius = 2
                elif event.key == pygame.K_3:
                    particle_radius = 3
            # mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # friction buttons
                if friction_1.hovering():
                    friction = .01
                    change_selection(friction_1, friction_buttons)
                elif friction_5.hovering():
                    friction = 0.05
                    change_selection(friction_5, friction_buttons)
                elif friction_10.hovering():
                    friction = 0.1
                    change_selection(friction_10, friction_buttons)
                # particle size buttons
                elif psize_1.hovering():
                    particle_radius = 1
                    change_selection(psize_1, psize_buttons)
                elif psize_2.hovering():
                    particle_radius = 2
                    change_selection(psize_2, psize_buttons)
                elif psize_3.hovering():
                    particle_radius = 3
                    change_selection(psize_3, psize_buttons)

                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > int(WINDOW_SIZE[0] / 5):
                    mouse_clicks.append((mouse_pos, pygame.time.get_ticks()))
                    for particle in particles:
                        # r = sqrt(pow(mouse_pos[0] - particle.position[0], 2) + pow(mouse_pos[1] - particle.position[1], 2))
                        # if r > 100:
                        #     continue
                        delta_x, delta_y = mouse_pos[0] - particle.position[0], mouse_pos[1] - particle.position[1]
                        angle_radians = atan2(delta_y, delta_x)
                        particle.velocity[0] += 10 * cos(angle_radians)
                        particle.velocity[1] += 10 * sin(angle_radians)
            # Quit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        # Rendering
        window.fill(BLACK)
        # Buttons
        fps_counter.update_text(f'FPS: {int(clock.get_fps())}')
        for button in UI:
            button.blit(window)
        # DEBUG
        rc = pygame.rect.Rect(0, 0, int(WINDOW_SIZE[0] / 5), int(WINDOW_SIZE[1] / 2))
        pygame.draw.rect(window, WHITE, rc, 10)
        dc = pygame.rect.Rect(0, int(WINDOW_SIZE[1] / 2), int(WINDOW_SIZE[0] / 5), int(WINDOW_SIZE[1] / 2))
        pygame.draw.rect(window, RED, dc, 10)
        # Mouse
        for index, (pos, timestamp) in enumerate(mouse_clicks):
            if pos[0] > int(WINDOW_SIZE[0] / 5):
                pygame.draw.circle(window, WHITE, pos, 100, 1)
            if pygame.time.get_ticks() - timestamp > 100:
                mouse_clicks.pop(index)
        # Render particles
        for particle in particles:
            particle.render(window, particle_radius, show_radius, R_MIN, R_ZENITH, R_MAX)
        # Update screen
        pygame.display.flip()
        # Wait 17 ms
        clock.tick(60)


if __name__ == '__main__':
    main()
