"""Chess API MCP Server for https://chess-api.com/"""
from typing import Optional, List
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Chess API")

# Chess API endpoint
CHESS_API_URL = "https://chess-api.com/v1"


@mcp.tool()
async def analyze_position(fen: str, depth: Optional[int] = None) -> str:
    """
    Analyze a chess position using the Chess API engine.
    
    Args:
        fen: Chess position in FEN (Forsyth-Edwards Notation) format
        depth: Optional analysis depth (higher = more accurate but slower)
               Depth 12 ≈ 2350 FIDE (IM level)
               Depth 18 ≈ 2750 FIDE (GM Hikaru level)
               Depth 20 ≈ 2850 FIDE (GM Magnus level)
    
    Returns:
        Detailed analysis including best move, evaluation, win chances, and continuation
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {"fen": fen}
            if depth is not None:
                payload["depth"] = depth
            
            response = await client.post(CHESS_API_URL, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response
            result = "Chess Position Analysis:\n\n"
            result += f"Position (FEN): {fen}\n\n"
            
            # Type of response
            if "type" in data:
                result += f"Response Type: {data['type']}\n"
            
            # Evaluation
            if "eval" in data:
                eval_val = data["eval"]
                result += f"Evaluation: {eval_val:+.2f}\n"
                if eval_val > 0:
                    result += "  (White is winning)\n"
                elif eval_val < 0:
                    result += "  (Black is winning)\n"
                else:
                    result += "  (Equal position)\n"
            
            # Win chance
            if "winChance" in data:
                win_chance = data["winChance"]
                result += f"Win Chance: {win_chance:.2f}%\n"
                if win_chance > 50:
                    result += f"  (White: {win_chance:.1f}%, Black: {100-win_chance:.1f}%)\n"
                else:
                    result += f"  (White: {win_chance:.1f}%, Black: {100-win_chance:.1f}%)\n"
            
            # Depth
            if "depth" in data:
                result += f"Analysis Depth: {data['depth']}\n"
            
            # Mate detection
            if "mate" in data:
                mate_in = data["mate"]
                if mate_in > 0:
                    result += f"Mate detected: White mates in {mate_in} moves\n"
                else:
                    result += f"Mate detected: Black mates in {abs(mate_in)} moves\n"
            
            # Best move
            if "san" in data:
                result += f"\nBest Move: {data['san']}\n"
            
            if "from" in data and "to" in data:
                result += f"  From {data['from']} to {data['to']}\n"
            
            # Move details
            if "piece" in data:
                pieces = {
                    'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop',
                    'r': 'Rook', 'q': 'Queen', 'k': 'King'
                }
                piece_name = pieces.get(data['piece'], data['piece'])
                result += f"  Piece: {piece_name}\n"
            
            if "promotion" in data:
                promo_pieces = {
                    'q': 'Queen', 'r': 'Rook', 'b': 'Bishop', 'n': 'Knight'
                }
                result += f"  Promotion to: {promo_pieces.get(data['promotion'], data['promotion'])}\n"
            
            if "isCapture" in data and data["isCapture"]:
                result += "  Capture: Yes\n"
                if "captured" in data:
                    result += f"  Captured piece: {data['captured']}\n"
            
            if "isCastling" in data and data["isCastling"]:
                result += "  Castling: Yes\n"
            
            # Text description
            if "text" in data:
                result += f"\nDescription: {data['text']}\n"
            
            # Continuation
            if "continuationArr" in data:
                continuation = data["continuationArr"]
                if continuation:
                    result += f"\nBest Continuation: {' '.join(continuation[:10])}\n"
                    if len(continuation) > 10:
                        result += f"  ... and {len(continuation) - 10} more moves\n"
            
            # Current turn
            if "turn" in data:
                turn = "White" if data["turn"] == "w" else "Black"
                result += f"\nTurn: {turn}\n"
            
            return result.strip()
            
        except httpx.HTTPStatusError as e:
            return f"Error from Chess API (HTTP {e.response.status_code}): {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error connecting to Chess API: {str(e)}"
        except Exception as e:
            return f"Error analyzing position: {str(e)}"


@mcp.tool()
async def analyze_moves(moves: str, depth: Optional[int] = None) -> str:
    """
    Analyze a chess game from a sequence of moves.
    
    Args:
        moves: Text input with a list of moves (e.g., "e4 e5 Nf3 Nc6")
        depth: Optional analysis depth (higher = more accurate but slower)
    
    Returns:
        Analysis of the final position after all moves
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {"input": moves}
            if depth is not None:
                payload["depth"] = depth
            
            response = await client.post(CHESS_API_URL, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the response
            result = "Chess Game Analysis:\n\n"
            result += f"Moves: {moves}\n\n"
            
            # Type of response
            if "type" in data:
                result += f"Response Type: {data['type']}\n"
            
            # Evaluation
            if "eval" in data:
                eval_val = data["eval"]
                result += f"Evaluation: {eval_val:+.2f}\n"
                if eval_val > 0:
                    result += "  (White is winning)\n"
                elif eval_val < 0:
                    result += "  (Black is winning)\n"
                else:
                    result += "  (Equal position)\n"
            
            # Win chance
            if "winChance" in data:
                win_chance = data["winChance"]
                result += f"Win Chance: {win_chance:.2f}%\n"
                if win_chance > 50:
                    result += f"  (White: {win_chance:.1f}%, Black: {100-win_chance:.1f}%)\n"
                else:
                    result += f"  (White: {win_chance:.1f}%, Black: {100-win_chance:.1f}%)\n"
            
            # Depth
            if "depth" in data:
                result += f"Analysis Depth: {data['depth']}\n"
            
            # Mate detection
            if "mate" in data:
                mate_in = data["mate"]
                if mate_in > 0:
                    result += f"Mate detected: White mates in {mate_in} moves\n"
                else:
                    result += f"Mate detected: Black mates in {abs(mate_in)} moves\n"
            
            # Best move
            if "san" in data:
                result += f"\nBest Move: {data['san']}\n"
            
            if "from" in data and "to" in data:
                result += f"  From {data['from']} to {data['to']}\n"
            
            # Move details
            if "piece" in data:
                pieces = {
                    'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop',
                    'r': 'Rook', 'q': 'Queen', 'k': 'King'
                }
                piece_name = pieces.get(data['piece'], data['piece'])
                result += f"  Piece: {piece_name}\n"
            
            if "promotion" in data:
                promo_pieces = {
                    'q': 'Queen', 'r': 'Rook', 'b': 'Bishop', 'n': 'Knight'
                }
                result += f"  Promotion to: {promo_pieces.get(data['promotion'], data['promotion'])}\n"
            
            if "isCapture" in data and data["isCapture"]:
                result += "  Capture: Yes\n"
                if "captured" in data:
                    result += f"  Captured piece: {data['captured']}\n"
            
            if "isCastling" in data and data["isCastling"]:
                result += "  Castling: Yes\n"
            
            # Text description
            if "text" in data:
                result += f"\nDescription: {data['text']}\n"
            
            # Continuation
            if "continuationArr" in data:
                continuation = data["continuationArr"]
                if continuation:
                    result += f"\nBest Continuation: {' '.join(continuation[:10])}\n"
                    if len(continuation) > 10:
                        result += f"  ... and {len(continuation) - 10} more moves\n"
            
            # Current turn
            if "turn" in data:
                turn = "White" if data["turn"] == "w" else "Black"
                result += f"\nTurn: {turn}\n"
            
            # Move flags
            if "flags" in data:
                result += f"Move Flags: {data['flags']}\n"
            
            return result.strip()
            
        except httpx.HTTPStatusError as e:
            return f"Error from Chess API (HTTP {e.response.status_code}): {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error connecting to Chess API: {str(e)}"
        except Exception as e:
            return f"Error analyzing moves: {str(e)}"


@mcp.tool()
async def get_best_move(fen: str, depth: Optional[int] = None) -> str:
    """
    Get the best move for a chess position with detailed analysis.
    
    Args:
        fen: Chess position in FEN format
        depth: Optional analysis depth (default uses engine's default)
               Recommended: 12-20 for strong analysis
    
    Returns:
        Best move with evaluation and explanation
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {"fen": fen}
            if depth is not None:
                payload["depth"] = depth
            
            response = await client.post(CHESS_API_URL, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Simple focused output on the best move
            result = ""
            
            if "san" in data:
                result += f"Best Move: {data['san']}\n"
            
            if "from" in data and "to" in data:
                result += f"Move: {data['from']} → {data['to']}\n"
            
            if "eval" in data:
                result += f"Evaluation: {data['eval']:+.2f}\n"
            
            if "mate" in data:
                mate_in = data["mate"]
                if mate_in > 0:
                    result += f"Forced Mate: White mates in {mate_in}\n"
                else:
                    result += f"Forced Mate: Black mates in {abs(mate_in)}\n"
            
            if "winChance" in data:
                result += f"Win Chance: {data['winChance']:.1f}%\n"
            
            if "text" in data:
                result += f"\n{data['text']}\n"
            
            if "continuationArr" in data and data["continuationArr"]:
                result += f"\nBest Line: {' '.join(data['continuationArr'][:8])}\n"
            
            return result.strip() if result else "No analysis available"
            
        except httpx.HTTPStatusError as e:
            return f"Error from Chess API (HTTP {e.response.status_code}): {e.response.text}"
        except httpx.RequestError as e:
            return f"Network error connecting to Chess API: {str(e)}"
        except Exception as e:
            return f"Error getting best move: {str(e)}"


def main() -> None:
    """Run the Chess API MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
