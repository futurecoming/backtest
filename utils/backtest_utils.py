import numpy as np
import pandas as pd


def create_sharpe_ratio(returns, periods=252):
    """夏普比率
    """
    if np.std(returns) == 0:
        return 0.
    else:
        return np.sqrt(periods) * np.mean(returns) / np.std(returns)


def create_drawdowns(equity_curve):
    """最大回撤
    """
    hwm = [0]
    eq_idx = equity_curve.index
    drawdown = pd.Series(index=eq_idx)
    duration = pd.Series(index=eq_idx)

    for t in range(1, len(eq_idx)):
        cur_hwm = max(hwm[t - 1], equity_curve[t])
        hwm.append(cur_hwm)
        drawdown[t] = hwm[t] - equity_curve[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t - 1] + 1

    return drawdown.max(), duration.max()


def create_annualized_return(equity_curve):
    """年化收益
    """
    periods = len(equity_curve)
    total_return = equity_curve['equity_curve'][-1]
    annualized_return = (total_return - 1.0) / periods * 365 * 100.0
    return annualized_return
