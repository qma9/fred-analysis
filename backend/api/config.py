# FRED base URL
BASE_URL = "https://api.stlouisfed.org/fred"

# FRED API endpoints
SERIES_ENDPOINT = "series"
OBSERVATIONS_ENDPOINT = f"{SERIES_ENDPOINT}/observations"

SERIES_IDS = [
    # Macro data
    "RRPONTSYD",  # ✅ Overnight Reverse Repurchase Agreements: Treasury Securities Sold by the Federal Reserve in the Temporary Open Market Operations
    "DTWEXAFEGS",  # ✅ Nominal Advanced Foreign Economies U.S. Dollar Index
    "DTB3",  # ✅ 3-Month Treasury Bill Secondary Market Rate, Discount Basis (Percent)
    "WM2NS",  # ✅ W M2 money supply
    "UNRATE",  # ✅ M Unemployment Rate
    "T5YIE",  # ✅ 5-Year Breakeven Inflation Rate
    # Financial markets data
    "VIXCLS",  # ✅ CBOE Volatility Index: VIX
    "OVXCLS",  # ✅ CBOE Crude Oil ETF Volatility Index
    # Controls
    "INFECTDISEMVTRACKD",  # ✅ Equity Market Volatility: Infectious Disease Tracker
    # Tech sector data
    "AITINO",  # ✅ M Manufacturers' New Orders: Information Technology Industries
    "IPG3344S",  # ✅ M Industrial Production: Manufacturing: Durable Goods: Semiconductor and Other Electronic Component (NAICS = 3344)
    # Cryptocurrency data
    "CBBTCUSD",  # ✅ Coinbase Bitcoin (USD)
]


SEMICONDUCTOR_SERIES = [
    "IPG3344S",
    "VIXCLS",
    "OVXCLS",
    "WM2NS",
    "DTWEXAFEGS",
    "DTB3",
    "INFECTDISEMVTRACKD",
    "UNRATE",
    "T5YIE",
    "AITINO",
]


CRYPTOCURRENCY_SERIES = [
    "CBBTCUSD",
    "VIXCLS",
    "OVXCLS",
    "WM2NS",
    "RRPONTSYD",
    "DTWEXAFEGS",
    "DTB3",
    "INFECTDISEMVTRACKD",
    "UNRATE",
    "T5YIE",
]
