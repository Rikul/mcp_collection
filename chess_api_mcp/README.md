# Chess API MCP Module

This module provides tools for analyzing chess positions and games using the [Chess API](https://chess-api.com/). The API offers powerful chess engine analysis with detailed move evaluations, win percentages, and continuation lines.

## Available Tools

### analyze_position
Analyze a chess position using the Chess API engine.

**Arguments:**
- `fen` (required): Chess position in FEN (Forsyth-Edwards Notation) format
- `depth` (optional): Analysis depth for accuracy
  - Depth 12 ≈ 2350 FIDE (International Master level)
  - Depth 18 ≈ 2750 FIDE (Grandmaster Hikaru Nakamura level)
  - Depth 20 ≈ 2850 FIDE (Grandmaster Magnus Carlsen level)

**Returns:**
- Best move with algebraic notation
- Position evaluation (negative = Black winning, positive = White winning)
- Win chance percentage (50% = equal, >50% = White advantage, <50% = Black advantage)
- Analysis depth
- Forced mate detection (if applicable)
- Move details (piece, capture, castling, promotion)
- Best continuation line
- Textual description

**Example:**
```python
analyze_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# Starting position analysis

analyze_position("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4", depth=18)
# Italian Game with high depth analysis
```

### analyze_moves
Analyze a chess game from a sequence of moves.

**Arguments:**
- `moves` (required): Text input with list of moves (e.g., "e4 e5 Nf3 Nc6")
- `depth` (optional): Analysis depth

**Returns:**
Same detailed analysis as `analyze_position` but for the final position after all moves are played.

**Example:**
```python
analyze_moves("e4 e5 Nf3 Nc6 Bb5")
# Ruy Lopez opening analysis

analyze_moves("1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6", depth=15)
# Ruy Lopez with numbered moves
```

### get_best_move
Get the best move for a position with a simplified, focused output.

**Arguments:**
- `fen` (required): Chess position in FEN format
- `depth` (optional): Analysis depth (recommended: 12-20)

**Returns:**
Concise output with:
- Best move in algebraic notation
- Move coordinates (from → to)
- Evaluation
- Win chance
- Brief description
- Short continuation line

**Example:**
```python
get_best_move("rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
# Get best move in this position
```

## API Response Fields

The Chess API provides rich information about each position:

- **type**: Response type ("move", "bestmove", or "info")
- **eval**: Position evaluation (negative = Black winning)
- **depth**: Analysis depth (higher = more accurate)
- **winChance**: Win percentage (50% = equal position)
- **mate**: Forced mate sequence length (if detected)
- **san**: Move in Short Algebraic Notation (e.g., "Nf3", "O-O")
- **from/to**: Move coordinates (e.g., "e2" to "e4")
- **piece**: Moving piece type (p/n/b/r/q/k)
- **captured**: Captured piece (if any)
- **promotion**: Promoted piece type (if applicable)
- **isCastling**: Whether move is castling
- **isCapture**: Whether move captures a piece
- **continuationArr**: Array of best continuation moves
- **turn**: Current player's turn (w/b)
- **text**: Human-readable description

## FEN Format

FEN (Forsyth-Edwards Notation) is the standard notation for describing chess positions.

**Format:** `[position] [turn] [castling] [en-passant] [halfmove] [fullmove]`

**Examples:**
- Starting position: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
- After 1.e4: `rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1`

## Running the Server

Install the dependencies and launch the MCP server:

```bash
# Using pip
pip install -e .
chess-api-mcp

# Using uv
uv pip install -e .
chess-api-mcp
```

## Dependencies

- `mcp`: MCP SDK for creating tools
- `httpx`: Async HTTP client for API requests

## API Endpoint

This module uses the Chess API at:
- **POST**: `https://chess-api.com/v1`
- **WebSocket**: `wss://chess-api.com/v1` (for streaming analysis)

## Use Cases

1. **Opening Analysis**: Analyze positions from your favorite openings
2. **Tactical Training**: Find best moves in tactical positions
3. **Game Review**: Analyze your games move by move
4. **Position Evaluation**: Understand who's winning and by how much
5. **Mate Detection**: Find forced checkmate sequences
6. **Learning**: Study engine suggestions with detailed explanations

## Notes

- Higher depth values provide more accurate analysis but take longer
- The API uses a strong chess engine for analysis
- Win chance calculations use the Lichess formula
- Negative evaluations favor Black, positive favor White
- Mate numbers show moves until checkmate
