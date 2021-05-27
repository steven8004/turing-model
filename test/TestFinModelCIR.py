import numpy as np
import time

import sys
sys.path.append("..")

from turing_models.models.model_rates_cir import zeroPrice_MC, zeroPrice
from turing_models.models.model_rates_cir import TuringCIRNumericalScheme

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinModelRatesCIR():

    r0 = 0.05
    a = 0.20
    b = 0.05
    sigma = 0.20
    t = 5.0

    numPaths = 2000
    dt = 0.05
    seed = 1968

    testCases.header(
        "MATURITY",
        "TIME",
        "FORMULA",
        "EULER",
        "LOGNORM",
        "MILSTEIN",
        "KJ",
        "EXACT")

    for t in np.linspace(0, 10, 21):

        start = time.time()
        p = zeroPrice(r0, a, b, sigma, t)
        p_MC1 = zeroPrice_MC(
            r0,
            a,
            b,
            sigma,
            t,
            dt,
            numPaths,
            seed,
            TuringCIRNumericalScheme.EULER.value)
        p_MC2 = zeroPrice_MC(
            r0,
            a,
            b,
            sigma,
            t,
            dt,
            numPaths,
            seed,
            TuringCIRNumericalScheme.LOGNORMAL.value)
        p_MC3 = zeroPrice_MC(
            r0,
            a,
            b,
            sigma,
            t,
            dt,
            numPaths,
            seed,
            TuringCIRNumericalScheme.MILSTEIN.value)
        p_MC4 = zeroPrice_MC(
            r0,
            a,
            b,
            sigma,
            t,
            dt,
            numPaths,
            seed,
            TuringCIRNumericalScheme.KAHLJACKEL.value)
        p_MC5 = zeroPrice_MC(
            r0,
            a,
            b,
            sigma,
            t,
            dt,
            numPaths,
            seed,
            TuringCIRNumericalScheme.EXACT.value)
        end = time.time()
        elapsed = end - start
        testCases.print(t, elapsed, p, p_MC1, p_MC2, p_MC3, p_MC4, p_MC5)

###############################################################################


test_FinModelRatesCIR()
testCases.compareTestCases()