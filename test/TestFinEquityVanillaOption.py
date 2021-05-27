import time

import sys
sys.path.append("..")

import numpy as np

from turing_models.utilities.global_types import TuringOptionTypes
from turing_models.products.equity.equity_vanilla_option import TuringEquityVanillaOption
from turing_models.market.curves.discount_curve_flat import TuringDiscountCurveFlat
from turing_models.models.model_black_scholes import TuringModelBlackScholes
from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.error import TuringError

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinEquityVanillaOption():

    valueDate = TuringDate(1, 1, 2015)
    expiryDate = TuringDate(1, 7, 2015)
    stockPrice = 100
    volatility = 0.30
    interestRate = 0.05
    dividendYield = 0.01
    model = TuringModelBlackScholes(volatility)
    discountCurve = TuringDiscountCurveFlat(valueDate, interestRate)
    dividendCurve = TuringDiscountCurveFlat(valueDate, dividendYield)

    numPathsList = [10000, 20000, 40000, 80000, 160000, 320000]

    testCases.header("NUMPATHS", "VALUE_BS", "VALUE_MC", "TIME")

    for numPaths in numPathsList:

        callOption = TuringEquityVanillaOption(
            expiryDate, 100.0, TuringOptionTypes.EUROPEAN_CALL)
        value = callOption.value(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        start = time.time()
        valueMC = callOption.valueMC(valueDate, stockPrice, discountCurve,
                                     dividendCurve, model, numPaths)
        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC, duration)

###############################################################################

    stockPrices = range(80, 120, 10)
    numPaths = 100000

    testCases.header("NUMPATHS", "CALL_VALUE_BS", "CALL_VALUE_MC", 
                     "CALL_VALUE_MC_SOBOL", "TIME")
    useSobol = True

    for stockPrice in stockPrices:

        callOption = TuringEquityVanillaOption(expiryDate, 100.0,
                                               TuringOptionTypes.EUROPEAN_CALL)

        value = callOption.value(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)

        start = time.time()

        useSobol = False
        valueMC1 = callOption.valueMC(valueDate, stockPrice, discountCurve,
                                      dividendCurve, model, numPaths, useSobol)

        useSobol = True
        valueMC2 = callOption.valueMC(valueDate, stockPrice, discountCurve,
                                      dividendCurve, model, numPaths, useSobol)

        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC1, valueMC2, duration)

###############################################################################

    stockPrices = range(80, 120, 10)
    numPaths = 100000

    testCases.header("NUMPATHS", "PUT_VALUE_BS", "PUT_VALUE_MC", 
                     "PUT_VALUE_MC_SOBOL", "TIME")

    for stockPrice in stockPrices:

        putOption = TuringEquityVanillaOption(expiryDate, 100.0,
                                              TuringOptionTypes.EUROPEAN_PUT)

        value = putOption.value(valueDate, stockPrice, discountCurve,
                                dividendCurve, model)

        start = time.time()

        useSobol = False
        valueMC1 = putOption.valueMC(valueDate, stockPrice, discountCurve,
                                      dividendCurve, model, numPaths, useSobol)

        useSobol = True
        valueMC2 = putOption.valueMC(valueDate, stockPrice, discountCurve,
                                      dividendCurve, model, numPaths, useSobol)

        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC1, valueMC2, duration)

###############################################################################

    stockPrices = range(80, 120, 10)

    testCases.header("STOCK PRICE", "CALL_VALUE_BS", "CALL_DELTA_BS", 
                     "CALL_VEGA_BS", "CALL_THETA_BS", "CALL_RHO_BS")

    for stockPrice in stockPrices:

        callOption = TuringEquityVanillaOption(expiryDate, 100.0,
                                               TuringOptionTypes.EUROPEAN_CALL)
        value = callOption.value(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        delta = callOption.delta(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        vega = callOption.vega(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        theta = callOption.theta(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        rho = callOption.rho(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        testCases.print(stockPrice, value, delta, vega, theta, rho)

    ###########################################################################

    testCases.header("STOCK PRICE", "PUT_VALUE_BS", "PUT_DELTA_BS", 
                     "PUT_VEGA_BS", "PUT_THETA_BS", "PUT_RHO_BS")

    for stockPrice in stockPrices:
        
        putOption = TuringEquityVanillaOption(expiryDate, 100.0,
                                              TuringOptionTypes.EUROPEAN_PUT)

        value = putOption.value(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        delta = putOption.delta(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        vega = putOption.vega(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        theta = putOption.theta(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        rho = putOption.rho(valueDate, stockPrice, discountCurve,
                                 dividendCurve, model)
        testCases.print(stockPrice, value, delta, vega, theta, rho)


def testImpliedVolatility_NEW():


    valueDate = TuringDate(1, 1, 2015)
    stockPrice = 100.0
    interestRate = 0.05
    dividendYield = 0.03
    discountCurve = TuringDiscountCurveFlat(valueDate, interestRate)
    dividendCurve = TuringDiscountCurveFlat(valueDate, dividendYield)

    strikes = np.linspace(50, 150, 11)
    timesToExpiry = [0.003, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0]    
    sigmas = np.arange(1, 100, 5) / 100.0
    optionTypes = [TuringOptionTypes.EUROPEAN_CALL, TuringOptionTypes.EUROPEAN_PUT]

    testCases.header("OPT_TYPE", "TEXP", "STOCK_PRICE", "STRIKE", "INTRINSIC",
                     "VALUE", "INPUT_VOL", "IMPLIED_VOL")
    
    tol = 1e-5
    numTests = 0
    numFails = 0
    
    for vol in sigmas:

        model = TuringModelBlackScholes(vol)

        for timeToExpiry in timesToExpiry:     

            expiryDate = valueDate.addYears(timeToExpiry)

            for strike in strikes:

                for optionType in optionTypes:

                    option = TuringEquityVanillaOption(expiryDate, strike,
                                                       optionType)
                
                    value = option.value(valueDate, stockPrice, discountCurve, 
                                         dividendCurve, model)

                    intrinsic = option.intrinsic(valueDate, stockPrice,
                                             discountCurve, dividendCurve)

                    # I remove the cases where the time value is zero
                    # This is arbitrary but 1e-10 seems good enough to me
                    
                    impliedVol = -999

                    if value - intrinsic > 1e-10:

                        impliedVol = option.impliedVolatility(valueDate, 
                                                              stockPrice, 
                                                              discountCurve, 
                                                              dividendCurve, 
                                                              value)
    
                    numTests += 1    
                        
                    errVol = np.abs(impliedVol - vol)
    
                    if errVol > tol:
    
                        testCases.print(optionType, 
                                  timeToExpiry, 
                                  stockPrice,
                                  strike, 
                                  intrinsic,
                                  value, 
                                  vol, 
                                  impliedVol)

                        # These fails include ones due to the zero time value    
                        numFails += 1
                            
                        testCases.print(optionType, timeToExpiry, stockPrice,
                                        strike,
                                        stockPrice, value, vol, impliedVol)

    assert numFails == 694, "Num Fails has changed."

#    print("Num Tests", numTests, "numFails", numFails)

###############################################################################

test_FinEquityVanillaOption()

start = time.time()
testImpliedVolatility_NEW()
end = time.time()
elapsed = end - start

#print("Elapsed:", elapsed)

testCases.compareTestCases()