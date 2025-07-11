from main import get_pokemon_data, get_random_pokemon_data
from picachu import print_welcome_art

def print_pokemon_info(pokemon):
    print(f"ID: {pokemon['id']}")
    print(f"Name: {pokemon['name']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print(f"Types: {', '.join(pokemon['types'])}")

def menu():
    while True:
        print_welcome_art()
        print("\nWelcome to the Pokémon Drawer!")
        print("1. Draw a Pokémon")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            while True:
                print("\nHow would you like to draw your Pokémon?")
                print("1. By name")
                print("2. By ID")
                print("3. Random")
                draw_choice = input("Enter your choice (1/2/3): ").strip()

                pokemon = None
                if draw_choice == "1":
                    name = input("Enter the Pokémon name: ").strip().lower()
                    pokemon = get_pokemon_data(name)
                elif draw_choice == "2":
                    poke_id = input("Enter the Pokémon ID: ").strip()
                    pokemon = get_pokemon_data(poke_id)
                elif draw_choice == "3":
                    pokemon = get_random_pokemon_data()
                else:
                    print("Invalid option. Please choose 1, 2, or 3.")
                    continue

                if pokemon:
                    print("\nHere are the details of the drawn Pokémon:")
                    print_pokemon_info(pokemon)
                    print("\nPokémon drawn successfully.")
                    continue_choice = input("\nWould you like to draw another one? (y/n): ").strip().lower()
                    if continue_choice != "y":
                        print("Goodbye!")
                        return
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    menu()
