from tunny import set_switch

from fundamental import PricingContext
from turing_models.instruments.eq_option import EqOption
from turing_models.products.equity import TuringOptionTypes
from turing_models.utilities.turing_date import TuringDate

set_switch(1)
# --------------------------------------------------------------------------
# Section 1: Pricing
# --------------------------------------------------------------------------


option = EqOption(option_type=TuringOptionTypes.EUROPEAN_CALL,
                  number_of_options=100,
                  expiration_date=TuringDate(2021, 7, 25),
                  strike_price=500.0,
                  start_averaging_date=TuringDate(2021, 4, 25),
                  value_date=TuringDate(2021, 4, 25),
                  stock_price=510.0,
                  volatility=0.02,
                  interest_rate=0.03,
                  dividend_yield=0.01111)

print(option.price())
print(option.eq_delta())
print(option.eq_gamma())
print(option.eq_vega())
print(option.eq_theta())
print(option.eq_rho())

print("-" * 100)

with PricingContext(interest_rate=0.04):
    print(option.price())
    print(option.eq_delta())
    print(option.eq_gamma())
    print(option.eq_vega())
    print(option.eq_theta())
    print(option.eq_rho())

print("-" * 100)

with PricingContext(interest_rate=0.04):
    print(option.price())
    print(option.eq_delta())
    print(option.eq_gamma())
    print(option.eq_vega())
    print(option.eq_theta())
    print(option.eq_rho())

print("-" * 100)

with PricingContext(interest_rate=0.06):
    print(option.price())
    print(option.eq_delta())
    print(option.eq_gamma())
    print(option.eq_vega())
    print(option.eq_theta())
    print(option.eq_rho())
