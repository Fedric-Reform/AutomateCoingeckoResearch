import requests
import pandas as pd
import schedule
import time
from datetime import datetime

# Replace with your CoinGecko API Key
API_KEY = "CG-MfMJsvzUhR8PtJfvvSRi1UEm"

# CoinGecko API Base URL
COINGECKO_URL = "https://pro-api.coingecko.com/api/v3/"

# Exchange Details
EXCHANGE_NAME = "Bitget"
EXCHANGE_ID = "bitget"

# Function to fetch current Market Cap & FDV
def get_current_market_data(coin_id):
    url = f"{COINGECKO_URL}coins/{coin_id}?x_cg_pro_api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        market_cap = data.get("market_data", {}).get("market_cap", {}).get("usd", None)
        fdv = data.get("market_data", {}).get("fully_diluted_valuation", {}).get("usd", None)
        volume24h = data.get("market_data", {}).get("total_volume", {}).get("usd", None)
        return market_cap, fdv, volume24h
    except Exception as e:
        print(f"Error fetching current market data for {coin_id}: {e}")
        return None, None, None

# Function to fetch Order Book Depth (±2%) from Bybit
def fetch_depth(coin_id):
    url = f"{COINGECKO_URL}coins/{coin_id}/tickers?exchange_ids={EXCHANGE_ID}&depth=true&x_cg_pro_api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        tickers = data.get("tickers", {})
        if tickers:
            # Get the first ticker for the coin
            ticker = tickers[0]
            bid_ask_spread = ticker.get("bid_ask_spread_percentage", None)
            depth_plus_2 = ticker.get("cost_to_move_up_usd", None)
            depth_minus_2 = ticker.get("cost_to_move_down_usd", None)
        
            return bid_ask_spread, depth_plus_2, depth_minus_2
        return None, None, None
    except Exception as e:
        print(f"Error fetching depth data for {coin_id}: {e}")
        return None, None, None
        
    # try:
    #     response = requests.get(endpoint, params=params, headers=headers)
    #     response.raise_for_status()  # Raise an error for non-2xx responses
    #     return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching data: {e}")
    #     return None

# Function to fetch categories of a coin
def get_coin_categories(coin_id):
    url = f"{COINGECKO_URL}coins/{coin_id}?x_cg_pro_api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return ', '.join(data.get("categories", []))
    except Exception as e:
        print(f"Error fetching categories for {coin_id}: {e}")
        return "Unknown"


# Main function to fetch & compile data
# def fetch_and_save_data():
#     print("\n🚀 Fetching data...")

# Main function to fetch & compile data
def main():
    # List of coin_ids
    coin_list = [
    'aark-digital','aerodrome-finance','aethir','aevo-exchange','airtor-protocol','alephium','alpha-quark-token','altered-state-token',
    'alvara-protocol','apecoin','apeironnft','artrade','autonolas','based-brett','beercoin-2','ben-the-dog','bitkub-coin','bizauto',
    'blackcardcoin','blast','bloodloop','book-of-meme','bouncebit','cat-in-a-dogs-world','catamoto','catboy-3','catwifhat-2',
    'chainge-finance','civic','coinbarpay','cookie','creo-engine','daoversal','decubate','definder-capital','degen-base','dog-go-to-the-moon-rune',
    'drift-protocol','duko','dymension','engines-of-fury','ethena','ethena-usde','ether-fi','everipedia','first-digital-usd','flappymoonbird',
    'fud-the-pug','galatasaray-fan-token','gamercoin','gme','goldfinch','gui-inu','heroes-of-mavia','hiveswap','htx-dao',
    'hypergpt','iagon','ice','imaginary-ones','io','ivendpay','jungledoge','kamino','katana-inu','klever','landx-governance-token',
    'layerzero','legends-of-elysium','lifeform','linqai','lista','lukso-token-2','magic-crystal','maneki','marcopolo','masa-finance',
    'mass-vehicle-ledger','massa','matr1x','mch-coin','merlin-chain','microvisionchain','mintlayer','mnet-continuum','mode','moew',
    'mon-protocol','monsterra','mother-iggy','mumu-the-bull-3','navi','nervos-network','ness-lab','non-playable-coin','notcoin','nyan',
    'omni-network','ong','origintrail','parcl','peng','pikamoon','pirate-token','pixels','playzap','polyhedra-network','portal-2',
    'portuma','privateai','project-ailey','qna3-ai','rarible','ready-to-fight','reality-metaverse','renzo','saakuru-labs','safe',
    'saga-2','saucerswap','scallop-2','serenity-shield','shido-2','sillynubcat','six-network','slerf','smartworld-global','solarx-2',
    'souiland','spacecatch','starknet','sylo','taiko','telcoin','teleport-system-token','tensor','thetanuts-finance','trias-token',
    'true-usd','ultiverse','unice','vechain','veloce-vext','victoria-vr','virtual-protocol','wen-4','wisdomise','worldwide-usd',
    'wormhole','xpla','xzk','zeebu','zerolend','zetachain','zksync'
    ]

    results = []

    for coin_id in coin_list:
        print(f"Fetching data for: {coin_id}")

        # Get Current Market Cap & FDV
        market_cap_today, fdv_today, volume24h = get_current_market_data(coin_id)

        # Fetch Order Book Depth & Liquidity Metrics
        bid_ask_spread, depth_plus_2, depth_minus_2 = fetch_depth(coin_id)

        # Fetch Coin Category
        category = get_coin_categories(coin_id)


        # Store data in a dictionary
        results.append({
            "Exchange": EXCHANGE_NAME,
            "Category": category,
            "Token CEX": coin_id,
            "Market Cap Today": market_cap_today,
            "FDV Today": fdv_today,
            "Depth +2%": depth_plus_2,
            "Depth -2%": depth_minus_2, 
            "Bid Ask Spread Percentage": round(bid_ask_spread, 2) if bid_ask_spread else "N/A",
            "24H Volume (USD)": volume24h
        })

    # Convert results to DataFrame
    df_output = pd.DataFrame(results)

    # Save the data to a new Excel file with a timestamp in the filename
    output_file = f"BitgetData{datetime.now().strftime('%Y%m%d')}.xlsx"
    df_output.to_excel(output_file, index=False)

    print(f"✅ Data saved to {output_file}")

# Schedule the function to run daily at a specific time (e.g., 08:00 AM)
# schedule.every().day.at("08:00").do(fetch_and_save_data)

# print("⏳ Scheduler is running. Press Ctrl+C to stop.")

# Keep the script running indefinitely
# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check for scheduled tasks every 60 seconds

if __name__ == "__main__":
    main()
