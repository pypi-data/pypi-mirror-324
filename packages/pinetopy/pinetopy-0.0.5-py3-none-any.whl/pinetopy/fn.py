import ccxt
import pandas as pd
import numpy as np
import ta

def kst(data):
    kst = pd.to_datetime(data, unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul').dt.strftime('%Y-%m-%d %H:%M:%S')
    return kst

def rsi(data, length=14):
    return ta.momentum.RSIIndicator(close=data, window=length).rsi().fillna(0)

def atr(df, length=14):
    _df = df.copy()
    _df['HL'] = _df['high'] - _df['low']  # 고가와 저가의 차이
    _df['HC'] = abs(_df['high'] - _df['close'].shift())  # 고가와 이전 종가의 차이
    _df['LC'] = abs(_df['low'] - _df['close'].shift())  # 저가와 이전 종가의 차이
    
    _df['TR'] = _df[['HL', 'HC', 'LC']].max(axis=1)
    return _df['TR'].ewm(alpha=1/length, adjust=False).mean()

def ema(df, length=9):
    return df.ewm(span=length, adjust=False).mean()

def sma(df, length=9):
    return df.rolling(window=length).mean()

def rma(series, period):
    alpha = 1 / period
    return series.ewm(alpha=alpha, adjust=False).mean()

def dirmov(df, length):
    high, low = df['high'], df['low']
    
    up = high.diff()
    down = -low.diff()

    plusDM = np.where((up > down) & (up > 0), up, 0)
    minusDM = np.where((down > up) & (down > 0), down, 0)
    
    tr = atr(df)

    smoothed_tr = rma(tr, length)
    smoothed_plusDM = rma(pd.Series(plusDM), length)
    smoothed_minusDM = rma(pd.Series(minusDM), length)
    
    plus = 100 * smoothed_plusDM / smoothed_tr
    minus = 100 * smoothed_minusDM / smoothed_tr

    return plus, minus

def adx(df, dilen=14, adxlen=14):

    plus, minus = dirmov(df, dilen)
    sum_dm = plus + minus
    dx = abs(plus - minus) / (sum_dm.replace(0, 1))
    adx = rma(dx, adxlen)
    adx = 100 * adx
    return adx

def line_cross(df, src='close', short_length=9, long_length=21, uptext='up', downtext='down'):
    _df = df.copy()
    _df['short'] = _df[src].rolling(window=short_length).mean()
    _df['long'] = _df[src].rolling(window=long_length).mean()

    return np.where((_df['short'] > _df['long']) & (_df['short'].shift(1) <= _df['long'].shift(1)), uptext,
        np.where((_df['short'] < _df['long']) & (_df['short'].shift(1) >= _df['long'].shift(1)), downtext, ''))

def stoch_rsi(df, src='close', length=14):
    _df = df.copy()
    _df['K'] = ta.momentum.StochRSIIndicator(close=df[src], window=length).stochrsi_k()
    _df['D'] = ta.momentum.StochRSIIndicator(close=df[src], window=length).stochrsi_d()
    _df['K'] = (_df['K'].fillna(0) * 100)
    _df['D'] = (_df['D'].fillna(0) * 100)
    return (_df['K'], _df['D'])

def wma(df, length):
    weights = np.arange(1, length + 1)
    return df.rolling(length).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def hull(df, src='close', length=9):
    wma_half = wma(df[src], int(length / 2))
    wma_full = wma(df[src], length)
    return wma(2 * wma_half - wma_full, int(np.sqrt(length)))

def macd(df, src='close', fast_length=12, slow_length=26, signal_length=9):
    _df = df.copy()
    _df['fast'] = ema(_df[src], length=fast_length)
    _df['slow'] = ema(_df[src], length=slow_length)
    _df['MACD'] = _df['fast'] - _df['slow']
    _df['signal'] = ema(_df['MACD'], length=signal_length)
    _df['histogram'] = _df['MACD'] - _df['signal']
    return _df[['MACD', 'signal', 'histogram']]

def impulse_macd(df, ma=34, signal=9):
    _df = df.copy()
    close = _df['close']
    high = _df['high']
    low = _df['low']

    _df['hlc3'] = (high + low + close) / 3
    _df['hlc3'] = _df['hlc3']
    _df['hi'] = high.ewm(alpha=1/ma, adjust=False).mean()
    _df['lo'] = low.ewm(alpha=1/ma, adjust=False).mean()

    ema1 = _df['hlc3'].ewm(span=ma, adjust=False).mean()
    ema2 = ema1.ewm(span=ma, adjust=False).mean()
    d = ema1 - ema2
    _df['mi'] = ema1 + d

    # Impulse MACD Value
    _df['ImpulseMACD'] = np.where(_df['mi'] > _df['hi'], _df['mi'] - _df['hi'],
                          np.where(_df['mi'] < _df['lo'], _df['mi'] - _df['lo'], 0))

    # Signal Line
    _df['ImpulseMACDSignal'] = _df['ImpulseMACD'].rolling(window=signal).mean()

    # Histogram
    _df['Histo'] = _df['ImpulseMACD'] - _df['ImpulseMACDSignal']

    _df['ImpulseMACD'] = _df['ImpulseMACD'].fillna(0)
    _df['ImpulseMACDSignal'] = _df['ImpulseMACDSignal'].fillna(0)
    _df['Histo'] = _df['Histo'].fillna(0)
    
    return _df[['ImpulseMACD', 'ImpulseMACDSignal', 'Histo']]

def ha_candle(df):
    _df = df.copy()
    _df['HA_Close'] = (_df['open'] + _df['high'] + _df['low'] + _df['close']) / 4
    
    # open
    for i in range(len(_df)):
        if i == 0:
            _df['HA_Open'] = (_df['open'].iloc[0] + _df['close'].iloc[0]) / 2
        else :
            _df.loc[i,'HA_Open'] = (_df['HA_Open'].iloc[i-1] + _df['HA_Close'].iloc[i-1]) / 2
   
    _df['HA_Open'] = _df['HA_Open'] # open
    _df['HA_High'] = _df[['high', 'HA_Open', 'HA_Close']].max(axis=1) # high
    _df['HA_Low'] = _df[['low', 'HA_Open', 'HA_Close']].min(axis=1) # low
    _df['HA_Close'] = _df['HA_Close'] # close
    return _df[['HA_Open','HA_High','HA_Low','HA_Close']]

def bband(df, src='close', length=20, factor=2.0, ddof=0):
    _df = df.copy()
    moving_average = _df[src].rolling(window=length).mean()
    
    std_dev = _df[src].rolling(window=length).std(ddof=ddof) * factor
    upper_band = moving_average + std_dev
    lower_band = moving_average - std_dev

    _df['basis'] = moving_average
    _df['upper'] = upper_band
    _df['lower'] = lower_band
    return _df[['basis','upper','lower']]

def ut_bot_alert(df, src='close', key_value=1, atr_period=10):

    _df = df.copy()
    src = _df[src]
    _df['ATR'] = atr(_df, atr_period)
    _df['nLoss'] = key_value * _df['ATR']
    _df['xATRTrailingStop'] = np.nan

    for i in range(len(_df)):
        prev_stop = _df['xATRTrailingStop'].iloc[i - 1] if i > 0 else 0
        prev_close = src.iloc[i - 1] if i > 0 else 0

        if src.iloc[i] > prev_stop and prev_close > prev_stop:
            _df.loc[i, 'xATRTrailingStop'] = max(prev_stop, src.iloc[i] - _df['nLoss'].iloc[i])
        elif src.iloc[i] < prev_stop and prev_close < prev_stop:
            _df.loc[i, 'xATRTrailingStop'] = min(prev_stop, src.iloc[i] + _df['nLoss'].iloc[i])
        else:
            _df.loc[i, 'xATRTrailingStop'] = (
                src.iloc[i] - _df['nLoss'].iloc[i]
                if src.iloc[i] > prev_stop
                else src.iloc[i] + _df['nLoss'].iloc[i]
            )

    _df['Buy'] = (
        (src > _df['xATRTrailingStop']) &
        (src.shift(1) <= _df['xATRTrailingStop'].shift(1))
    )
    _df['Sell'] = (
        (src < _df['xATRTrailingStop']) &
        (src.shift(1) >= _df['xATRTrailingStop'].shift(1))
    )

    return _df.apply(lambda row: 'Buy' if row['Buy'] else ('Sell' if row['Sell'] else ''), axis=1)

def ema_trend_meter(df, src='close', base=1, ema1=7, ema2=14, ema3=21):
    _df = df.copy()
    _df[f"EMA0"] = df[src].ewm(span=base, adjust=False).mean()
    _df[f"EMA1"] = df[src].ewm(span=ema1, adjust=False).mean()
    _df[f"EMA2"] = df[src].ewm(span=ema2, adjust=False).mean()
    _df[f"EMA3"] = df[src].ewm(span=ema3, adjust=False).mean()

    _df['Bull1'] = _df['EMA1'] < _df['EMA0']
    _df['Bull2'] = _df['EMA2'] < _df['EMA0']
    _df['Bull3'] = _df['EMA3'] < _df['EMA0']

    return _df[['Bull1','Bull2','Bull3']]

def williams_r(df, length=14):
    _df = df.copy()
    highest_high = _df['high'].rolling(window=length).max()
    lowest_low = _df['low'].rolling(window=length).min()
    _df['R'] = 100 * (_df['close'] - highest_high) / (highest_high - lowest_low)
    return _df['R']

def dc(df, length=20):
    _df = df.copy()
    _df['upper'] = _df['high'].rolling(window=length).max()
    _df['lower'] = _df['low'].rolling(window=length).min()
    _df['basis'] = ((_df['upper'] + _df['lower']) / 2)

    return _df[['basis','upper','lower']]

def mfi(df, length=14):
    _df = df.copy()
    _df['hlc3'] = (_df['high'] + _df['low'] + _df['close']) / 3
    delta = _df['hlc3'].diff()

    upper = (_df['volume'] * np.where(delta > 0, _df['hlc3'], 0)).rolling(window=length).sum()
    lower = (_df['volume'] * np.where(delta < 0, _df['hlc3'], 0)).rolling(window=length).sum()

    _df['MFI'] = 100.0 - (100.0 / (1.0 + (upper / lower)))
    return _df['MFI']

def hull(df, src='close', length=9):
    _df = df.copy()
    wma_half = wma(_df[src], int(length / 2))
    wma_full = wma(_df[src], length)
    _df['hull'] = wma(2 * wma_half - wma_full, int(np.sqrt(length)))
    return _df['hull']

def ema_trend_meter(df, src='close', base=1, ema1=7, ema2=14, ema3=21):

    _df = df.copy()
    _df[f"EMA0"] = df[src].ewm(span=base, adjust=False).mean()
    _df[f"EMA1"] = df[src].ewm(span=ema1, adjust=False).mean()
    _df[f"EMA2"] = df[src].ewm(span=ema2, adjust=False).mean()
    _df[f"EMA3"] = df[src].ewm(span=ema3, adjust=False).mean()

    _df['Bull1'] = _df['EMA1'] < _df['EMA0']
    _df['Bull2'] = _df['EMA2'] < _df['EMA0']
    _df['Bull3'] = _df['EMA3'] < _df['EMA0']
    _df['etm_signal'] = _df.apply(lambda row: 'LONG' if row['Bull1'] and row['Bull2'] and row['Bull3'] else ('SHORT' if not row['Bull1'] and not row['Bull2'] and not row['Bull3'] else ''), axis=1)

    return _df[['Bull1','Bull2','Bull3', 'etm_signal']]

def psar(df, step=0.02, max_step=0.2):
    _df = df.copy()
    sar = ta.trend.PSARIndicator(high=_df['high'], low=_df['low'], close=_df['close'], step=step, max_step=max_step).psar()
    _df['PSAR'] = sar
    _df['PSAR_TREND'] = np.where(_df['close'] > _df['PSAR'], 'LONG', np.where(_df['close'] < _df['PSAR'], 'SHORT', 'FLAT'))
    return _df[['PSAR', 'PSAR_TREND']]

def ichimoku(df, conversion=9, base=26, spanb=52):
    _df = df.copy()
    data = ta.trend.IchimokuIndicator(high=_df['high'], low=_df['low'], window1=conversion, window2=base, window3=spanb)
    _df['conversion_line'] = data.ichimoku_conversion_line()
    _df['base_line'] = data.ichimoku_base_line()
    _df['lag'] = _df['close']
    _df['spanA'] = data.ichimoku_a()
    _df['spanB'] = data.ichimoku_b()
    return _df[['conversion_line','base_line', 'lag', 'spanA', 'spanB']]

def trix(df, len=18):
    _df = df.copy()
    close = np.log(_df['close'])
    ema1 = ema(close, len)
    ema2 = ema(ema1, len)
    ema3 = ema(ema2, len)
    _df['TRIX'] = (10000 * np.diff(ema3, prepend=ema3[0]))
    return _df['TRIX']

def ultimate_oscillator(df, fast=7, middle=14, slow=28):
    _df = df.copy()
    uo = ta.momentum.ultimate_oscillator(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window1=fast, 
        window2=middle, 
        window3=slow
    )
    _df['UO'] = uo
    return _df['UO']

def rate_of_change(df, src='close', len=9):
    _df = df.copy()
    close = df[src]
    roc = (close - close.shift(len)) / close.shift(len)
    _df['ROC'] = (roc * 100)
    return _df['ROC']

def aroon(df, len=14):
    _df = df.copy()
    data = ta.trend.AroonIndicator(high=_df['high'], low=_df['low'], window=len)
    _df['aroon_up'] = data.aroon_up()
    _df['aroon_down'] = data.aroon_down()
    return _df[['aroon_up', 'aroon_down']]

def mass_index(df, len=10):
    _df = df.copy()
    data = ta.trend.MassIndex(high=_df['high'], low=_df['low'], window_slow=len)
    _df['MASS'] = data.mass_index()
    return _df['MASS']

def ppo(df, fast=12, slow=26, signal=9):
    _df = df.copy()
    data = ta.momentum.PercentagePriceOscillator(
        close=_df['close'], 
        window_fast=fast, 
        window_slow=slow, 
        window_sign=signal
    )
    _df['ppo_histo'] = data.ppo_hist()
    _df['ppo'] = data.ppo()
    _df['ppo_signal'] = data.ppo_signal()
    return _df[['ppo_histo', 'ppo', 'ppo_signal']]

def awesome_oscillator(df, len1=5, len2=34):
    _df = df.copy()
    hl2 = (_df['high'] + _df['low']) / 2
    _df['AO'] = (sma(hl2,len1) - sma(hl2,len2))
    _df['AO_TREND'] = np.where(_df['AO'].diff() <= 0, 'down', 'up')
    return _df[['AO', 'AO_TREND']]

def kc(df, len=20, mult=2):
    _df = df.copy()
    data = ta.volatility.KeltnerChannel(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window=len,
        multiplier=mult,
        original_version=False
    )
    _df['KC_H'] = data.keltner_channel_hband()
    _df['KC_M'] = data.keltner_channel_mband()
    _df['KC_L'] = data.keltner_channel_lband()
    return _df[['KC_H', 'KC_M', 'KC_L']]

def know_sure_thing(df):
    _df = df.copy()
    data = ta.trend.KSTIndicator(close=_df['close'])
    _df['KST'] = data.kst()
    _df['KST_SIGNAL'] = data.kst_sig()
    return _df[['KST', 'KST_SIGNAL']]

def tsi(df, src='close', slow=25, fast=13):
    _df = df.copy()
    data = ta.momentum.TSIIndicator(
        close=_df[src], 
        window_slow=slow, 
        window_fast=fast
    )
    _df['TSI'] = data.tsi()
    _df['TSI_SIGNAL'] = ema(df=_df['TSI'], length=fast)
    return _df[['TSI', 'TSI_SIGNAL']]

def cci(df, len=20, sma_len=14):
    _df = df.copy()
    _df['CCI'] = ta.trend.cci(high=_df['high'], low=_df['low'], close=_df['close'], window=len)
    _df['CCI_SIGNAL'] = sma(df=_df['CCI'], length=sma_len)
    return _df[['CCI', 'CCI_SIGNAL']]

def vortex(df, len=14):
    _df = df.copy()
    data = ta.trend.VortexIndicator(
        high=_df['high'], 
        low=_df['low'], 
        close=_df['close'], 
        window=len
    )
    _df['VI_P'] = data.vortex_indicator_pos()
    _df['VI_M'] = data.vortex_indicator_neg()
    return _df[['VI_P', 'VI_M']]