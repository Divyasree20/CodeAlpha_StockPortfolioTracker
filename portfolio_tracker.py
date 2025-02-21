import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import time
import threading

# Define an empty portfolio dictionary
portfolio = {}  # Now stores stock data + alert thresholds
price_alerts = {}  # Dictionary to store stock alert thresholds

# Function to add stock with purchase price
def add_stock(symbol, shares, purchase_price):
    """Add stock to the portfolio with purchase price."""
    if symbol in portfolio:
        portfolio[symbol]["shares"] += shares
        portfolio[symbol]["purchase_price"] = purchase_price  # Update purchase price
    else:
        portfolio[symbol] = {"shares": shares, "purchase_price": purchase_price}
    
    print(f"✅ Added {shares} shares of {symbol} at ${purchase_price:.2f} per share.")

# Function to remove stock
def remove_stock(symbol, shares):
    """Remove stocks from the portfolio."""
    if symbol in portfolio:
        if portfolio[symbol]["shares"] > shares:
            portfolio[symbol]["shares"] -= shares
            print(f"✅ Removed {shares} shares of {symbol}.")
        elif portfolio[symbol]["shares"] == shares:
            del portfolio[symbol]
            print(f"✅ Removed all shares of {symbol} from portfolio.")
        else:
            print(f"⚠ You don't own that many shares of {symbol}.")
    else:
        print(f"⚠ Stock {symbol} is not in your portfolio.")

# Function to fetch real-time stock prices and check alerts
def get_stock_price(symbol):
    """Fetch the latest stock price and check alerts."""
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]  # Get latest stock price
        price = round(price, 2)

        # Check alerts
        if symbol in price_alerts:
            if price >= price_alerts[symbol]["high"]:
                print(f"🚨 ALERT: {symbol} has risen above ${price_alerts[symbol]['high']}! Current: ${price}")
            if price <= price_alerts[symbol]["low"]:
                print(f"⚠️ ALERT: {symbol} has dropped below ${price_alerts[symbol]['low']}! Current: ${price}")

        return price
    except Exception as e:
        print(f"⚠ Error fetching price for {symbol}: {e}")
        return None

# Function to view portfolio with stock values
def view_portfolio():
    """Display portfolio with real-time stock prices and values."""
    if not portfolio:
        print("\n📭 Your portfolio is empty.")
        return

    print("\n📊 Your Stock Portfolio:")
    total_value = 0  # Track total portfolio value
    
    for symbol, data in portfolio.items():
        shares = data["shares"]
        price = get_stock_price(symbol)
        if price:
            stock_value = price * shares
            total_value += stock_value
            print(f"{symbol}: {shares} shares | Price: ${price:.2f} | Value: ${stock_value:.2f}")
    
    print(f"\n💰 Total Portfolio Value: ${total_value:.2f}")

# Function to calculate gains/losses
def calculate_gains():
    """Calculate profit/loss for each stock."""
    print("\n📊 Stock Performance (Gains/Losses):")
    total_profit_loss = 0.0  # Track total portfolio gains/losses

    for symbol, data in portfolio.items():
        shares = data["shares"]
        purchase_price = data["purchase_price"]
        
        current_price = get_stock_price(symbol)  # Fetch live stock price
        if current_price:
            total_cost = shares * purchase_price  # Initial investment
            current_value = shares * current_price  # Current worth
            profit_loss = current_value - total_cost  # Profit or loss amount
            profit_loss_percent = (profit_loss / total_cost) * 100  # Percentage change
            
            total_profit_loss += profit_loss
            
            print(f"{symbol}: Bought at ${purchase_price:.2f}, Now ${current_price:.2f} → "
                  f"{'📈 Gain' if profit_loss > 0 else '📉 Loss'}: ${profit_loss:.2f} ({profit_loss_percent:.2f}%)")
    
    print("\n💰 Total Portfolio Gains/Losses: ${:.2f}".format(total_profit_loss))

# Function to plot portfolio distribution
def plot_portfolio():
    """Visualize stock holdings as a pie chart."""
    if not portfolio:
        print("\n📭 Your portfolio is empty.")
        return

    labels = []
    sizes = []

    for symbol, data in portfolio.items():
        shares = data["shares"]
        price = get_stock_price(symbol)
        if price:
            value = shares * price
            labels.append(symbol)
            sizes.append(value)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("📊 Stock Portfolio Distribution")
    plt.show()

# Function to set price alerts
def set_price_alert(symbol, high, low):
    """Set price alerts for a stock."""
    price_alerts[symbol] = {"high": high, "low": low}
    print(f"🔔 Alert set for {symbol}: Above ${high} or Below ${low}.")

# Function to automatically update stock prices every minute
def auto_update_prices():
    while True:
        view_portfolio()
        time.sleep(60)  # Update every 60 seconds

# Start live tracking in a separate thread
tracking_thread = threading.Thread(target=auto_update_prices, daemon=True)
tracking_thread.start()

# Main menu loop
while True:
    print("\n1️⃣ Add Stock")
    print("2️⃣ Remove Stock")
    print("3️⃣ View Portfolio")
    print("4️⃣ View Portfolio Value")
    print("5️⃣ View Gains/Losses")
    print("6️⃣ View Portfolio Graph")
    print("7️⃣ Set Price Alerts")
    print("8️⃣ Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        symbol = input("Enter stock symbol: ").upper()
        shares = int(input(f"Enter number of shares for {symbol}: "))
        purchase_price = float(input(f"Enter purchase price per share for {symbol}: "))
        add_stock(symbol, shares, purchase_price)
    elif choice == "2":
        symbol = input("Enter stock symbol to remove: ").upper()
        shares = int(input(f"Enter number of shares to remove for {symbol}: "))
        remove_stock(symbol, shares)
    elif choice == "3":
        view_portfolio()
    elif choice == "4":
        view_portfolio()
    elif choice == "5":
        calculate_gains()
    elif choice == "6":
        plot_portfolio()
    elif choice == "7":
        symbol = input("Enter stock symbol to set alert: ").upper()
        high = float(input(f"Set HIGH alert price for {symbol}: "))
        low = float(input(f"Set LOW alert price for {symbol}: "))
        set_price_alert(symbol, high, low)
    elif choice == "8":
        print("👋 Exiting. Thank you for using the stock tracker!")
        break
    else:
        print("⚠ Invalid choice. Please enter a valid option.")
