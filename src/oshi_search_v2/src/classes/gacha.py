import random


def is_ssr():
    SSR_EMISSION_RATE = 0.0003
    return random.random() <= SSR_EMISSION_RATE
