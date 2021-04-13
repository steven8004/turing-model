###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################


import time
import numpy as np

import sys
sys.path.append("..")

from financepy.turingutils.turing_global_types import TuringCapFloorTypes
from financepy.products.rates.turing_ibor_cap_floor import FinIborCapFloor
from financepy.products.rates.turing_ibor_swap import FinIborSwap
from financepy.products.rates.turing_ibor_swap import TuringSwapTypes
from financepy.products.rates.turing_ibor_deposit import TuringIborDeposit
from financepy.products.rates.turing_ibor_single_curve import TuringIborSingleCurve

from financepy.turingutils.turing_frequency import TuringFrequencyTypes
from financepy.turingutils.turing_day_count import TuringDayCountTypes
from financepy.turingutils.turing_date import TuringDate

from financepy.turingutils.turing_calendar import TuringCalendarTypes
from financepy.turingutils.turing_calendar import TuringBusDayAdjustTypes
from financepy.turingutils.turing_calendar import TuringDateGenRuleTypes

from financepy.turingutils.turing_global_types import TuringSwapTypes

from financepy.market.curves.turing_discount_curve_zeros import TuringDiscountCurveZeros
from financepy.market.curves.turing_interpolator import FinInterpTypes
from financepy.market.curves.turing_discount_curve_flat import TuringDiscountCurveFlat

from financepy.models.turing_model_black import FinModelBlack
from financepy.models.turing_model_bachelier import FinModelBachelier
from financepy.models.turing_model_black_shifted import TuringModelBlackShifted
from financepy.models.turing_model_sabr import FinModelSABR
from financepy.models.turing_model_sabr_shifted import TuringModelSABRShifted
from financepy.models.turing_model_rates_hw import FinModelRatesHW

from financepy.turingutils.turing_global_variables import gDaysInYear

from financepy.market.volatility.turing_ibor_cap_vol_curve import TuringIborCapVolCurve
from financepy.turingutils.turing_schedule import TuringSchedule

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

##############################################################################

def test_FinIborDepositsAndSwaps(valuationDate):

    depoBasis = TuringDayCountTypes.THIRTY_E_360_ISDA
    depos = []

    spotDays = 0
    settlementDate = valuationDate.addWeekDays(spotDays)
    depositRate = 0.05

    depo1 = TuringIborDeposit(settlementDate, "1M", depositRate, depoBasis)
    depo2 = TuringIborDeposit(settlementDate, "3M", depositRate, depoBasis)
    depo3 = TuringIborDeposit(settlementDate, "6M", depositRate, depoBasis)

    depos.append(depo1)
    depos.append(depo2)
    depos.append(depo3)

    fras = []

    swaps = []
    fixedBasis = TuringDayCountTypes.ACT_365F
    fixedFreq = TuringFrequencyTypes.SEMI_ANNUAL
    fixedLegType = TuringSwapTypes.PAY

    swapRate = 0.05
    swap1 = FinIborSwap(settlementDate, "1Y", fixedLegType, swapRate, fixedFreq, fixedBasis)
    swap2 = FinIborSwap(settlementDate, "3Y", fixedLegType, swapRate, fixedFreq, fixedBasis)
    swap3 = FinIborSwap(settlementDate, "5Y", fixedLegType, swapRate, fixedFreq, fixedBasis)

    swaps.append(swap1)
    swaps.append(swap2)
    swaps.append(swap3)

    liborCurve = TuringIborSingleCurve(valuationDate, depos, fras, swaps)

    return liborCurve

##########################################################################


def test_FinIborCapFloor():

    todayDate = TuringDate(20, 6, 2019)
    valuationDate = todayDate
    startDate = todayDate.addWeekDays(2)
    maturityDate = startDate.addTenor("1Y")
    liborCurve = test_FinIborDepositsAndSwaps(todayDate)

    # The capfloor has begun
    # lastFixing = 0.028

    ##########################################################################
    # COMPARISON OF MODELS
    ##########################################################################

    strikes = np.linspace(0.02, 0.08, 5)

    testCases.header("LABEL", "STRIKE", "BLK", "BLK_SHFTD", "SABR",
                     "SABR_SHFTD", "HW", "BACH")

    model1 = FinModelBlack(0.20)
    model2 = TuringModelBlackShifted(0.25, 0.0)
    model3 = FinModelSABR(0.013, 0.5, 0.5, 0.5)
    model4 = TuringModelSABRShifted(0.013, 0.5, 0.5, 0.5, -0.008)
    model5 = FinModelRatesHW(0.30, 0.01)
    model6 = FinModelBachelier(0.01)

    for k in strikes:
        capFloorType = TuringCapFloorTypes.CAP
        capfloor = FinIborCapFloor(startDate, maturityDate, capFloorType, k)
        cvalue1 = capfloor.value(valuationDate, liborCurve, model1)
        cvalue2 = capfloor.value(valuationDate, liborCurve, model2)
        cvalue3 = capfloor.value(valuationDate, liborCurve, model3)
        cvalue4 = capfloor.value(valuationDate, liborCurve, model4)
        cvalue5 = capfloor.value(valuationDate, liborCurve, model5)
        cvalue6 = capfloor.value(valuationDate, liborCurve, model6)
        testCases.print("CAP", k, cvalue1, cvalue2, cvalue3, cvalue4, cvalue5, cvalue6)

    testCases.header("LABEL", "STRIKE", "BLK", "BLK_SHFTD", "SABR",
                     "SABR_SHFTD", "HW", "BACH")

    for k in strikes:
        capFloorType = TuringCapFloorTypes.FLOOR
        capfloor = FinIborCapFloor(startDate, maturityDate, capFloorType, k)
        fvalue1 = capfloor.value(valuationDate, liborCurve, model1)
        fvalue2 = capfloor.value(valuationDate, liborCurve, model2)
        fvalue3 = capfloor.value(valuationDate, liborCurve, model3)
        fvalue4 = capfloor.value(valuationDate, liborCurve, model4)
        fvalue5 = capfloor.value(valuationDate, liborCurve, model5)
        fvalue6 = capfloor.value(valuationDate, liborCurve, model6)
        testCases.print("FLR", k, fvalue1, fvalue2, fvalue3, fvalue4, fvalue5, fvalue6)

###############################################################################
# PUT CALL CHECK
###############################################################################

    testCases.header("LABEL", "STRIKE", "BLK", "BLK_SHFTD", "SABR",
                     "SABR SHFTD", "HW", "BACH")

    for k in strikes:
        capFloorType = TuringCapFloorTypes.CAP
        capfloor = FinIborCapFloor(startDate, maturityDate, capFloorType, k)
        cvalue1 = capfloor.value(valuationDate, liborCurve, model1)
        cvalue2 = capfloor.value(valuationDate, liborCurve, model2)
        cvalue3 = capfloor.value(valuationDate, liborCurve, model3)
        cvalue4 = capfloor.value(valuationDate, liborCurve, model4)
        cvalue5 = capfloor.value(valuationDate, liborCurve, model5)
        cvalue6 = capfloor.value(valuationDate, liborCurve, model6)

        capFloorType = TuringCapFloorTypes.FLOOR
        capfloor = FinIborCapFloor(startDate, maturityDate, capFloorType, k)
        fvalue1 = capfloor.value(valuationDate, liborCurve, model1)
        fvalue2 = capfloor.value(valuationDate, liborCurve, model2)
        fvalue3 = capfloor.value(valuationDate, liborCurve, model3)
        fvalue4 = capfloor.value(valuationDate, liborCurve, model4)
        fvalue5 = capfloor.value(valuationDate, liborCurve, model5)
        fvalue6 = capfloor.value(valuationDate, liborCurve, model6)

        pcvalue1 = cvalue1 - fvalue1
        pcvalue2 = cvalue2 - fvalue2
        pcvalue3 = cvalue3 - fvalue3
        pcvalue4 = cvalue4 - fvalue4
        pcvalue5 = cvalue5 - fvalue5
        pcvalue6 = cvalue6 - fvalue6

        testCases.print("PUT_CALL", k, pcvalue1, pcvalue2, pcvalue3,
                        pcvalue4, pcvalue5, pcvalue6)

###############################################################################


def test_FinIborCapFloorVolCurve():
    ''' Aim here is to price cap and caplets using cap and caplet vols and to
    demonstrate they are the same - NOT SURE THAT HULLS BOOKS FORMULA WORKS FOR
    OPTIONS. '''

    todayDate = TuringDate(20, 6, 2019)
    valuationDate = todayDate
    maturityDate = valuationDate.addTenor("3Y")
    dayCountType = TuringDayCountTypes.THIRTY_E_360
    frequency = TuringFrequencyTypes.ANNUAL

    k = 0.04
    capFloorType = TuringCapFloorTypes.CAP
    capFloor = FinIborCapFloor(valuationDate,
                                maturityDate,
                                capFloorType,
                                k,
                                None,
                                frequency,
                                dayCountType)

    capVolDates = TuringSchedule(valuationDate,
                                 valuationDate.addTenor("10Y"),
                                 frequency)._generate()

    flatRate = 0.04
    liborCurve = TuringDiscountCurveFlat(valuationDate,
                                         flatRate,
                                         frequency,
                                         dayCountType)

    flat = False
    if flat is True:
        capVolatilities = [20.0] * 11
        capVolatilities[0] = 0.0
    else:
        capVolatilities = [0.00, 15.50, 18.25, 17.91, 17.74, 17.27,
                           16.79, 16.30, 16.01, 15.76, 15.54]

    capVolatilities = np.array(capVolatilities)/100.0
    capVolatilities[0] = 0.0

    volCurve = TuringIborCapVolCurve(valuationDate,
                                     capVolDates,
                                     capVolatilities,
                                     dayCountType)

#    print(volCurve._capletGammas)

    # Value cap using a single flat cap volatility
    tcap = (maturityDate - valuationDate) / gDaysInYear
    vol = volCurve.capVol(maturityDate)
    model = FinModelBlack(vol)
    valueCap = capFloor.value(valuationDate, liborCurve, model)
#    print("CAP T", tcap, "VOL:", vol, "VALUE OF CAP:", valueCap)

    # Value cap by breaking it down into caplets using caplet vols
    vCaplets = 0.0
    capletStartDate = capFloor._capFloorLetDates[1]
    testCases.header("START", "END", "VOL", "VALUE")

    for capletEndDate in capFloor._capFloorLetDates[2:]:
        vol = volCurve.capletVol(capletEndDate)
        modelCaplet = FinModelBlack(vol)
        vCaplet = capFloor.valueCapletFloorLet(valuationDate,
                                               capletStartDate,
                                               capletEndDate,
                                               liborCurve,
                                               modelCaplet)

        vCaplets += vCaplet
        testCases.print("%12s" % capletStartDate,
                        "%s" % capletEndDate,
                        "%9.5f" % (vol*100.0),
                        "%9.5f" % vCaplet)

        capletStartDate = capletEndDate

    testCases.header("LABEL", "VALUE")
    testCases.print("CAPLETS->CAP: ", vCaplets)

###############################################################################


def test_FinIborCapletHull():

    #  Hull Page 703, example 29.3
    todayDate = TuringDate(20, 6, 2019)
    valuationDate = todayDate
    maturityDate = valuationDate.addTenor("2Y")
    liborCurve = TuringDiscountCurveFlat(valuationDate,
                                         0.070,
                                         TuringFrequencyTypes.QUARTERLY,
                                         TuringDayCountTypes.THIRTY_E_360)

    k = 0.08
    capFloorType = TuringCapFloorTypes.CAP
    capFloor = FinIborCapFloor(valuationDate,
                               maturityDate,
                               capFloorType,
                               k,
                               None,
                               TuringFrequencyTypes.QUARTERLY,
                               TuringDayCountTypes.THIRTY_E_360)

    # Value cap using a single flat cap volatility
    model = FinModelBlack(0.20)
    capFloor.value(valuationDate, liborCurve, model)

    # Value cap by breaking it down into caplets using caplet vols
    capletStartDate = valuationDate.addTenor("1Y")
    capletEndDate = capletStartDate.addTenor("3M")

    vCaplet = capFloor.valueCapletFloorLet(valuationDate,
                                           capletStartDate,
                                           capletEndDate,
                                           liborCurve,
                                           model)

    # Cannot match Hull due to dates being adjusted
    testCases.header("CORRECT PRICE", "MODEL_PRICE")
    testCases.print(517.29, vCaplet)

###############################################################################


def test_FinIborCapFloorQLExample():

    valuationDate = TuringDate(14, 6, 2016)

    dates = [TuringDate(14, 6, 2016), TuringDate(14, 9, 2016),
             TuringDate(14, 12, 2016), TuringDate(14, 6, 2017),
             TuringDate(14, 6, 2019), TuringDate(14, 6, 2021),
             TuringDate(15, 6, 2026), TuringDate(16, 6, 2031),
             TuringDate(16, 6, 2036), TuringDate(14, 6, 2046)]

    rates = [0.000000, 0.006616, 0.007049, 0.007795,
             0.009599, 0.011203, 0.015068, 0.017583,
             0.018998, 0.020080]

    freqType = TuringFrequencyTypes.ANNUAL
    dayCountType = TuringDayCountTypes.ACT_ACT_ISDA

    discountCurve = TuringDiscountCurveZeros(valuationDate,
                                             dates,
                                             rates,
                                             freqType,
                                             dayCountType,
                                             FinInterpTypes.LINEAR_ZERO_RATES)

    startDate = TuringDate(14, 6, 2016)
    endDate = TuringDate(14, 6, 2026)
    calendarType = TuringCalendarTypes.UNITED_STATES
    busDayAdjustType = TuringBusDayAdjustTypes.MODIFIED_FOLLOWING
    freqType = TuringFrequencyTypes.QUARTERLY
    dateGenRuleType = TuringDateGenRuleTypes.FORWARD
    lastFixing = 0.0065560
    notional = 1000000
    dayCountType = TuringDayCountTypes.ACT_360
    optionType = TuringCapFloorTypes.CAP
    strikeRate = 0.02

    cap = FinIborCapFloor(startDate, endDate, optionType, strikeRate,
                           lastFixing, freqType,  dayCountType, notional,
                           calendarType, busDayAdjustType, dateGenRuleType)

    blackVol = 0.547295
    model = FinModelBlack(blackVol)

    start = time.time()
    numRepeats = 10
    for i in range(0, numRepeats):
        v = cap.value(valuationDate, discountCurve, model)

    end = time.time()
    period = end - start
#    print(v, period/numRepeats)

###############################################################################


test_FinIborCapletHull()
test_FinIborCapFloorVolCurve()
test_FinIborCapFloor()
test_FinIborCapFloorQLExample()
testCases.compareTestCases()
