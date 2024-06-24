from analyze_manual_download import analyze_manual_download
from screen_compare import find_cards
import tkinter as tk
from tkinter import messagebox

def handle_choice(choice):
    if choice == "Choice 1":
        # Do something for Choice 1
        messagebox.showinfo("Choice", "You selected Choice 1")
    elif choice == "Choice 2":
        # Do something for Choice 2
        messagebox.showinfo("Choice", "You selected Choice 2")
    elif choice == "Choice 3":
        # Do something for Choice 3
        messagebox.showinfo("Choice", "You selected Choice 3")
    elif choice == "Choice 4":
        # Do something for Choice 4
        messagebox.showinfo("Choice", "You selected Choice 4")
    elif choice == "Choice 5":
        # Do something for Choice 5
        messagebox.showinfo("Choice", "You selected Choice 5")


data_dict = analyze_manual_download()
active_archetype = ''
pack_cards = []
pick = 0

def find_best_for_arch(cards, arch):
    analyze = {}
    for card in cards:
        analyze[card] = data_dict[card][arch]
    
    return max(analyze, key=analyze.get), analyze[max(analyze, key=analyze.get)]

while(True):
    
    card_list=None
    if pick % 8 < len(pack_cards):
        card_list = pack_cards[pick%8]
    pick += 1
    cards = find_cards('MH3', [i for i in card_list if i not in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']]) 
    pack_cards.append(cards)
    if len(cards) == 0:
        print('No cards found. Trying again...')
    
    this_pick_analysis = {}
    for card in cards:
        this_card_data = data_dict[card]
        best_archetype = max(this_card_data, key=this_card_data.get)
        best_val = this_card_data[best_archetype]
        this_pick_analysis[card] = best_val

    best_pick = max(this_pick_analysis, key=this_pick_analysis.get)
    message_string = f'Overall, I think you should take {best_pick}. It has a GIH WR of ' \
           f'{data_dict[best_pick][max(data_dict[best_pick], key=data_dict[best_pick].get)]} in ' \
            f'{max(data_dict[best_pick], key=data_dict[best_pick].get).upper()}. '
    
    choices = {best_pick: max(data_dict[best_pick], key=data_dict[best_pick].get)}

    better_card, better_perc = find_best_for_arch(cards, active_archetype)
    choices[better_card] = active_archetype
    message_string += f'(Alternatively, if you want to stay in {active_archetype.upper()}, take {better_card}. Its GIH WR for {active_archetype.upper()} is {better_perc})'

    root = tk.Tk()
    root.withdraw()

    selected_choice = messagebox.askquestion(f"Change Direction?", message_string, icon="question")

    if selected_choice == 'yes':
        active_archetype = choices[better_card]

    print('Yay!')
    
        



