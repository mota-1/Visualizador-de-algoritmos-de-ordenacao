import pygame
import random
import sys
import geradores
import numpy as np
import pygame.sndarray


# --- Configuration ---
WIDTH, HEIGHT = 800, 600
ARRAY_SIZE = 20
current_size = [ARRAY_SIZE]
# BAR_WIDTH = WIDTH // current_size[0]
FPS = 40
current_fps = [FPS]
MAX_BAR_HEIGHT = HEIGHT - 50
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 40
BUTTON_MARGIN = 10
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

# --- Button Class ---
class Button:
    def __init__(self, x, y, text, callback):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text
        self.callback = callback

    def draw(self, screen, font, mouse_pos):
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

def draw_array(screen, arr, highlight_indices):
    bar_width = WIDTH / len(arr)

    for i, val in enumerate(arr):
        x = int(i * bar_width)
        y = HEIGHT - val
        width = max(1, int(bar_width))  # Ensure width is at least 1 pixel
        rect = pygame.Rect(x, y, width, val)
        pygame.draw.rect(screen, (100, 200, 255), rect)

        if i in highlight_indices:
            pygame.draw.rect(screen, (255, 255, 50), rect)
            wider_rect = pygame.Rect(x - 1, y, width + 2, val)
            pygame.draw.rect(screen, (255, 0, 0), wider_rect)


    pygame.display.flip()

    valid_indices = [i for i in highlight_indices if i is not None and 0 <= i < len(arr)]
    if valid_indices:
        first_idx = valid_indices[0]
        val = arr[first_idx]
        freq = 200 + int((val / MAX_BAR_HEIGHT) * 800)
        tone = generate_tone(freq)
        tone.play()



def generate_tone(frequency, duration_ms=None, volume=0.5):
    if duration_ms is None:
        duration_ms = 1000 / current_fps[0] + 10

    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    waveform = (volume * waveform * 32767).astype(np.int16)

    # Convert to 2D stereo by duplicating mono waveform
    stereo_waveform = np.column_stack((waveform, waveform))  # (n_samples, 2)
    return pygame.sndarray.make_sound(stereo_waveform)



# --- Visualize Sorting ---
def visualize_sorting(algorithm_name):
    
    array = [int(i * (MAX_BAR_HEIGHT / current_size[0])) for i in range(1, current_size[0] + 1)]
    random.shuffle(array)
    sorting_generator = getattr(geradores, algorithm_name)(array)

    pygame.display.set_caption(f"Visualizar {algorithm_name.replace("_visu", "").replace("_", " ").title()}")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    back_button = Button(WIDTH - BUTTON_WIDTH - 10, 10, "Voltar", lambda: main_menu())

    try:
        arr, i1, i2 = next(sorting_generator)
    except StopIteration:
        arr, i1, i2 = [], None, None

    running = True
    prev_arr = None  # Track previous frame

    while running:
        clock.tick(current_fps[0])
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            back_button.handle_event(event)

        screen.fill(BG_COLOR)
        back_button.draw(screen, font, mouse_pos)
        draw_array(screen, arr, {i1, i2} if i1 is not None else set())
        

        # --- 🔊 Gravity Sort Sound Logic ---
        if i1 is None and i2 is None and prev_arr is not None and len(arr) == len(prev_arr):
            for i in range(len(arr)):
                if arr[i] > prev_arr[i]:  # Bar has grown
                    freq = 200 + int((arr[i] / MAX_BAR_HEIGHT) * 800)
                    tone = generate_tone(freq, volume=0.3)
                    tone.play()

        prev_arr = arr.copy()

        pygame.display.flip()

        try:
            arr, i1, i2 = next(sorting_generator)
        except StopIteration:
            i1 = i2 = None



# --- Main Menu ---
def main_menu():
    # pygame.mixer.pre_init(44100, -16, 1, 512) # <- this doesn't do anything

    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualizador de algoritmo de ordenação")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()
    

    algorithms = [
        "radix_LSD_sort_visu", "counting_sort_visu", "pigeonhole_sort_visu", "merge_sort_visu",
        "insertion_sort_visu", "bubble_sort_visu", "gravity_sort_visu",
        "sleep_sort_visu", "bogo_sort_visu", 
    ]

    buttons = []
    start_y = 60
    for idx, name in enumerate(algorithms):
        x = (WIDTH - BUTTON_WIDTH) // 2
        y = start_y + idx * (BUTTON_HEIGHT + BUTTON_MARGIN)
        buttons.append(Button(x, y, name.replace("_visu", "").replace("_", " ").title(), lambda n=name: visualize_sorting(n)))

    # FPS Adjustment Buttons
    def increase_fps():
        current_fps[0] = min(120, current_fps[0] + 10)

    def decrease_fps():
        current_fps[0] = max(10, current_fps[0] - 10)

    fps_buttons = [
        Button(WIDTH - BUTTON_WIDTH - 10, HEIGHT - 100, "FPS +", increase_fps),
        Button(WIDTH - BUTTON_WIDTH - 10, HEIGHT - 50, "FPS -", decrease_fps),
    ]

    def increase_arr_size():
        current_size[0] = min(400, current_size[0]+10)
    
    def decrease_arr_size():
        current_size[0] = max(5, current_size[0]-10)
    
    size_buttons = [
        Button(20, HEIGHT - 100, "Tamanho +", increase_arr_size),
        Button(20, HEIGHT - 50, "Tamanho -", decrease_arr_size),
    ]

    running = True
    while running:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)
            for btn in fps_buttons:
                btn.handle_event(event)
            for btn in size_buttons:
                btn.handle_event(event)



        for button in buttons:
            button.draw(screen, font, mouse_pos)

        for btn in fps_buttons:
            btn.draw(screen, font, mouse_pos)

        # Display FPS
        fps_text = font.render(f"FPS: {current_fps[0]}", True, TEXT_COLOR)
        screen.blit(fps_text, (WIDTH - BUTTON_WIDTH - 10, HEIGHT - 140))

        for btn in size_buttons:
            btn.draw(screen, font, mouse_pos)

        # Display FPS
        size_text = font.render(f"Size: {current_size[0]}", True, TEXT_COLOR)
        screen.blit(size_text, (20, HEIGHT - 140))



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# --- Run ---
if __name__ == "__main__":
    main_menu()
