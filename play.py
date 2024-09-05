import httpx

BASE_URL = 'http://127.0.0.1:8000/api/'  # Base URL of the API
player_identity = None


def start_game():
    global player_identity
    print("Welcome to the Isopod Adventure Game! 🐞")
    player_identity = input("Enter your identity to start or resume the game: ")

    # Start or resume the game for the player
    response = httpx.post(f"{BASE_URL}player/", data={'identity': player_identity})

    if response.status_code == 200:
        print(f"Game started for identity '{player_identity}'.")
        show_current_location()
    else:
        print("Failed to start the game. Please try again.")
        exit(1)


def show_current_location():
    # Get the current location and player details
    response = httpx.get(f"{BASE_URL}player/{player_identity}/")

    if response.status_code == 200:
        player_data = response.json()
        location = player_data['current_location']
        print(f"\nYou are at: {location['name']}")
        print(f"Description: {location['description']}")

        available_directions = []
        for direction in ['north', 'south', 'east', 'west']:
            if location[direction]:
                available_directions.append(direction.capitalize())

        print(f"Available directions: {', '.join(available_directions)}")
    else:
        print("Failed to get current location.")


def move(direction):
    # Move in a given direction
    response = httpx.post(f"{BASE_URL}move/{player_identity}/{direction.lower()}/")

    if response.status_code == 200:
        print(response.json()['message'])
        show_current_location()
    else:
        print(response.json().get('message', 'Failed to move in that direction.'))


def pick_up_item():
    # Pick up an item at the current location
    response = httpx.post(f"{BASE_URL}pickup/{player_identity}/")

    if response.status_code == 200:
        print(response.json()['message'])
        show_inventory()
    else:
        print(response.json().get('message', 'No items to pick up here!'))


def show_inventory():
    # Show player's inventory
    response = httpx.get(f"{BASE_URL}inventory/{player_identity}/")

    if response.status_code == 200:
        inventory_items = response.json()
        print("\nYour Inventory:")
        if inventory_items:
            for item in inventory_items:
                print(f"- {item['name']}")
        else:
            print("Your inventory is empty.")
    else:
        print("Failed to retrieve inventory.")


def main():
    start_game()

    while True:
        print("\nAvailable actions: move, pickup, inventory, quit")
        action = input("What would you like to do? ").strip().lower()

        if action == 'move':
            direction = input("Enter direction (north, south, east, west): ").strip().lower()
            if direction in ['north', 'south', 'east', 'west']:
                move(direction)
            else:
                print("Invalid direction. Please choose from north, south, east, or west.")
        elif action == 'pickup':
            pick_up_item()
        elif action == 'inventory':
            show_inventory()
        elif action == 'quit':
            print("Thank you for playing the Isopod Adventure Game! 🐞")
            break
        else:
            print("Invalid action. Please choose from move, pickup, inventory, or quit.")


if __name__ == "__main__":
    main()
