import pygame
import sys
import random

DIFFICULTIES = {
    "Beginner": {"grid_size": 9, "mines": 10, "cell_size": 40},
    "Intermediate": {"grid_size": 16, "mines": 40, "cell_size": 30},
    "Expert": {"grid_size": 30, "mines": 99, "cell_size": 20},  
    "Custom": {"grid_size": 10, "mines": 15, "cell_size": 40}
}
current_difficulty = "Beginner"
GRID_SIZE = DIFFICULTIES[current_difficulty]["grid_size"]
CELL_SIZE = DIFFICULTIES[current_difficulty]["cell_size"]
MINES_COUNT = DIFFICULTIES[current_difficulty]["mines"]
UI_HEIGHT = 80
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + UI_HEIGHT
FPS = 30

def set_difficulty(difficulty_name):
    global current_difficulty, GRID_SIZE, CELL_SIZE, MINES_COUNT, WIDTH, HEIGHT
    if difficulty_name in DIFFICULTIES:
        current_difficulty = difficulty_name
        config = DIFFICULTIES[difficulty_name]
        GRID_SIZE = config["grid_size"]
        CELL_SIZE = config["cell_size"]
        MINES_COUNT = config["mines"]
    
        if difficulty_name == "Expert":
            WIDTH = 30 * CELL_SIZE
            HEIGHT = 16 * CELL_SIZE + UI_HEIGHT
            GRID_SIZE = 16  
        else:
            WIDTH = GRID_SIZE * CELL_SIZE
            HEIGHT = GRID_SIZE * CELL_SIZE + UI_HEIGHT

COLORS = {
    "hidden": (44, 47, 51),      
    "revealed": (60, 63, 68),    
    "flag": (255, 85, 85),       
    "mine": (200, 60, 60),       
    "text": (220, 220, 220),     
    "grid": (70, 73, 80),        
    "ui_bg": (30, 32, 36),      
    "ui_border": (80, 80, 100),  
    "button_bg": (50, 54, 60),   
    "button_active": (80, 120, 200), 
    "button_text": (230, 230, 230),
    "button_selected": (100, 180, 255),
    "numbers": {  
        1: (80, 180, 255),      
        2: (80, 220, 120),      
        3: (255, 120, 120),     
        4: (180, 120, 255),     
        5: (255, 180, 80),     
        6: (80, 255, 220),      
        7: (255, 255, 120),    
        8: (200, 200, 200)      
    }
}

# --- HELPER FUNCTIONS (must be above main) ---
def show_custom_dialog(screen):
    dialog_w, dialog_h = 340, 260
    dialog_x = (screen.get_width() - dialog_w) // 2
    dialog_y = (screen.get_height() - dialog_h) // 2
    font = pygame.font.SysFont("Segoe UI", 22)
    font_label = pygame.font.SysFont("Segoe UI", 18)
    font_button = pygame.font.SysFont("Segoe UI", 20, bold=True)
    input_font = pygame.font.SysFont("Segoe UI", 22)

    grid_size = "10"
    mine_count = "15"
    active_input = "grid"
    error_msg = ""

    input_box_grid = pygame.Rect(dialog_x+40, dialog_y+70, 60, 36)
    input_box_mines = pygame.Rect(dialog_x+220, dialog_y+70, 60, 36)
    button_rect = pygame.Rect(dialog_x+60, dialog_y+170, 100, 40)
    cancel_rect = pygame.Rect(dialog_x+180, dialog_y+170, 100, 40)

    done = False
    result = None
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active_input == "grid":
                    if event.key == pygame.K_BACKSPACE:
                        grid_size = grid_size[:-1]
                    elif event.unicode.isdigit() and len(grid_size) < 2:
                        grid_size += event.unicode
                elif active_input == "mines":
                    if event.key == pygame.K_BACKSPACE:
                        mine_count = mine_count[:-1]
                    elif event.unicode.isdigit() and len(mine_count) < 3:
                        mine_count += event.unicode
                if event.key == pygame.K_TAB:
                    active_input = "mines" if active_input == "grid" else "grid"
                if event.key == pygame.K_RETURN:
                    try:
                        g = int(grid_size)
                        m = int(mine_count)
                        if not (5 <= g <= 30):
                            error_msg = "Grid: 5-30"
                        elif not (1 <= m < g*g):
                            error_msg = "Mines: 1 to grid²-1"
                        else:
                            result = (g, m)
                            done = True
                    except:
                        error_msg = "Enter valid numbers"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_grid.collidepoint(event.pos):
                    active_input = "grid"
                elif input_box_mines.collidepoint(event.pos):
                    active_input = "mines"
                elif button_rect.collidepoint(event.pos):
                    try:
                        g = int(grid_size)
                        m = int(mine_count)
                        if not (5 <= g <= 30):
                            error_msg = "Grid: 5-30"
                        elif not (1 <= m < g*g):
                            error_msg = "Mines: 1 to grid²-1"
                        else:
                            result = (g, m)
                            done = True
                    except:
                        error_msg = "Enter valid numbers"
                elif cancel_rect.collidepoint(event.pos):
                    done = True
                    result = None

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,120))
        screen.blit(overlay, (0,0))

        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_w, dialog_h)
        pygame.draw.rect(screen, (40, 42, 50), dialog_rect, border_radius=18)
        pygame.draw.rect(screen, (100, 100, 200), dialog_rect, 3, border_radius=18)

        title = font.render("Custom Game", True, (180, 180, 255))
        screen.blit(title, (dialog_x+90, dialog_y+18))

        label1 = font_label.render("Grid Size", True, (180,180,200))
        label2 = font_label.render("Mines", True, (180,180,200))
        screen.blit(label1, (dialog_x+40, dialog_y+50))
        screen.blit(label2, (dialog_x+220, dialog_y+50))

        pygame.draw.rect(screen, (30,30,36), input_box_grid, border_radius=8)
        pygame.draw.rect(screen, (100,180,255) if active_input=="grid" else (80,80,100), input_box_grid, 2, border_radius=8)
        pygame.draw.rect(screen, (30,30,36), input_box_mines, border_radius=8)
        pygame.draw.rect(screen, (100,180,255) if active_input=="mines" else (80,80,100), input_box_mines, 2, border_radius=8)
        grid_txt = input_font.render(grid_size, True, (180,180,255))
        mine_txt = input_font.render(mine_count, True, (180,180,255))
        screen.blit(grid_txt, (input_box_grid.x+12, input_box_grid.y+4))
        screen.blit(mine_txt, (input_box_mines.x+12, input_box_mines.y+4))

        pygame.draw.rect(screen, (60,180,120), button_rect, border_radius=10)
        pygame.draw.rect(screen, (40,120,80), button_rect, 2, border_radius=10)
        ok_txt = font_button.render("OK", True, (255,255,255))
        screen.blit(ok_txt, (button_rect.x+28, button_rect.y+7))
        pygame.draw.rect(screen, (180,60,60), cancel_rect, border_radius=10)
        pygame.draw.rect(screen, (120,40,40), cancel_rect, 2, border_radius=10)
        cancel_txt = font_button.render("Cancel", True, (255,255,255))
        screen.blit(cancel_txt, (cancel_rect.x+10, cancel_rect.y+7))

        if error_msg:
            err = font_label.render(error_msg, True, (255,80,80))
            screen.blit(err, (dialog_x+60, dialog_y+130))
        pygame.display.flip()
    return result

class Cell:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y + UI_HEIGHT, CELL_SIZE, CELL_SIZE) 
        self.is_mine = False 
        self.revealed = False 
        self.flagged = False 
        self.adjacent = 0 

def init_grid(safe_row=None, safe_col=None): 
    grid_height = 16 if current_difficulty == "Expert" else GRID_SIZE
    grid_width = 30 if current_difficulty == "Expert" else GRID_SIZE
    
    grid = [[Cell(col*CELL_SIZE, row*CELL_SIZE) 
             for col in range(grid_width)] for row in range(grid_height)]
    
    available_cells = []
    for row in range(grid_height):
        for col in range(grid_width):
            if safe_row is not None and safe_col is not None:
                if abs(row - safe_row) <= 1 and abs(col - safe_col) <= 1:
                    continue
            available_cells.append(grid[row][col])
    
    if len(available_cells) >= MINES_COUNT:
        mines = random.sample(available_cells, MINES_COUNT)
    else:
        mines = random.sample([c for row in grid for c in row], MINES_COUNT)
    
    for cell in mines: 
        cell.is_mine = True 
    for row in grid:
        for c in row:
            if c.is_mine:
                continue
            # Calculate the cell's row and col index
            c_row = (c.rect.y - UI_HEIGHT) // CELL_SIZE
            c_col = c.rect.x // CELL_SIZE
            neighbors = [
                (nr, nc)
                for nr in range(c_row - 1, c_row + 2)
                for nc in range(c_col - 1, c_col + 2)
            ]
            c.adjacent = sum(
                grid[nr][nc].is_mine
                for nr, nc in neighbors
                if 0 <= nr < grid_height and 0 <= nc < grid_width
            )
    return grid

def flood_fill(grid, row, col): 
    grid_height = 16 if current_difficulty == "Expert" else GRID_SIZE
    grid_width = 30 if current_difficulty == "Expert" else GRID_SIZE
    
    cell = grid[row][col] 
    if cell.revealed or cell.flagged: return 
    cell.revealed = True 
    if cell.adjacent == 0 and not cell.is_mine: 
        for dr in (-1,0,1): 
            for dc in (-1,0,1):
                r, c = row+dr, col+dc 
                if 0 <= r < grid_height and 0 <= c < grid_width: 
                    flood_fill(grid, r, c) 

def check_win(grid):
    for row in grid:
        for cell in row:
            if not cell.is_mine and not cell.revealed:
                return False
    return True

def show_game_over(screen): 
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box_width, box_height = 300, 150
    box_rect = pygame.Rect((WIDTH - box_width)//2, (HEIGHT - box_height)//2, box_width, box_height)
    pygame.draw.rect(screen, (255, 255, 255), box_rect)
    pygame.draw.rect(screen, COLORS["grid"], box_rect, 2)

    font = pygame.font.SysFont(None, 32)
    text = font.render("💥 You Lost!", True, COLORS["text"])
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
    screen.blit(text, text_rect)

    button_rect = pygame.Rect(WIDTH//2 - 40, HEIGHT//2 + 20, 80, 30)
    pygame.draw.rect(screen, COLORS["hidden"], button_rect)
    pygame.draw.rect(screen, COLORS["grid"], button_rect, 2)
    btn_text = pygame.font.SysFont(None, 24).render("OK", True, COLORS["text"])
    btn_text_rect = btn_text.get_rect(center=button_rect.center)
    screen.blit(btn_text, btn_text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Victory popup screen
def show_victory(screen, elapsed_time):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box_width, box_height = 320, 200
    box_rect = pygame.Rect((WIDTH - box_width)//2, (HEIGHT - box_height)//2, box_width, box_height)
    pygame.draw.rect(screen, (255, 255, 255), box_rect)
    pygame.draw.rect(screen, (0, 200, 0), box_rect, 3)

    font_large = pygame.font.SysFont(None, 36)
    font_medium = pygame.font.SysFont(None, 24)
    
    text = font_large.render("🎉 Victory!", True, (0, 150, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)
    
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, COLORS["text"])
    time_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
    screen.blit(time_text, time_rect)

    button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 30, 100, 35)
    pygame.draw.rect(screen, (0, 200, 0), button_rect)
    pygame.draw.rect(screen, COLORS["grid"], button_rect, 2)
    btn_text = pygame.font.SysFont(None, 24).render("New Game", True, (255, 255, 255))
    btn_text_rect = btn_text.get_rect(center=button_rect.center)
    screen.blit(btn_text, btn_text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

def main():
    pygame.init() 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption(f"Minesweeper - {current_difficulty}") 
    clock = pygame.time.Clock() 
    grid = init_grid() 
    game_over = False 
    game_won = False 
    start_time = pygame.time.get_ticks()
    first_click = True 

    def reset(): 
        nonlocal grid, game_over, game_won, start_time, first_click, screen
        grid, game_over, game_won = init_grid(), False, False 
        start_time = pygame.time.get_ticks()
        first_click = True
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Minesweeper - {current_difficulty}")

    def change_difficulty(new_difficulty):
        nonlocal screen
        set_difficulty(new_difficulty)
        reset()

    while True: 
        clock.tick(FPS) 
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and not game_over and not game_won:
                x, y = e.pos
                if y >= UI_HEIGHT:
                    row, col = (y - UI_HEIGHT)//CELL_SIZE, x//CELL_SIZE
                    grid_height = 16 if current_difficulty == "Expert" else GRID_SIZE
                    grid_width = 30 if current_difficulty == "Expert" else GRID_SIZE
                    if 0 <= row < grid_height and 0 <= col < grid_width:
                        cell = grid[row][col]
                        if e.button == 1:
                            if first_click:
                                first_click = False
                                start_time = pygame.time.get_ticks()
                                if cell.is_mine:
                                    grid = init_grid(row, col)
                                    cell = grid[row][col]
                                # After re-initializing, ensure the cell is not a mine
                                flood_fill(grid, row, col)
                                if check_win(grid):
                                    game_won = True
                                    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
                                    show_victory(screen, elapsed_time)
                                    reset()
                            else:
                                if cell.is_mine:
                                    game_over = True
                                    show_game_over(screen)
                                    reset()
                                else:
                                    flood_fill(grid, row, col)
                                    if check_win(grid):
                                        game_won = True
                                        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
                                        show_victory(screen, elapsed_time)
                                        reset()
                        elif e.button == 3:
                            if not cell.revealed:
                                cell.flagged = not cell.flagged
                elif 10 <= y <= 50:
                    for i, difficulty in enumerate(DIFFICULTIES.keys()):
                        button_x = 10 + i * 90
                        if button_x <= x <= button_x + 85:
                            if difficulty == "Custom":
                                result = show_custom_dialog(screen)
                                if result:
                                    g, m = result
                                    DIFFICULTIES["Custom"]["grid_size"] = g
                                    DIFFICULTIES["Custom"]["mines"] = m
                                    DIFFICULTIES["Custom"]["cell_size"] = 40 if g <= 15 else 30 if g <= 22 else 20
                                    set_difficulty("Custom")
                                    reset()
                            else:
                                change_difficulty(difficulty)
                            break
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                reset()

        screen.fill((50, 50, 50)) 
        
        pygame.draw.rect(screen, COLORS["ui_bg"], (0, 0, WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, COLORS["ui_border"], (0, UI_HEIGHT-1), (WIDTH, UI_HEIGHT-1), 2)
        
        button_font = pygame.font.SysFont("Arial", 16, bold=True)
        for i, difficulty in enumerate(DIFFICULTIES.keys()):
            button_x = 10 + i * 90
            button_rect = pygame.Rect(button_x, 10, 85, 30)
            button_color = (100, 200, 100) if difficulty == current_difficulty else (180, 180, 180)
            text_color = (255, 255, 255) if difficulty == current_difficulty else COLORS["text"]
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, COLORS["ui_border"], button_rect, 1)
            
            btn_text = button_font.render(difficulty, True, text_color)
            text_rect = btn_text.get_rect(center=button_rect.center)
            screen.blit(btn_text, text_rect)
        
        if not first_click and not game_over and not game_won:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        elif first_click:
            elapsed_time = 0
        else:
            elapsed_time = 0  
            
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_font = pygame.font.SysFont("Arial", 24, bold=True)
        time_text = time_font.render(f"⏱️ {minutes:02d}:{seconds:02d}", True, COLORS["text"])
        screen.blit(time_text, (10, 50))
        
        flagged_count = sum(1 for row in grid for cell in row if cell.flagged)
        remaining_mines = MINES_COUNT - flagged_count
        mine_text = time_font.render(f"💣 {remaining_mines:02d}", True, COLORS["text"])
        mine_rect = mine_text.get_rect()
        mine_rect.topright = (WIDTH - 10, 50)
        screen.blit(mine_text, mine_rect)
        
        for r, row in enumerate(grid): 
            for c, cell in enumerate(row):
                color = COLORS["revealed"] if cell.revealed else COLORS["hidden"]
                pygame.draw.rect(screen, color, cell.rect)
                
                if not cell.revealed:
                    pygame.draw.line(screen, (220, 220, 220), 
                                   (cell.rect.left, cell.rect.top), 
                                   (cell.rect.right-1, cell.rect.top), 2)
                    pygame.draw.line(screen, (220, 220, 220), 
                                   (cell.rect.left, cell.rect.top), 
                                   (cell.rect.left, cell.rect.bottom-1), 2)
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (cell.rect.right-1, cell.rect.top), 
                                   (cell.rect.right-1, cell.rect.bottom-1), 2)
                    pygame.draw.line(screen, (100, 100, 100), 
                                   (cell.rect.left, cell.rect.bottom-1), 
                                   (cell.rect.right-1, cell.rect.bottom-1), 2)
                else:
                    pygame.draw.rect(screen, COLORS["grid"], cell.rect, 1)
                
                if cell.flagged and not cell.revealed:
                    flag_size = CELL_SIZE // 6
                    center_x, center_y = cell.rect.center
                    pygame.draw.line(screen, (139, 69, 19), 
                                   (center_x, center_y - flag_size), 
                                   (center_x, center_y + flag_size), 3)
                    flag_points = [
                        (center_x + 2, center_y - flag_size),
                        (center_x + flag_size + 5, center_y - flag_size//2),
                        (center_x + 2, center_y)
                    ]
                    pygame.draw.polygon(screen, COLORS["flag"], flag_points)
                
                if cell.revealed:
                    if cell.is_mine:
                        center_x, center_y = cell.rect.center
                        mine_radius = CELL_SIZE // 4
                        pygame.draw.circle(screen, COLORS["mine"], (center_x, center_y), mine_radius)
                        spike_length = mine_radius // 2
                        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                            end_x = center_x + spike_length * pygame.math.Vector2(1, 0).rotate(angle).x
                            end_y = center_y + spike_length * pygame.math.Vector2(1, 0).rotate(angle).y
                            pygame.draw.line(screen, COLORS["mine"], (center_x, center_y), (end_x, end_y), 2)
                        pygame.draw.circle(screen, (150, 150, 150), (center_x - 3, center_y - 3), 3)
                        
                    elif cell.adjacent > 0:
                        number_color = COLORS["numbers"].get(cell.adjacent, COLORS["text"])
                        txt_font = pygame.font.SysFont("Arial", 20, bold=True)
                        txt = txt_font.render(str(cell.adjacent), True, number_color)
                        txt_rect = txt.get_rect(center=cell.rect.center)
                        screen.blit(txt, txt_rect)

        pygame.display.flip() 

if __name__ == "__main__":
    main()