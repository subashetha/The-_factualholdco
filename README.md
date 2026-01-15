# Market Snapshot API 📈

A high-performance backend microservice that delivers real-time stock market data and instant heuristic reasoning. Built with **FastAPI** to ensure low latency (<2000ms response).

## 🚀 Features

- **Real-Time Data**: Fetches live market data (Price, Volume, Change) using `yfinance`.
- **Heuristic Logic Engine**: Automatically generates a **Thesis** (Bullish/Bearish) and **Risk Assessment** (High/Low/Medium) based on price action and Beta volatility.
- **RESTful API**: Simple, well-documented API endpoints.
- **Production Ready**: Lightweight and designed for easy deployment (includes `Procfile` for Railway/Heroku).

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Data Source**: [yfinance](https://pypi.org/project/yfinance/)
- **Data Processing**: Pandas & Pydantic
- **Server**: Uvicorn

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/market-snapshot-api.git
   cd market-snapshot-api
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Locally**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## 📖 API Documentation

### Get Market Snapshot
Fetches data and reasoning for a specific stock ticker.

- **Endpoint**: `GET /api/snapshot`
- **Query Parameters**:
  - `ticker` (string, required): The stock symbol (e.g., `NVDA`, `AAPL`, `TSLA`).

#### Example Request
```bash
curl "http://127.0.0.1:8000/api/snapshot?ticker=NVDA"
```

#### Example Response
```json
{
  "meta": {
    "ticker": "NVDA",
    "timestamp": "2023-10-27T10:30:00"
  },
  "data": {
    "price": 405.00,
    "change_percent": 2.5,
    "volume": 35000000
  },
  "reasoning": {
    "thesis": "Strong Bullish momentum detected. Price is significantly outperforming daily baseline.",
    "risk": "HIGH. This asset historically moves significantly more than the market."
  }
}
```

## 📦 Deployment

This project includes a `Procfile` and is ready for deployment on platforms like **Railway** or **Heroku**.

```bash
# Procfile command
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 📄 License

MIT License.
