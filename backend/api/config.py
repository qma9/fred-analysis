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
    "A939RX0Q048SBEA",  # Q ✅ Real Gross Domestic Product per Capita
    "WM2NS",  # W M2 money supply
    "UNRATE",  # M Unemployment Rate
    "T5YIE",  # ✅ 5-Year Breakeven Inflation Rate
    # Financial markets data
    "SP500",  # ✅ S&P 500
    "VIXCLS",  # ✅ CBOE Volatility Index: VIX
    "OVXCLS",  # ✅ CBOE Crude Oil ETF Volatility Index
    # Controls
    "USREC",  # M NBER based Recession Indicators for the United States from the Period following the Peak through the Trough
    "UMCSENT",  # M University of Michigan: Consumer Sentiment
    "INFECTDISEMVTRACKD",  # ✅ Equity Market Volatility: Infectious Disease Tracker
    # Tech sector data
    "AITINO",  # M Manufacturers' New Orders: Information Technology Industries
    # "CAPUTLG3344S",  # M Capacity Utilization: Manufacturing: Durable Goods: Semiconductor and Other Electronic Component (NAICS = 3344)
    "IPG3344S",  # M Industrial Production: Manufacturing: Durable Goods: Semiconductor and Other Electronic Component (NAICS = 3344)
    # Cryptocurrency data
    "CBBTCUSD",  # ✅ Coinbase Bitcoin (USD)
    "CBETHUSD",  # ✅ Coinbase Ethereum (USD)
]

ACCUMULATING_TARGETS = [
]

SIMPLE_TARGETS = [
    "USREC",
]

INTERPOLATION_TARGETS = [
    "SP500",
    "WM2NS",
    "IPG3344S",
    "A939RX0Q048SBEA",
    "UMCSENT",
    "UNRATE",
    "AITINO",
    "VIXCLS",
    "DTB3",
    "DTWEXAFEGS",
    "OVXCLS",
    "RRPONTSYD",
    "T5YIE",
    "CBBTCUSD",
    "CBETHUSD",
]
