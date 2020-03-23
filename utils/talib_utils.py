import talib
import numpy as np


class TalibHelper:
    # 简单移动平均
    @staticmethod
    def cal_ma(close, period):
        return talib.MA(np.array(close), timeperiod=period)

    # 指数移动平均
    @staticmethod
    def cal_ema(close, peroid):
        return talib.EMA(np.array(close), timeperiod=peroid)

    # MACD
    @staticmethod
    def cal_macd(close, fast=6, slow=12, signal=9):
        macd, signal, hist = talib.MACD(np.array(close), fastperiod=fast, slowperiod=slow, signalperiod=signal)
        return macd, signal, hist

    # RSI
    @staticmethod
    def cal_rsi(close, period):
        return talib.RSI(np.array(close), timeperiod=period)


if __name__ == '__main__':
    pass
