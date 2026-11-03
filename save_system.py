import json
import os

class GameState:
    def __init__(self):
        self.player_level = 1
        self.player_xp = 0
        self.inventory = []
        self.current_location = "Town"

    def add_xp(self, amount):
        self.player_xp += amount
        print(f"Gained {amount} XP. Total XP: {self.player_xp}")
        # In a real game, you'd check for level ups here

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added {item} to inventory.")

    def move_to(self, location):
        self.current_location = location
        print(f"Moved to {self.current_location}.")

    def display_status(self):
        print("\n--- Current Status ---")
        print(f"Level: {self.player_level}")
        print(f"XP: {self.player_xp}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print(f"Location: {self.current_location}")
        print("----------------------\n")

class SaveManager:
    def __init__(self, filename="savegame.json"):
        self.filename = filename

    def save_game(self, game_state):
        # Convert GameState object to a dictionary for JSON serialization
        data_to_save = {
            "player_level": game_state.player_level,
            "player_xp": game_state.player_xp,
            "inventory": game_state.inventory,
            "current_location": game_state.current_location
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"Game saved successfully to {self.filename}.")
        except IOError as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        if not os.path.exists(self.filename):
            print("No save file found. Starting new game.")
            return GameState() # Return a new game state if no save exists

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            # Create a new GameState and populate it with loaded data
            game_state = GameState()
            game_state.player_level = loaded_data.get("player_level", 1)
            game_state.player_xp = loaded_data.get("player_xp", 0)
            game_state.inventory = loaded_data.get("inventory", [])
            game_state.current_location = loaded_data.get("current_location", "Town")

            print(f"Game loaded successfully from {self.filename}.")
            return game_state
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading game: {e}. Starting new game.")
            return GameState() # Return a new game state on error

# --- Example Usage ---
if __name__ == "__main__":
    save_manager = SaveManager()
    current_game = save_manager.load_game() # Attempt to load existing game

    current_game.display_status()

    # Simulate gameplay
    current_game.add_xp(50)
    current_game.add_item("Sword")
    current_game.move_to("Forest")
    current_game.add_xp(100)
    current_game.add_item("Potion")

    current_game.display_status()

    # Save the game
    save_manager.save_game(current_game)

    print("\n--- Restarting the script to demonstrate loading ---")
    # Simulate restarting the application
    reloaded_game = save_manager.load_game()
    reloaded_game.display_status()
