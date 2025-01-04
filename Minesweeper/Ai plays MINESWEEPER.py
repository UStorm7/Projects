import random

class Minesweeper:
    """Representation of the Minesweeper game."""

    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty board
        self.board = [[False for _ in range(width)] for _ in range(height)]

        # Add mines randomly
        while len(self.mines) < mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """Return the number of mines adjacent to a cell."""
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if (di == 0 and dj == 0):
                    continue
                ni, nj = cell[0] + di, cell[1] + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    count += self.board[ni][nj]
        return count

    def won(self):
        """Check if all mines have been found."""
        return self.mines_found == self.mines

class Sentence:
    """Logical statement about a Minesweeper game."""

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_safes(self):
        """Return cells known to be safe."""
        if self.count == 0:
            return self.cells.copy()
        return set()

    def known_mines(self):
        """Return cells known to be mines."""
        if len(self.cells) == self.count:
            return self.cells.copy()
        return set()

    def mark_safe(self, cell):
        """Update the sentence if a cell is known to be safe."""
        if cell in self.cells:
            self.cells.remove(cell)

    def mark_mine(self, cell):
        """Update the sentence if a cell is known to be a mine."""
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

class MinesweeperAI:
    """AI to play Minesweeper."""

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """Update the AI's knowledge base."""
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if (di == 0 and dj == 0):
                    continue
                ni, nj = cell[0] + di, cell[1] + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) not in self.safes and (ni, nj) not in self.mines:
                        neighbors.add((ni, nj))

        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        self.update_knowledge()

    def update_knowledge(self):
        """Infer new information from the knowledge base."""
        for sentence in self.knowledge.copy():
            safes = sentence.known_safes()
            mines = sentence.known_mines()
            for safe in safes:
                self.mark_safe(safe)
            for mine in mines:
                self.mark_mine(mine)

        self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

    def make_safe_move(self):
        """Return a safe cell to choose."""
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """Return a random move that is not known to be a mine."""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    return (i, j)
        return None

def main():
    # Initialize the Minesweeper game and AI
    game = Minesweeper(height=8, width=8, mines=8)
    ai = MinesweeperAI(height=8, width=8)

    print("Minesweeper Game Started!")
    print(f"Board size: {game.height}x{game.width}")
    print(f"Number of mines: {len(game.mines)}")
    print()

    # Keep playing until the game is won or no moves are left
    while not game.won():
        # Get a safe move from the AI
        move = ai.make_safe_move()
        if move is None:
            # If no safe move, make a random move
            move = ai.make_random_move()
            if move is None:
                print("No moves left to make!")
                break

        # Make the move and check the outcome
        if game.is_mine(move):
            print(f"AI stepped on a mine at {move}! Game over.")
            break
        else:
            # Get the number of nearby mines and update the AI
            count = game.nearby_mines(move)
            print(f"AI moved to {move} with {count} nearby mines.")
            ai.add_knowledge(move, count)

        # Print game progress
        print(f"Mines found: {len(ai.mines)} / {len(game.mines)}")
        print(f"Safe moves made: {len(ai.safes)}")
        print()

    # Check if the game was won
    if game.won():
        print("AI won the game by identifying all mines!")
    else:
        print("Game ended before AI could identify all mines.")

if __name__ == "__main__":
    main()
