# Chess-Bot 

## Overview

ChessAI is a chess-playing bot developed entirely from scratch, without relying on any chess libraries. The project uses bitboards to manage the board state and implements the minimax algorithm with alpha-beta pruning, a custom evaluation function, and transposition tables. It can interact with the Lichess API, enabling gameplay against human players and other bots.

## Features

### Move Generation

* Bitboard-Based Move Generation: Legal moves are computed using bitboards, ensuring efficiency and correctness.

* Special Rules Handling: Castling, en passant, and pawn promotion are all correctly implemented.

### Decision Making

* Minimax Algorithm: The bot evaluates positions to choose the most promising move.

* Alpha-Beta Pruning: Speeds up decision-making by reducing the number of nodes evaluated.

* Move Ordering: Prioritizes moves with high tactical potential (e.g., queen moves) to enhance pruning effectiveness.

### Evaluation Function

* Piece Values and Positioning: Evaluates each piece's value and its position on the board.

* Penalty for Weak Pawn Structures: Considers penalties for doubled and isolated pawns.

* Endgame-Specific Adjustments: Encourages king centralization and pawn advancement in the endgame.

### Optimization

* Transposition Tables: Stores previously evaluated positions using Zobrist hashing to avoid redundant calculations.

* Dynamic Depth Adjustment: Depth of evaluation adapts based on the time taken for previous moves, allowing deeper searches during slower phases like the endgame.

### Opening Play

* Predefined Opening Book: Includes common opening moves to ensure the bot starts from strong tactical positions.

### API Integration

* Lichess API: The bot connects to Lichess to play games against other players and bots, with functionality to automate challenges and manage games.

## Achievements

* Achieving an approximate Elo rating of 1800
* Defeated a 2000 ELO bot on Lichess, here is the PGN of the game :
```pgn
1.e4 e6 2.d4 d5 3.exd5 exd5 4.Nc3 Nc6 5.Bb5 Qd7 6.Nf3 a6 7.Ba4 b5 8.Bb3 Nge7 9.Bf4 f6 10.O-O g5 11.Bg3 b4 12.Na4 g4 13.Nh4 a5 14.Nc5 Qd8 15.a4 Bg7 16.Re1 O-O 17.c3 f5 18.Bc2 f4 19.Qd3 Bf5 20.Nxf5 Rxf5 21.Bh4 Qd6 22.Nb7 Qd7 23.Bxe7 bxc3 24.Nc5 cxb2 25.Nxd7 bxa1=Q 26.Rxa1 Nxe7 27.Re1 g3 28.Rxe7 gxf2+ 29.Kxf2 Rh5 30.h3 c6 31.g4 Rh4 32.Ne5 Rf8 33.Nxc6 f3 34.Nxa5 Rxh3 35.Bb3 Rh2+ 36.Kg3 Re2 37.Bxd5+ Kh8 38.Rxe2 fxe2 39.Qxe2 Bxd4 40.Qe7 Bg7 41.Nc6 Ra8 42.Bb3 Bf8 43.Qf6+ Bg7 44.Qf7 Rf8 45.Qe6 Bb2 46.Ne5 Bd4 47.Nf7+ Kg8 48.Nh6+ Kh8 49.Qe7 Rb8 50.Nf7+ Kg8 51.Nh6+ Kh8 52.Qe6 Rf8 53.Qd5 Bg7 54.Qg8+ Rxg8 55.Nf7#  {*}
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NathanRouille/Chess-Bot.git
   cd Chess-Bot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Lichess API token:

   - Generate your Bot API token on Lichess at [lichess.org/account/oauth/token](https://lichess.org/account/oauth/token).
   - Save the token in a `.env` file or set it as an environment variable:

     ```
     LICHESS_TOKEN= 'your_token_here'
     ```

## Usage

1. Run the bot:

   ```bash
   python main.py
   ```

2. Paste the game ID in the terminal when prompted.
The game ID can be found in the URL of the Lichess game you want to analyze. For example:
For the URL https://lichess.org/abc123, the game ID is abc123.


## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
