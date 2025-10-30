import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from sklearn.linear_model import LinearRegression

def fetch_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

def plot_closing_prices(data, ticker):
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], color='blue', label='Close Price')
    plt.title(f'Closing Prices of {ticker}')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()

def prepare_data(data):
    data = data.copy()
    data['Index'] = np.arange(len(data))
    return data

def train_regression_model(index, prices):
    model = LinearRegression()
    model.fit(index.reshape(-1,1), prices)
    return model

def predict_future_prices(model, last_index, num_days):
    future_indices = np.arange(last_index+1, last_index+1+num_days).reshape(-1,1)
    future_preds = model.predict(future_indices)
    return future_preds

def main():
    print("============== Stock Predictor ==============")
    ticker = input("Enter Stock Ticker (e.g. MSFT): ").strip().upper()
    start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
    end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
    num_days = int(input("Days to Predict Into The Future: "))

    try:
        data = fetch_stock_data(ticker, start_date, end_date)
    except Exception as e:
        print(f"Could not fetch data. Error: {e}")
        return

    if data.empty:
        print("No data found. Please check your ticker or date range.")
        return

    plot_closing_prices(data, ticker)
    data = prepare_data(data)
    X = data['Index'].values
    y = data['Close'].values

    model = train_regression_model(X, y)
    future_preds = predict_future_prices(model, X[-1], num_days)
    print("\nPredicted closing prices for the next {} days:".format(num_days))
    for i, price in enumerate(future_preds, 1):
        print(f"Day {i}: {float(price):.2f}")

    plt.figure(figsize=(10,5))
    plt.plot(data.index, y, label='Actual Close Price')
    last_date = data.index[-1]
    future_dates = pd.bdate_range(last_date + timedelta(days=1), periods=num_days)
    plt.plot(future_dates, future_preds, 'r--', label='Predicted Price')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{ticker} - Actual & Predicted Closing Prices")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
