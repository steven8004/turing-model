###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import sys
sys.path.append("..")

import numpy as np
from financepy.models.turing_model_sabr_shifted import TuringModelSABRShifted
from financepy.turingutils.turing_global_types import TuringOptionTypes

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

###############################################################################

###############################################################################


def test_ShiftedSABR():

    testCases.header("TEST", "CALIBRATION ERROR")

    alpha = 0.0
    beta = 0.5
    rho = -0.09
    nu = 0.1
    shift = 0.02
    
    strikeVol = 0.1
    
    f = 0.043
    k = 0.050
    r = 0.03
    texp = 2.0

    callOptionType = TuringOptionTypes.EUROPEAN_CALL
    putOptionType = TuringOptionTypes.EUROPEAN_PUT
    
    df = np.exp(-r * texp)
    
    # SABR equivalent to lognormal (Black) model (i.e. beta = 1, rho = 0, nu = 0, shift = 0)
    modelSABR_01 = TuringModelSABRShifted(0.0, 1.0, 0.0, 0.0, 0.0)
    modelSABR_01.setAlphaFromBlackVol(strikeVol, f, k, texp)

    impliedLognormalVol = modelSABR_01.blackVol(f, k, texp)
    impliedATMLognormalVol = modelSABR_01.blackVol(k, k, texp)
    impliedLognormalSmile = impliedLognormalVol - impliedATMLognormalVol

    assert impliedLognormalSmile == 0.0, "In lognormal model, smile should be flat"
    calibrationError = round(strikeVol - impliedLognormalVol, 12)
    testCases.print("LOGNORMAL CASE", calibrationError)

    # Volatility: pure SABR dynamics
    modelSABR_02 = TuringModelSABRShifted(alpha, beta, rho, nu, shift)
    modelSABR_02.setAlphaFromBlackVol(strikeVol, f, k, texp)

    impliedLognormalVol = modelSABR_02.blackVol(f, k, texp)
    impliedATMLognormalVol = modelSABR_02.blackVol(k, k, texp)
    impliedLognormalSmile = impliedLognormalVol - impliedATMLognormalVol
    calibrationError = round(strikeVol - impliedLognormalVol, 12)
    testCases.print("SABR CASE", calibrationError)

    # Valuation: pure SABR dynamics
    valueCall = modelSABR_02.value(f, k, texp, df, callOptionType)
    valuePut = modelSABR_02.value(f, k, texp, df, putOptionType)
    assert round((valueCall - valuePut), 12) == round(df*(f - k), 12), \
        "The method called 'value()' doesn't comply with Call-Put parity"

    # TODO: adding Call-Put parity test for all sensitivities

###############################################################################


test_ShiftedSABR()
testCases.compareTestCases()