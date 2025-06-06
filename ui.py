import pygame
import time
from tracking import save_performance, save_action
from solver import solve

# Constants for the grid and neural network diagram
GRID_SIZE = 9
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def draw_nn_diagram(
    screen, center_x, center_y,
    activations=None,
    input_vals=None, output_val=None,
    input_highlight=None, output_highlight=False,
    hidden_highlight=None
):
    num_inputs = 5
    num_hidden_layers = 2  # or whatever your model uses
    nodes_per_hidden = 10  # match your model's hidden layer size
    num_outputs = 4  # e.g., Easy, Medium, Hard, Expert

    layer_gap = 110
    node_gap = 60

    # Calculate layer x positions
    layers_x = [center_x - (num_hidden_layers//2 + 1)*layer_gap]
    for i in range(num_hidden_layers):
        layers_x.append(layers_x[-1] + layer_gap)
    layers_x.append(layers_x[-1] + layer_gap)

    def get_layer_y(num_nodes):
        total_height = (num_nodes-1)*node_gap
        return [center_y - total_height//2 + i*node_gap for i in range(num_nodes)]

    input_nodes = [(layers_x[0], y) for y in get_layer_y(num_inputs)]
    hidden_nodes = []
    for l in range(num_hidden_layers):
        hidden_nodes.append([(layers_x[l+1], y) for y in get_layer_y(nodes_per_hidden)])
    output_nodes = [(layers_x[-1], y) for y in get_layer_y(num_outputs)]

    all_layers = [input_nodes] + hidden_nodes + [output_nodes]

    # Draw connections (optional: only if you want to show them)
    for l in range(len(all_layers)-1):
        for n1 in all_layers[l]:
            for n2 in all_layers[l+1]:
                pygame.draw.line(screen, (180,180,180), n1, n2, 2)

    # Draw nodes with activation coloring
    for l, layer_nodes in enumerate(all_layers):
        for n, (x, y) in enumerate(layer_nodes):
            value = 0
            if activations and l < len(activations) and n < len(activations[l]):
                value = activations[l][n]
                # Normalize value to [0, 1] for color mapping
                norm = max(0, min(1, (value + 1) / 2))  # For tanh, adjust as needed
                color = (
                    int(255 * (1 - norm)),  # Red decreases with activation
                    int(255 * norm),        # Green increases with activation
                    0
                )
            else:
                color = (0, 0, 255)
            pygame.draw.circle(screen, color, (x, y), 22)

def run_ui(puzzle, difficulty, suggested, nn_activations=None):
    pygame.init()
    screen = pygame.display.set_mode((1400, 600))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont(None, 40)
    bold_font = pygame.font.SysFont(None, 40, bold=True)  # Add bold font
    clock = pygame.time.Clock()
    running = True
    selected = None
    errors = 0
    start_ticks = pygame.time.get_ticks()
    last_move_time = time.time()

    grid = [row[:] for row in puzzle]
    solution = [row[:] for row in puzzle]
    solve(solution)
    wrong_cells = set()

    # Animation state
    input_flash = None
    output_flash = False
    hidden_flash = [False] * 5
    flash_timer = 0

    while running:
        screen.fill((255,255,255))
        # Draw grid
        for i in range(10):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, (0,0,0), (0, i*60), (540, i*60), width)
            pygame.draw.line(screen, (0,0,0), (i*60, 0), (i*60, 540), width)
        # Draw numbers
        for i in range(9):
            for j in range(9):
                if grid[i][j]:
                    if puzzle[i][j] != 0:
                        num_font = bold_font  # Original numbers in bold
                    else:
                        num_font = font      # User-filled numbers regular
                    color = (0,0,0)
                    img = num_font.render(str(grid[i][j]), True, color)
                    screen.blit(img, (j*60+20, i*60+15))
        # Draw selection
        if selected:
            pygame.draw.rect(screen, (0,255,0), (selected[1]*60, selected[0]*60, 60, 60), 3)
        # Draw info
        elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        info = font.render(f"Diff: {difficulty}  Time: {elapsed}s  Errors: {errors}", True, (0,0,255))
        screen.blit(info, (10, 550))

        # Prepare NN input/output values
        input_vals = [elapsed, errors, difficulty]
        output_val = suggested  # Use the passed-in argument

        # Animate NN diagram
        if flash_timer and pygame.time.get_ticks() - flash_timer < 300:
            draw_nn_diagram(
                screen, 975, 300,  # was 950, 300
                activations=nn_activations,
                input_vals=input_vals,
                output_val=output_val,
                input_highlight=input_flash,
                output_highlight=output_flash,
                hidden_highlight=hidden_flash
            )
        else:
            draw_nn_diagram(
                screen, 975, 300,
                input_vals=input_vals,
                output_val=output_val
            )
            input_flash = None
            output_flash = False
            hidden_flash = [False] * 5
            flash_timer = 0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_performance(difficulty, elapsed, errors)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < 540 and y < 540:
                    selected = (y//60, x//60)
            elif event.type == pygame.KEYDOWN and selected:
                if event.key in range(pygame.K_1, pygame.K_9+1):
                    val = event.key - pygame.K_0
                    i, j = selected
                    if puzzle[i][j] == 0:
                        now = time.time()
                        time_delta = now - last_move_time
                        last_move_time = now
                        mistake = int(val != solution[i][j])
                        save_action(i, j, val, time_delta, mistake)
                        if val == solution[i][j]:
                            grid[i][j] = val
                            if (i, j) in wrong_cells:
                                wrong_cells.remove((i, j))
                            # Animate: highlight time input, all hidden, and output
                            input_flash = 0  # 0 = time
                            output_flash = True
                            hidden_flash = [True] * 5
                            flash_timer = pygame.time.get_ticks()
                        else:
                            grid[i][j] = val
                            wrong_cells.add((i, j))
                            errors += 1
                            # Animate: highlight errors input, all hidden, and output
                            input_flash = 1  # 1 = errors
                            output_flash = True
                            hidden_flash = [True] * 5
                            flash_timer = pygame.time.get_ticks()
                        # Check for completion
                        if all(grid[x][y] == solution[x][y] for x in range(9) for y in range(9)):
                            save_performance(difficulty, elapsed, errors)
                            running = False
                elif event.key == pygame.K_DELETE:
                    i, j = selected
                    if puzzle[i][j] == 0:
                        grid[i][j] = 0
                        if (i, j) in wrong_cells:
                            wrong_cells.remove((i, j))
                elif event.key == pygame.K_ESCAPE:
                    selected = None
        clock.tick(30)
    pygame.quit()
