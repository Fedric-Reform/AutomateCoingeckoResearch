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
EXCHANGE_NAME = "Gate.io"
EXCHANGE_ID = "gate"

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
  '20ex','abyss-world','aerodrome-finance','aether-games','aevo-exchange','agg','ait-protocol','alitaai','alltoscan','andromeda-2','andy-on-sol',
'apeironnft','aperture-finance','arcana-token','arrow-token','artificial-neural-network-ordinals','artrade','avalox','babybonk','bac-games',
'bad-idea-ai','based-brett','bee-launchpad','beercoin-2','ben-the-dog','beoble','bitbrawl','bitscrunch-token','blackcardcoin','blastoff',
'blendr-network','blockgames','blocksquare','blocx-2','blood-crystal','bone-bone','book-of-meme','bouncebit','bowled-io','brc-20-dex',
'brcstarter','brightpool','bvm','bxn','castle-of-blackwater','cat-in-a-dogs-world','catgpt','chatai','chex-token','chickencoin','childrens-aid-foundation',
'codyfight','common-wealth','copycat-finance','coq-inu','credefi','creo-engine','cross-the-ages','crypto-hunters-coin','ctomorrow-platform',
'decentralized-runes','decubate','deepfakeai','defactor','defispot','degen-base','demr','destra-network','dgi-game','digibyte','dimo',
'dopamine','drift-protocol','duko','dymension','early','edge-matrix-computing','edu3labs','eesee','egoncoin','electroneum','elixir-token',
'elysia','engines-of-fury','entangle','ethena','ether-fi','everipedia','everyworld','exverse','ezswap-protocol','flash-protocol',
'fluence-2','foxy','freebnk','gaimin','gam3s-gg','game-of-bitcoin-rune','gamebuild','gamercoin','gameta','gecko-inu','genesysgo-shadow',
'gme','green-shiba-inu','helium-mobile','heroes-of-mavia','hippop','honeyland-honey','htx-dao','hydro-protocol-2','hypercomic','hypergpt',
'imaginary-ones','intentx','io','ionic-protocol','ipor','iq50','ivendpay','juice-finance','jumoney','kim-token','laika-ai','legends-of-elysium',
'lends','lightlink','lillius','linear-protocol-lnr','little-dragon','lobo-the-wolf-pup-runes','lynex','maga-hat','maneki','marcopolo',
'masa-finance','mass-vehicle-ledger','medieus','meme-economics-rune','memusic','merlin-chain','merlin-chain-bridged-voya-merlin',
'merlin-starter','merlinswap','meson-network','metados','metahorse-unity','metaphone','mfercoin','microvisionchain','milady-wif-hat',
'miracle-play','mnet-continuum','mode','mog-coin','mon-protocol','multi-universe-central','myro','myso-token','nelore-coin',
'neurowebai','neversol','nexgami','nibiru','notcoin','nuklai','nulink-2','nyan','octavia','omni-network','onbuff','oobit','open-ticketing-ecosystem',
'orangedx','ordibank','ordify','origintrail','pandora','param','parcl','patex','peng','pepe-in-a-memes-world','pepefork','pigcoin-2',
'pixels','planet-mojo','playa3ull-games-2','playbux','ponke','popcat','portal-2','propbase','propy','pundu','punkai','qna3-ai','qubic-network',
'r-games','ready-to-fight','reboot-world','renzo','ring-ai','root-protocol','ruby-protocol','rsic-genesis-rune','safe','saga-2','satoshi-nakamoto-rune',
'satoshisync','satoshivm','scallop-2','schrodinger-2','sekuya-2','skai','slerf','smart-layer-network','smolecoin','snapmuse-io',
'solchat','spacecatch','spectral','sportsology-game','starheroes','starknet','statter-network','storyfire','subquery-network','swarm-markets',
'swisscheese','taiko','taproot','tars-protocol','tectum','tensor','the-next-gem-ai','thedonato-token','thetanuts-finance','toko','tonx',
'trex20','trinity-of-the-fabled-abyss-fragment','trio-ordinals','truflation','uncommon-goods','undeads-games','up','velar','vendetta',
'venom','verida','vimmer','vinci-protocol','virtual-protocol','vtrading','vyvo-smart-chain','wanko-manko-rune','weatherxm-network',
'weave6','web3war','wisdomise','wormhole','wrapped-eeth','wuffi','xswap-2','y8u','zeepr','zerolend','zetachain','zeus-network','zkswap-finance'
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
    output_file = f"GateioData.xlsx"
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
