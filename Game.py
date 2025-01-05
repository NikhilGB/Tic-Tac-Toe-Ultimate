import tkinter as tk
from tkinter import messagebox
import pygame
import sys

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        
        # Bind window closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize pygame mixer for sounds
        pygame.mixer.init()
        
        # Load sound files (replace with your sound file paths)
        try:
            self.click_sound = pygame.mixer.Sound("click.wav")
            self.victory_sound = pygame.mixer.Sound("victory.wav")
            self.background_music = pygame.mixer.Sound("background.mp3")
        except pygame.error:
            print("Warning: Sound files not found. Game will run without sound.")
            self.click_sound = None
            self.victory_sound = None
            self.background_sound = None
        
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        
        self.main_menu_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        
        # Create turn indicator label
        self.turn_indicator = tk.Label(
            self.game_frame,
            text="Player X's Turn",
            font=('Arial', 16),
            fg="blue"
        )
        self.turn_indicator.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.create_main_menu()
        self.create_game_board()
        
        self.show_main_menu()
        
    def create_main_menu(self):
        title = tk.Label(self.main_menu_frame, text="Tic Tac Toe", font=('Arial', 24))
        title.pack(pady=20)
        
        start_button = tk.Button(self.main_menu_frame, text="Start Game", 
                               font=('Arial', 16), command=self.start_game)
        start_button.pack(pady=10)
        
        quit_button = tk.Button(self.main_menu_frame, text="Quit", 
                              font=('Arial', 16), command=self.on_closing)
        quit_button.pack(pady=10)
    
    def create_game_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="", font=('Arial', 20),
                                 width=5, height=2,
                                 command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)
    
    def stop_all_sounds(self):
        # Stop background music if playing
        if hasattr(self, 'background_music') and self.background_music:
            self.background_music.stop()
        pygame.mixer.stop()  # Stop all playing sounds
    
    def show_main_menu(self):
        self.game_frame.pack_forget()
        self.main_menu_frame.pack()
        # Play background music
        if hasattr(self, 'background_music') and self.background_music:
            self.background_music.play(-1)  # -1 means loop indefinitely
    
    def start_game(self):
        self.main_menu_frame.pack_forget()
        self.game_frame.pack()
        self.stop_all_sounds()  # Stop background music
        self.reset_game()
    
    def update_turn_indicator(self):
        self.turn_indicator.config(
            text=f"Player {self.current_player}'s Turn",
            fg="blue" if self.current_player == "X" else "red"
        )
    
    def button_click(self, row, col):
        index = row * 3 + col
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                fg="blue" if self.current_player == "X" else "red"
            )
            
            # Play click sound
            if self.click_sound:
                self.click_sound.play()
            
            if self.check_winner():
                if self.victory_sound:
                    self.victory_sound.play()
                self.turn_indicator.config(
                    text=f"Player {self.current_player} Wins!",
                    fg="green"
                )
                result = messagebox.askyesno(
                    "Game Over",
                    f"Player {self.current_player} wins!\nDo you want to play again?"
                )
                self.handle_game_end(result)
            elif "" not in self.board:
                if self.victory_sound:
                    self.victory_sound.play()
                self.turn_indicator.config(
                    text="It's a Draw!",
                    fg="orange"
                )
                result = messagebox.askyesno(
                    "Game Over",
                    "It's a draw!\nDo you want to play again?"
                )
                self.handle_game_end(result)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.update_turn_indicator()
    
    def check_winner(self):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != "":
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != "":
                return True
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != "":
            return True
        if self.board[2] == self.board[4] == self.board[6] != "":
            return True
        return False
    
    def handle_game_end(self, play_again):
        if play_again:
            self.reset_game()
        else:
            self.show_main_menu()
    
    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="")
        self.update_turn_indicator()
    
    def on_closing(self):
        """Handle window closing event"""
        self.stop_all_sounds()  # Stop all sounds
        pygame.mixer.quit()     # Quit pygame mixer
        self.root.destroy()     # Destroy the window
        sys.exit()             # Exit the program
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
