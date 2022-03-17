#!/usr/local/bin/python3

# -*-coding:utf-8-*-

# @Author: hugheslou
# @Time: 2018/7/15 20:39

import sys
import tushare as ts
import pandas as pd

print(sys.version)

print(ts.__version__)


def buy(capital, price):
    share = capital * (1 - fee) // (price * per_share)
    capital = capital - round(share * price * per_share * (1 + fee), 2)
    return capital, share


def sell(share, price):
    return share * per_share * price * (1 - fee)


def _random(n=13):
    from random import randint
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(randint(start, end))


init_principal = 1_000_000
fee = 0.0003
min_fee = 5
# 美的、格力差价在5%以内时，美的；大于15%时，格力
low = 0.05 * 100
high = 0.15 * 100

per_share = 100

midea = pd.DataFrame(ts.get_k_data('000333', '2018-01-01', ktype='5'))
gree = pd.DataFrame(ts.get_k_data('000651', '2018-01-01', ktype='5'))

# print(ts.get_k_data('000001', index=True, ktype='5'))
print(_random(16))
print(midea.size)
print(midea.index)
# print(midea.columns)

print(gree.size)
print(gree.index)
# print(gree.columns)

buy_str = 'use {:.2f} to buy {} share {} at {} with price {:.2f} percentage {:.4f}%, left {:.2f}'
sell_str = 'sell {} share {} at {} with price {:.2f} percentage {:.4f}% get {:.2f}, total {:.2f}'

volume = 0
hold_gree = False
principal = init_principal
g_price = 0
m_price = 0

for i in midea.index:
    # 先假定T+0交易
    date = midea.loc[i].values[0]
    m_price = midea.loc[i].values[1]
    g_price = gree.loc[i].values[1]
    d_percentage = (m_price / g_price - 1) * 100

    # 确定初始交易
    if i == 0:
        # 优先midea
        # if d_percentage >= high:
        #     trans, volume = buy(principal, g_price)
        #     hold_gree = True
        #     print(buy_str.format(principal, volume, 'gree', date, g_price, d_percentage, trans))
        #     principal = trans
        # else:
        #     trans, volume = buy(principal, m_price)
        #     print(buy_str.format(principal, volume, 'midea', date, m_price, d_percentage, trans))
        #     principal = trans

        # 优先gree
        if d_percentage <= low:
            trans, volume = buy(principal, m_price)
            print(buy_str.format(principal, volume, 'midea', date, m_price, d_percentage, trans))
            principal = trans
        else:
            trans, volume = buy(principal, g_price)
            hold_gree = True
            print(buy_str.format(principal, volume, 'gree', date, g_price, d_percentage, trans))
            principal = trans
    else:
        if d_percentage <= low:
            if hold_gree:
                trans = sell(volume, g_price)
                principal = principal + trans
                print(sell_str.format(volume, 'gree', date, g_price, d_percentage, trans, principal))
                trans, volume = buy(principal, m_price)
                print(buy_str.format(principal, volume, 'midea', date, m_price, d_percentage, trans))
                principal = trans
                hold_gree = False
        elif d_percentage >= high:
            if not hold_gree:
                trans = sell(volume, m_price)
                principal = principal + trans
                print(sell_str.format(volume, 'midea', date, m_price, d_percentage, trans, principal))
                trans, volume = buy(principal, g_price)
                print(buy_str.format(principal, volume, 'gree', date, g_price, d_percentage, trans))
                principal = trans
                hold_gree = True
        else:
            pass

position = principal + volume * per_share * (g_price if hold_gree else m_price)

print('media price {:.2f}, gree price {:.2f}'.format(m_price, g_price))
print('principal {:.2f}'.format(principal))
print('share {}'.format(volume))
print('gree' if hold_gree else 'midea')
print('position {:.2f}'.format(position))
print('profit {:.2f}%'.format((position / init_principal - 1) * 100))

# print(midea)

# print(gree)

# print(type(midea))
