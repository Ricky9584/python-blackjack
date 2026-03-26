import tkinter as tk
import random

class BlackjackApp:
    """An interactive Blackjack application developed in Python with a Tkinter interface."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Blackjack")
        self.root.configure(bg="#0b6623")
        
        # Standard set of cards
        self.suits = ["♣", "♦", "♥", "♠"]
        self.ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        # Game state variables
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.balance = 1000
        self.price = 0 

        self.setup_ui()
        self.draw_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.reset_game()

    def build_deck(self):
        """Creates and shuffles a new deck of cards."""
        self.deck = [(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.deck)

    def draw_card_from_deck(self) -> tuple:
        """Draws a single card. If the deck is empty, it rebuilds it."""
        if not self.deck:
            self.build_deck()
        return self.deck.pop()

    def calculate_score(self, hand: list) -> int:
        """Calculates the optimal score for the given hand of cards."""
        score = 0
        aces = 0
        
        for rank, _ in hand:
            if rank in ("J", "Q", "K"):
                score += 10
            elif rank == "A":
                score += 1
                aces += 1
            else:
                score += int(rank)
        
        # Promotes an Ace from 1 to 11 if it doesn't bust (exceed 21)
        if aces > 0 and score + 10 <= 21:
            score += 10
            
        return score

    def format_hand(self, hand: list) -> str:
        """Converts the list of card tuples into a visual string for the interface."""
        return "\n".join([f"{rank}{suit}" for rank, suit in hand])

    def setup_ui(self):
        """Initializes the graphical user interface (UI) and places the widgets."""
        # Title frame
        top_frame = tk.Frame(self.root, bg=self.root['bg'])
        top_frame.pack()

        title = tk.Label(top_frame, text="Welcome to Python Blackjack!", fg="Gold", bg="#0b6623",
                         width=50, height=3, font=("Helvetica", 36, "bold italic"))
        title.pack(side=tk.TOP)
        
        # Cards frame
        # Main container defined with a fixed height so place() coordinates have a canvas to map to
        label_frame = tk.Frame(self.root, bg="#0b6623", height=300)
        label_frame.pack(fill="x", pady=20)
        label_frame.pack_propagate(False) # Prevents the frame from collapsing
        
        # 1. Left section: Balance (Anchored to the West, at 10% of the screen width)
        self.balance_label = tk.Label(label_frame, text="Your balance:\n$" + str(self.balance),
                                      width=17, fg="white", bg="#0b6623", font=("Tahoma", 16))
        self.balance_label.place(relx=0.1, rely=0.5, anchor="w")
        
        # 2. Center section: Cards area (Anchored to its exact center, at 50% of screen width)
        cards_inner_frame = tk.Frame(label_frame, bg="#0b6623")
        cards_inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Headers (Row 0)
        player_header = tk.Label(cards_inner_frame, text="Your cards", fg="white", bg="#0b6623", font=("Tahoma", 16))
        player_header.grid(row=0, column=0, pady=(0, 10))
        
        dealer_header = tk.Label(cards_inner_frame, text="Dealer's cards", fg="white", bg="#0b6623", font=("Tahoma", 16))
        dealer_header.grid(row=0, column=1, pady=(0, 10))
        
        # Cards (Row 1)
        card_label_style = {"fg": "white", "bg": "#0b6623", "width": 15, "height": 8, 
                            "font": ("Tahoma", 19, "bold"), "highlightthickness": 6, 
                            "highlightbackground": "#022F0E"}
        
        self.cards_label = tk.Label(cards_inner_frame, text="", **card_label_style)
        self.cards_label.grid(row=1, column=0, padx=10)
        
        self.dealer_cards_label = tk.Label(cards_inner_frame, text="", **card_label_style)
        self.dealer_cards_label.grid(row=1, column=1, padx=10)

        # 3. Right section: Reset Button (Anchored to the East, at 90% of screen width)
        def on_enter(e):
            e.widget['bg'] = "#d8e0d9"
            
        def on_leave(e):
            e.widget['bg'] = "white"

        btn_style = {"width": 15, "height": 1, "fg": "black", "bg": "white", 
                     "font": ("Tahoma", 16), "border": 5, "relief": "ridge"}
        
        bet_label = tk.Label(label_frame, text="Enter bet amount:", fg="white", bg="#0b6623", font=("Tahoma", 16))
        bet_label.place(relx=0.9, rely=0.25, anchor="e")
        self.money_entry = tk.Entry(label_frame, width=20, font=("Tahoma", 14))
        self.money_entry.place(relx=0.9, rely=0.35, anchor="e")

        self.reset_btn = tk.Button(label_frame, text="New game", command=self.reset_game, **btn_style)
        self.reset_btn.bind("<Enter>", on_enter)
        self.reset_btn.bind("<Leave>", on_leave)
        self.reset_btn.place(relx=0.9, rely=0.75, anchor="e")


        # Outcome frame
        self.result_label = tk.Label(self.root, text="", fg="white", bg="#0b6623", font=("Tahoma", 19))
        self.result_label.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#0b6623")
        btn_frame.pack()

        self.draw_btn = tk.Button(btn_frame, text="Draw", command=self.player_draw, **btn_style)
        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop, **btn_style)
        
        for btn in (self.draw_btn, self.stop_btn):
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.pack(side=tk.LEFT, padx=40, pady=20)

    def update_display(self):
        """Updates the interface labels with the currently drawn cards."""
        self.cards_label.config(text=self.format_hand(self.player_hand))
        self.dealer_cards_label.config(text=self.format_hand(self.dealer_hand))

    def player_draw(self):
        """Handles the player's action of drawing a card."""
        card = self.draw_card_from_deck()
        self.player_hand.append(card)
        self.update_display()

        if self.calculate_score(self.player_hand) > 21:
            self.stop()

    def dealer_play(self):
        """The dealer plays automatically: draws until the score reaches 17 or higher."""
        while self.calculate_score(self.dealer_hand) < 17:
            card = self.draw_card_from_deck()
            self.dealer_hand.append(card)
        self.update_display()

    def stop(self):
        """Stops the player's turn, starts the dealer's turn, and determines the winner."""
        self.draw_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

        player_total = self.calculate_score(self.player_hand)

        # If the player has already busted
        if player_total > 21:
            self.result_label.config(text=f"Your cards' sum is: {player_total}, You busted!")
            self.balance -= self.price
            self.update_balance()
            return

        # Let the dealer play
        self.dealer_play()
        dealer_total = self.calculate_score(self.dealer_hand)

        # Determine the outcome
        if dealer_total > 21 or player_total > dealer_total:
            outcome = f"You won! Your opponent had {dealer_total}"
            self.balance += self.price
        elif player_total == dealer_total:
            outcome = f"Draw! Your opponent had {dealer_total}"
        else:
            outcome = f"You lost! Your opponent had {dealer_total}"
            self.balance -= self.price

        self.result_label.config(text=f"Your cards' sum is: {player_total}\n{outcome}")
        self.update_balance()
        
    def update_balance(self):
        """Helper to update the balance label text."""
        self.balance_label.config(text=f"Your balance:\n${self.balance}")

    def reset_game(self) -> None:
        """Resets the state to start a new game from scratch."""
        if self.balance == 0:
            self.result_label.config(text="You have no money left to play!")
            return
        
        bet_input = self.money_entry.get().strip()
        
        if not bet_input:
            self.result_label.config(text="You must enter a bet amount!")
            return
        
        if not bet_input.isdigit():
            self.result_label.config(text="You have to insert a number!")
            return
        
        self.price = int(bet_input)
        
        # Now safely check if player has enough
        if self.balance < self.price:
            self.result_label.config(text="You don't have enough money to play!")
            return
        
        # All validated, start the game
        self.reset_btn.config(state="disabled")
        self.draw_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.result_label.config(text="")
        self.update_balance()

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.build_deck()

        for _ in range(2):
            self.player_hand.append(self.draw_card_from_deck())
        self.dealer_hand.append(self.draw_card_from_deck())

        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1300x700')
    app = BlackjackApp(root)
    root.mainloop()