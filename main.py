from fastapi import FastAPI, HTTPException, Query
from service import get_snapshot
from models import SnapshotResponse
import uvicorn
import logging

# Initialize the Application
app = FastAPI(
    title="Market Snapshot API",
    description="High-performance backend reasoning engine for stock data.",
    version="1.0.0"
)

# Initialize Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/api/snapshot", response_model=SnapshotResponse)
async def get_market_snapshot(ticker: str = Query(..., min_length=1, max_length=10, description="The stock ticker symbol (e.g. NVDA)")):
    """
    Main Endpoint: GET /api/snapshot
    
    Flow:
    1. Receives ticker from user.
    2. Calls service layer to fetch data + generate reasoning.
    3. Returns structured JSON.
    
    Error Handling:
    - If ticker is invalid or data not found -> 404.
    - If upstream API fails -> 503.
    """
    try:
        logger.info(f"Received request for ticker: {ticker}")
        
        # Call the logic layer
        snapshot = await get_snapshot(ticker)
        
        return snapshot

    except ValueError as e:
        # Service raises ValueError if ticker doesn't exist or has no data
        logger.warning(f"Validation error for {ticker}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found or no data available.")
        
    except Exception as e:
        # Catch-all for unexpected issues (e.g., yfinance down, network issues)
        logger.error(f"Internal error processing {ticker}: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable. Could not fetch market data.")

if __name__ == "__main__":
    # Entry point for local debugging
    # Workers=1 is sufficient for dev; in prod we'd use gunicorn with uvicorn workers.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
