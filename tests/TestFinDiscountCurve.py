###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append("..")

from financepy.turingutils.turing_date import TuringDate
from financepy.turingutils.turing_frequency import TuringFrequencyTypes
from financepy.market.curves.turing_interpolator import FinInterpTypes
from financepy.market.curves.turing_discount_curve import TuringDiscountCurve
from financepy.turingutils.turing_math import scale

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################
# TODO: Add other discount curves
###############################################################################

PLOT_GRAPHS = False


def test_FinDiscountCurve():

    # Create a curve from times and discount factors
    startDate = TuringDate(1, 1, 2018)
    years = np.linspace(0, 10, 6)
    rate = 0.05 + 0.005*years - 0.0003*years*years
    dfs = np.exp(-rate * years)
    dates = startDate.addYears(years)

    curve = TuringDiscountCurve(startDate, dates, dfs, FinInterpTypes.FLAT_FWD_RATES)

    testCases.header("T", "DF", "ZERORATE", "CC_FWD", "MM_FWD", "SURVPROB")

    plotYears = np.linspace(0, 12, 12*12+1)[1:]
    plotDates = startDate.addYears(plotYears)

    # Examine dependency of curve on compounding rate
    zeroRates_A = curve.zeroRate(plotDates, TuringFrequencyTypes.ANNUAL)
    zeroRates_S = curve.zeroRate(plotDates, TuringFrequencyTypes.SEMI_ANNUAL)
    zeroRates_Q = curve.zeroRate(plotDates, TuringFrequencyTypes.QUARTERLY)
    zeroRates_M = curve.zeroRate(plotDates, TuringFrequencyTypes.MONTHLY)
    zeroRates_C = curve.zeroRate(plotDates, TuringFrequencyTypes.CONTINUOUS)

    if PLOT_GRAPHS:
        plt.figure(figsize=(6, 4))
        plt.plot(plotYears, scale(zeroRates_A, 100), label='A')
        plt.plot(plotYears, scale(zeroRates_S, 100), label='S')
        plt.plot(plotYears, scale(zeroRates_Q, 100), label='Q')
        plt.plot(plotYears, scale(zeroRates_M, 100), label='M')
        plt.plot(plotYears, scale(zeroRates_C, 100), label='C')
        plt.ylim((5, 8))

        plt.title('Discount Curves')
        plt.xlabel('Time (years)')
        plt.ylabel('Zero Rate (%)')
        plt.legend(loc='lower right', frameon=False)

    # Examine dependency of fwd curve on the interpolation scheme

    for interp in FinInterpTypes:

        curve = TuringDiscountCurve(startDate, dates, dfs, interp)
        fwdRates = curve.fwd(plotDates)
        zeroRates = curve.zeroRate(plotDates, TuringFrequencyTypes.ANNUAL)
        parRates = curve.swapRate(startDate, plotDates, TuringFrequencyTypes.ANNUAL)

        if PLOT_GRAPHS:
            plt.figure(figsize=(6, 4))
            plt.plot(plotYears, scale(fwdRates, 100), label='FWD RATES')
            plt.plot(plotYears, scale(zeroRates, 100), label='ZERO RATES')
            plt.plot(plotYears, scale(parRates, 100), label='PAR RATES')
            plt.ylim((3.0, 8.5))

            plt.title('Forward Curves using ' + str(interp))
            plt.xlabel('Time (years)')
            plt.ylabel('Fwd Rate (%)')
            plt.legend(loc='lower right', frameon=False)

###############################################################################


test_FinDiscountCurve()
testCases.compareTestCases()
