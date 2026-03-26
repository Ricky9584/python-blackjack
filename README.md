# Python Blackjack

A fully functional Blackjack card game built with Python and Tkinter.

## Features

- 🎰 Play against the dealer with realistic rules
- 💰 Betting system with balance tracking
- 🎯 Proper Blackjack rules (Ace handling, dealer AI, bust detection)
- 🎨 Clean, interactive GUI with hover effects
- ✅ Input validation for bet amounts

## Requirements

- Python 3.8+
- tkinter (included with Python)

## Installation

git clone https://github.com/Ricky9584/python-blackjack.git
cd python-blackjack
python blackjack_objects.py

## How to Play

1. Enter a bet amount and click "New game"
2. You start with $1000
3. Click "Draw" to hit, "Stop" when ready
4. Get closer to 21 than the dealer without going over
5. Win your bet if you beat the dealer, lose it if you bust or lose

## Game Rules

- **Face cards** (J, Q, K) = 10 points
- **Aces** = 1 or 11 (automatically optimized)
- **Bust** = exceed 21 (you lose)
- **Dealer** stands at 17 or higher
- **Draw** = tie (no money exchanged)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
