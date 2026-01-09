import yfinance as yf
from datetime import datetime
from models import SnapshotResponse, Meta, MarketData, Reasoning
import logging

# Configure logging to track what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_snapshot(ticker_symbol: str) -> SnapshotResponse:
    """
    Orchestrator function:
    1. Fetches raw data.
    2. Applies reasoning logic.
    3. Returns structured response.
    """
    # Step 1: Fetch Real Data
    # usage of yfinance is chosen for its reliability and ease of use for free data.
    logger.info(f"Fetching data for {ticker_symbol}")
    info, history = _fetch_data(ticker_symbol)

    # Step 2: Extract key metrics
    current_price = info.get('currentPrice') or info.get('regularMarketPrice')
    
    # Fallback logic: If real-time price is missing, use the last close
    if not current_price and not history.empty:
        current_price = history['Close'].iloc[-1]
    
    if not current_price:
        raise ValueError(f"Could not find price data for {ticker_symbol}")

    # Calculate change percentage (using previous close)
    previous_close = info.get('previousClose') or (history['Close'].iloc[-2] if len(history) > 1 else current_price)
    change_percent = ((current_price - previous_close) / previous_close) * 100

    # Step 3: Synthesis/Reasoning
    # We pass the raw numbers to our internal logic engine to produce the 'Thesis'
    reasoning = _generate_reasoning(change_percent, info.get('beta', 1.0))

    # Step 4: Construct Response
    return SnapshotResponse(
        meta=Meta(
            ticker=ticker_symbol.upper(),
            timestamp=datetime.now()
        ),
        data=MarketData(
            price=round(current_price, 2),
            change_percent=round(change_percent, 2),
            volume=info.get('volume') or 0
        ),
        reasoning=reasoning
    )

def _fetch_data(ticker: str):
    """
    Wraps yfinance calls.
    Why: Keeps external API coupling isolated in one function.
    """
    tik = yf.Ticker(ticker)
    
    # Get 'info' for fundamental data (beta, sector, etc.)
    # Get 'history' for today's price action
    return tik.info, tik.history(period="5d")

def _generate_reasoning(change_pct: float, beta: float) -> Reasoning:
    """
    HEURISTIC REASONING ENGINE
    
    Goal: Provide a quick "Thesis" and "Risk" assessment without an LLM.
    
    Logic 1: Trend Identification (Thesis)
       - If change > 2%: Strong Bullish momentum.
       - If change > 0.5%: Mild Bullish.
       - If change < -2%: Strong Bearish.
       - Else: Neutral/Sideways.
       
    Logic 2: Risk Assessment (Risk)
       - We use 'Beta' (market volatility relative to S&P 500).
       - Beta > 1.5: High Risk (Volatile stock like Tesla/Nvidia).
       - Beta < 0.8: Low Risk (Stable stock like Johnson & Johnson).
       - Else: Medium Risk.
       
    Why this logic?
       - It is deterministic (always gives the same answer for the same numbers).
       - It computes in microseconds (meeting the 2000ms requirement).
    """
    
    # 1. Thesis Generation
    if change_pct > 3.0:
        thesis = "Strong Bullish momentum detected. Price is significantly outperforming daily baseline."
    elif change_pct > 0.5:
        thesis = "Modest Bullish trend. Stock is trading positively but within normal variance."
    elif change_pct < -3.0:
        thesis = "Strong Bearish pressure. Significant sell-off detected today."
    elif change_pct < -0.5:
        thesis = "Bearish sentiment. Stock is underperforming daily baseline."
    else:
        thesis = "Neutral/Consolidation. Price is chopping sideways with no clear direction."

    # 2. Risk Generation using Beta
    # Beta measures how much the stock moves compared to the general market.
    # Default to 1.0 (Market Average) if beta is missing.
    beta_val = beta if beta else 1.0
    
    if beta_val > 1.5:
        risk = "HIGH. This asset historically moves significantly more than the market."
    elif beta_val < 0.85:
        risk = "LOW. This asset is historically defensive and stable."
    else:
        risk = "MEDIUM. Volatility is in line with the broader market."

    return Reasoning(thesis=thesis, risk=risk)
