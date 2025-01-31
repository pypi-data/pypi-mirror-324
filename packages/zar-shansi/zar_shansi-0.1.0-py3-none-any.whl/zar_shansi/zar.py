import random
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

dice_faces = {
    1: """
    ┌───────┐
    │       │
    │   ●   │
    │       │
    └───────┘
    """,
    2: """
    ┌───────┐
    │ ●     │
    │       │
    │     ● │
    └───────┘
    """,
    3: """
    ┌───────┐
    │ ●     │
    │   ●   │
    │     ● │
    └───────┘
    """,
    4: """
    ┌───────┐
    │ ●   ● │
    │       │
    │ ●   ● │
    └───────┘
    """,
    5: """
    ┌───────┐
    │ ●   ● │
    │   ●   │
    │ ●   ● │
    └───────┘
    """,
    6: """
    ┌───────┐
    │ ●   ● │
    │ ●   ● │
    │ ●   ● │
    └───────┘
    """
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_dice(options):
    clear()
    print(Fore.CYAN + "Zar Atılıyor..." + Style.RESET_ALL)
    time.sleep(1)

    dice_value = random.randint(1, 6)
    selected_option = random.choice(options)

    color_map = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    color = color_map[dice_value - 1] 

    print(color + dice_faces[dice_value] + Style.RESET_ALL) 
    print(Fore.WHITE + f"Sonuç: {dice_value}" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + f"Seçilen: {selected_option}" + Style.RESET_ALL)

def get_user_options():
    options = []
    print(Fore.LIGHTGREEN_EX + "Lütfen seçimleri girin (En az 2 seçenek, bitince 'tamam' yazın):" + Style.RESET_ALL)
    
    while True:
        option = input(Fore.LIGHTYELLOW_EX + "Seçenek: " + Style.RESET_ALL).strip()
        if option.lower() == "tamam" and len(options) >= 2:
            break
        elif option.lower() == "tamam":
            print(Fore.RED + "En az 2 seçenek girmelisin!" + Style.RESET_ALL)
        elif option:
            options.append(option)

    return options
def start_game():
    while True:
        options = get_user_options()
        
        input(Fore.LIGHTGREEN_EX + "\nZar atmak için ENTER'a basın..." + Style.RESET_ALL)
        roll_dice(options)
        
        play_again = input(Fore.LIGHTCYAN_EX + "\nTekrar oynamak ister misin? (E/H): " + Style.RESET_ALL).strip().lower()
        if play_again != 'e':
            print(Fore.LIGHTRED_EX + "\nOyun bitti! Görüşmek üzere!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    start_game()