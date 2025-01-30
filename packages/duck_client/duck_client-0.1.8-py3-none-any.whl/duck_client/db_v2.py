import duckdb
from typing import Literal
from urllib.parse import urljoin
from tqdm import tqdm
from duck_client.error import DBReadOnlyError, DBError


class DataBase:
    FREQ_MAP = {
        "1m": 1,
        "3m": 3,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "12h": 720,
        "1d": 1440,
    }

    ASSET_CLASS_MAP = {
        "spot": "spot",
        "um": "futures/um",
        # "cm": "/futures/cm", #NOTE: not supported yet
    }

    MOMENTUM_WINDOW_MAP = {
        "1d": 7,
        "12h": 6,
        "4h": 6,
        "1h": 4,
        "30m": 4,
        "15m": 4,
        "3m": 5,
        "1m": 5,
    }

    VOLATILITY_WINDOW_MAP = {
        "1d": 14,
        "12h": 14,
        "4h": 18,
        "1h": 24,
        "30m": 12,
        "15m": 16,
        "3m": 20,
        "1m": 30,
    }

    BETA_WINDOW_MAP = {
        "1d": 90,
        "12h": 180,
        "4h": 180,
        "1h": 720,
        "30m": 1440,
        "15m": 2880,
        "3m": 7 * 24 * 20,
        "1m": 7 * 24 * 60,
    }

    def __init__(
        self,
        cache_path: str | None = None,
        db_path: str | None = None,
        read_only: bool = True,
    ):
        self._db_path = db_path
        self._cache_path = cache_path
        self._read_only = read_only
        if db_path:
            self.conn = duckdb.connect(database=db_path, read_only=read_only)
        else:
            self.conn = duckdb.connect()

    def _read_only_check(self):
        if self._read_only:
            raise DBReadOnlyError(
                "Cannot create table in `read-only` mode, please set `read_only=False`"
            )

    def _asset_class_check(self, asset_class: Literal["spot", "um"]):
        if asset_class not in self.ASSET_CLASS_MAP:
            raise DBError(
                f"Invalid asset class: {asset_class}. Must be one of: {', '.join(self.ASSET_CLASS_MAP.keys())}"
            )

    def _freq_check(
        self, freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"]
    ):
        if freq not in self.FREQ_MAP:
            raise DBError(
                f"Invalid frequency: {freq}. Must be one of: {', '.join(self.FREQ_MAP.keys())}"
            )

    def _create_klines_table(
        self,
        asset_class: Literal["spot", "um"],
        freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"],
    ):
        self._read_only_check()
        self._asset_class_check(asset_class)
        self._freq_check(freq)
        path = urljoin(self._cache_path, self.ASSET_CLASS_MAP[asset_class])
        if freq == "1m":
            sql = f"""
            CREATE OR REPLACE TABLE binance_{asset_class}_klines_{freq} AS
            SELECT DISTINCT
                SPLIT_PART(filename, '/', -3) as symbol,
                timestamp,
                open,
                high,
                low,
                close,
                volume,
                quote_volume,
                taker_buy_volume,
                taker_buy_quote_volume
            FROM read_parquet(
                '{path}/*/klines/*/1m/*.parquet',
                FILENAME = true
            )
            """
        else:
            sql = f"""
            CREATE OR REPLACE TABLE binance_{asset_class}_klines_{freq} AS
            SELECT DISTINCT
                SPLIT_PART(filename, '/', -3) as symbol,
                time_bucket(INTERVAL {self.FREQ_MAP[freq]} minutes, to_timestamp(timestamp / 1000)) as timestamp,
                FIRST(open) as open,
                MAX(high) as high,
                MIN(low) as low,
                LAST(close) as close,
                SUM(volume) as volume,
                SUM(quote_volume) as quote_volume,
                SUM(taker_buy_volume) as taker_buy_volume,
                SUM(taker_buy_quote_volume) as taker_buy_quote_volume
            FROM read_parquet(
                '{path}/*/klines/*/1m/*.parquet',
                FILENAME = true
            )
            GROUP BY symbol, time_bucket(INTERVAL {self.FREQ_MAP[freq]} minutes, to_timestamp(timestamp / 1000))
            """
        self.conn.execute(sql)

    def _create_factors_table(
        self,
        asset_class: Literal["spot", "um"],
        freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"],
    ):
        self._read_only_check()
        self._asset_class_check(asset_class)
        self._freq_check(freq)

        m_window = self.MOMENTUM_WINDOW_MAP[freq]
        v_window = self.VOLATILITY_WINDOW_MAP[freq]
        b_window = self.BETA_WINDOW_MAP[freq]

        sql = f"""
        CREATE OR REPLACE TABLE binance_{asset_class}_factors_{freq} AS
        WITH base_table AS (
            SELECT DISTINCT
                a.symbol,
                a.timestamp,
                a.close,
                a.return,
                b.return AS btc_return
            FROM (
                SELECT DISTINCT
                    symbol,
                    timestamp,
                    close,
                    close / LAG(close) OVER (PARTITION BY symbol ORDER BY timestamp) - 1 AS return
                FROM binance_{asset_class}_klines_{freq}
            ) a
            LEFT JOIN (
                SELECT 
                    timestamp,
                    close / LAG(close) OVER (ORDER BY timestamp) - 1 AS return
                FROM binance_{asset_class}_klines_{freq}
                WHERE symbol = 'BTCUSDT'
            ) b ON a.timestamp = b.timestamp
        ),
        momentum_table AS (
            SELECT 
                *,
                CASE 
                    WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) >= {m_window} 
                    THEN PRODUCT(1 + return) OVER (PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN {m_window - 1} PRECEDING AND CURRENT ROW) - 1 
                    ELSE NULL 
                END AS momentum
            FROM base_table
        ),
        vol_table AS (
            SELECT 
                *,
                CASE 
                    WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) >= {v_window} 
                    THEN STDDEV(return) OVER (PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN {v_window - 1} PRECEDING AND CURRENT ROW) 
                    ELSE NULL 
                END AS volatility
            FROM momentum_table
        ),
        beta_table AS (
            SELECT 
                *,
                CASE 
                    WHEN ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) >= {b_window} 
                    THEN REGR_SLOPE(btc_return, return) OVER (PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN {b_window - 1} PRECEDING AND CURRENT ROW) 
                    ELSE NULL 
                END AS beta
            FROM vol_table
        )

        SELECT 
            timestamp,
            symbol,
            close,
            return,
            momentum,
            volatility,
            beta
        FROM beta_table;
        """

        self.conn.execute(sql)

    def update_klines(self):
        for asset_class in tqdm(self.ASSET_CLASS_MAP):
            for freq in tqdm(self.FREQ_MAP, leave=False):
                try:
                    self._create_klines_table(asset_class, freq)
                except Exception as e:
                    print(f"Error creating klines table for {asset_class} {freq}: {e}")

    def update_factors(self):
        for asset_class in tqdm(self.ASSET_CLASS_MAP):
            for freq in tqdm(self.FREQ_MAP, leave=False):
                try:
                    self._create_factors_table(asset_class, freq)
                except Exception as e:
                    print(f"Error creating factors table for {asset_class} {freq}: {e}")

    def df_factors(
        self,
        symbols: list[str] | None = None,
        freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"] = "1m",
        asset_class: Literal["spot", "um"] = "um",
        start_date: str | None = None,
        end_date: str | None = None,
        order_by_timestamp: bool = False,
    ):
        self._asset_class_check(asset_class)
        self._freq_check(freq)

        sql = f"""
        SELECT * FROM binance_{asset_class}_factors_{freq}
        WHERE 1=1
        {f"AND symbol IN ({','.join([f''''{s}' ''' for s in symbols])})" if symbols else ""}
        {f"AND timestamp >= TIMESTAMP '{start_date}'" if start_date else ""}
        {f"AND timestamp < TIMESTAMP '{end_date}'" if end_date else ""}
        """
        if order_by_timestamp:
            sql += "ORDER BY timestamp"
        return self.conn.query(sql).to_df()

    def df_klines(
        self,
        symbols: list[str] | None = None,
        freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"] = "1m",
        asset_class: Literal["spot", "um"] = "um",
        start_date: str | None = None,
        end_date: str | None = None,
        order_by_timestamp: bool = False,
    ):
        self._asset_class_check(asset_class)
        self._freq_check(freq)

        sql = f"""
        SELECT * FROM binance_{asset_class}_klines_{freq}
        WHERE 1=1
        {f"AND symbol IN ({','.join([f''''{s}' ''' for s in symbols])})" if symbols else ""}
        {f"AND timestamp >= TIMESTAMP '{start_date}'" if start_date else ""}
        {f"AND timestamp < TIMESTAMP '{end_date}'" if end_date else ""}
        """
        if order_by_timestamp:
            sql += "ORDER BY timestamp"
        return self.conn.query(sql).to_df()
    
    def factors_matrix(self, symbols: list[str] | None = None, factor: Literal["return", "momentum", "volatility", "beta"] = "return", freq: Literal["1m", "3m", "15m", "30m", "1h", "4h", "12h", "1d"] = "1m", asset_class: Literal["spot", "um"] = "um", start_date: str | None = None, end_date: str | None = None):
        self._asset_class_check(asset_class)
        self._freq_check(freq)
        
        sql = f"""
        WITH filtered_factors AS (
            SELECT timestamp, symbol, {factor}
            FROM binance_{asset_class}_factors_{freq}
            WHERE 1=1
            {f"AND symbol IN ({','.join([f''''{s}' ''' for s in symbols])})" if symbols else ''}
            {f"AND timestamp >= TIMESTAMP '{start_date}'" if start_date else ''}
            {f"AND timestamp < TIMESTAMP '{end_date}'" if end_date else ''}
        )
        PIVOT filtered_factors ON symbol USING min({factor})
        ORDER BY timestamp
        """
        
        return self.conn.query(sql).to_df()
