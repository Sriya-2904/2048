from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import random

GRID_SIZE = 4

class Game2048(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = GRID_SIZE
        self.tiles = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.generate_tile()
        self.generate_tile()
        self.build_ui()

    def build_ui(self):
        self.labels = []
        for row in range(GRID_SIZE):
            row_labels = []
            for col in range(GRID_SIZE):
                label = Label(text="", font_size=40, color=(0, 0, 0, 1))
                row_labels.append(label)
                self.add_widget(label)
            self.labels.append(row_labels)
        self.update_ui()

    def generate_tile(self):
        empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.tiles[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            # Higher score increases chance of "4"
            self.tiles[r][c] = 4 if random.random() > 0.1 else 2

    def update_ui(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.tiles[r][c]
                self.labels[r][c].text = str(value) if value else ""

    def slide_and_merge(self, row):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        return new_row + [0] * (GRID_SIZE - len(new_row))

    def move(self, direction):
        moved = False
        if direction == "left":
            for r in range(GRID_SIZE):
                new_row = self.slide_and_merge(self.tiles[r])
                if new_row != self.tiles[r]:
                    moved = True
                self.tiles[r] = new_row
        elif direction == "right":
            for r in range(GRID_SIZE):
                new_row = self.slide_and_merge(self.tiles[r][::-1])[::-1]
                if new_row != self.tiles[r]:
                    moved = True
                self.tiles[r] = new_row
        elif direction == "up":
            for c in range(GRID_SIZE):
                col = [self.tiles[r][c] for r in range(GRID_SIZE)]
                new_col = self.slide_and_merge(col)
                if new_col != col:
                    moved = True
                for r in range(GRID_SIZE):
                    self.tiles[r][c] = new_col[r]
        elif direction == "down":
            for c in range(GRID_SIZE):
                col = [self.tiles[r][c] for r in range(GRID_SIZE)]
                new_col = self.slide_and_merge(col[::-1])[::-1]
                if new_col != col:
                    moved = True
                for r in range(GRID_SIZE):
                    self.tiles[r][c] = new_col[r]

        if moved:
            self.generate_tile()
            self.update_ui()
            if self.check_game_over():
                print("Game Over")

    def check_game_over(self):
        for row in self.tiles:
            if 0 in row:
                return False
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.tiles[r][c] == self.tiles[r][c + 1] or self.tiles[c][r] == self.tiles[c + 1][r]:
                    return False
        return True


class TouchHandler(FloatLayout):
    def __init__(self, game_board, **kwargs):
        super().__init__(**kwargs)
        self.game_board = game_board
        self.touch_start = (0, 0)

    def on_touch_down(self, touch):
        self.touch_start = touch.pos

    def on_touch_up(self, touch):
        dx = touch.pos[0] - self.touch_start[0]
        dy = touch.pos[1] - self.touch_start[1]

        # Detect swipe direction
        if abs(dx) > abs(dy):
            if dx > 50:
                self.game_board.move("right")
            elif dx < -50:
                self.game_board.move("left")
        else:
            if dy > 50:
                self.game_board.move("up")
            elif dy < -50:
                self.game_board.move("down")


class Game2048App(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.game_board = Game2048()

        # Add swipe detection
        touch_handler = TouchHandler(self.game_board)
        layout.add_widget(self.game_board)
        layout.add_widget(touch_handler)

        return layout


if __name__ == '__main__':
    Game2048App().run()
