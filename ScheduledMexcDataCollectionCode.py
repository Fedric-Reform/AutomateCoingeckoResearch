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
EXCHANGE_NAME = "MEXC"
EXCHANGE_ID = "mxc"

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
    'abyss-world','aerodrome-finance','aethir','aevo-exchange','airtor-protocol','ait-protocol','alephium','alltoscan','altered-state-token',
'altlayer','alvara-protocol','andromeda-2','andy-on-sol','apecoin','arcana-token','arrow-token','artfi','artrade','asmatch','atlas-navi',
'aurora-near','autoair-ai','autonolas','avalox','babybonk','bad-idea-ai','beercoin-2','befi-labs','ben-the-dog','beoble','biaoqing','big-pump',
'bitbrawl','bitscrunch-token','bizauto','blackcardcoin','blast','blendr-network','blockgames','blocksquare','blocx-2','blood-crystal',
'book-of-meme','bouncebit','brcstarter','bvm','bxn','canxium','castle-of-blackwater','cat-in-a-dogs-world','catamoto','catboy-3',
'catwifhat-3','chainge-finance','chex-token','chickencoin','clearpool','coinbarpay','common-wealth','cookie','coq-inu','creo-engine',
'cross-the-ages','crypto-hunters-coin','ctomorrow-platform','dechat','decubate','deepfakeai','defactor','definder-capital','defispot','degen-base',
'depin-dao','destra-network','devve','dgi-game','digitalbits','dimitra','dog-go-to-the-moon-rune','dogwifcoin','dopamine','drift-protocol',
'duko','dymension','ecomi','edge-matrix-computing','edu3labs','eesee','electroneum','elixir-token','elysia','email-token','engines-of-fury',
'entangle','ethena','ether-fi','ethereum-push-notification-service','evadore','everipedia','exverse','first-digital-usd','forward',
'freebnk','fud-the-pug','gaimin','galaxis-token','gam3s-gg','gamebuild','gamercoin','gecko-inu','gme','goldfinch','gptverse','gram-2',
'graphlinq-protocol','green-bitcoin','green-shiba-inu','gui-inu','hashpack','helium-mobile','heroes-of-mavia','hippop','honeyland-honey','htx-dao',
'hydro-protocol-2','hypercomic','hypergpt','ice','imaginary-ones','ime-lab','io','iq50','ivendpay','jobchain','kamino','karrat',
'katana-inu','kim-token','kitten-haimer','klever','koala-ai','laika-ai','landx-governance-token','layerzero','legends-of-elysium','lends',
'lightlink','linqai','lista','little-dragon','lobo-the-wolf-pup-runes','lukso-token-2','lynex','maga-hat','mainnetz','maneki','marcopolo','masa-finance',
'mass-vehicle-ledger','massa','matr1x','mch-coin','memusic','merlin-chain','meson-network','metados','metahorse-unity','mfercoin',
'microvisionchain','mintlayer','mixmob','mode','moew','mog-coin','mon-protocol','monsterra','mother-iggy','multi-universe-central',
'mumu-the-bull-3','myro','nakamoto-games','navi','nervos-network','nettensor','neuron','neurowebai','nibiru','non-playable-coin',
'notcoin','nuklai','nyan','octavia','omni-network','omnicat','ong','open-ticketing-ecosystem','orangedx','ordibank','ordify','param',
'parcl','partisia-blockchain','patex','paysenger-ego','peng','pepe-in-a-memes-world','pepefork','pigcoin-2','pikamoon','pitbull',
'pivx','pixels','planet-mojo','playa3ull-games-2','playbux','playzap','polyhedra-network','ponke','popcat','portal-2','portuma','privateai',
'propbase','propy','pundu','punkai','qna3-ai','qorpo-world','qubic-network','r-games','rarible','reach','ready-to-fight','realio-network',
'reality-metaverse','renzo','richquack','ring-ai','rogin-ai','roost','roseon','saakuru-labs','safe','saga-2','satoshisync','satoshivm',
'saucerswap','scallop-2','sekuya-2','shido-2','sillynubcat','six-network','skai','slash-vision-labs','slerf','smart-layer-network',
'smartworld-global','smolecoin','snapmuse-io','solarx-2','solchat','solidus-aitech','sora-ai','spacecatch','spectral','sportsology-game',
'starheroes','starknet','storm-warfare','storyfire','subquery-network','swarm-markets','swisscheese','sylo','syncus','ta-da','taiko','tars-protocol',
'tectum','teh-epik-duck','tensor','the-next-gem-ai','thetanuts-finance','toadie-meme-coin','trex20','trias-token','trinity-of-the-fabled-abyss-fragment','trio-ordinals',
'true-usd','truflation','ultiverse','undeads-games','unice','unigraph-ordinals','up','vechain','velar','veloce-vext','venom','verida',
'victoria-vr','virtual-protocol','vita-inu','volumint','vtrading','vyvo-smart-chain','wall-street-games-2','weatherxm-network',
'weave6','wen-4','wisdomise','worldwide-usd','wormhole','wuffi','xpla','xswap-2','xzk','y8u','zeebu','zentry','zerolend','zetachain',
'zeus-network','zkswap-finance','zksync'
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
    output_file = f"MexcData{datetime.now().strftime('%Y%m%d')}.xlsx"
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
