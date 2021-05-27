import numpy as np

import sys
sys.path.append("..")

from turing_models.market.volatility.ibor_cap_vol_curve import TuringIborCapVolCurve
from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.day_count import TuringDayCountTypes
from turing_models.models.model_black import TuringModelBlack
from turing_models.market.curves.discount_curve_flat import TuringDiscountCurveFlat
from turing_models.utilities.frequency import TuringFrequencyTypes
from turing_models.products.rates.ibor_swaption import TuringSwapTypes
from turing_models.products.rates.ibor_swaption import TuringIborSwaption
from turing_models.utilities.global_types import TuringCapFloorTypes
from turing_models.products.rates.ibor_lmm_products import TuringIborLMMProducts
from turing_models.products.rates.ibor_cap_floor import TuringIborCapFloor

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)

# This is in progress and needs to be completed

###############################################################################


# def test_Swaptions():
#     ''' In progress and so not used. TODO. '''

#     startYear = 2020
#     endYear = 2030
#     valuationDate = TuringDate(1, 1, startYear)
#     exerciseDate = TuringDate(1, 1, 2023)
#     settlementDate = valuationDate
#     maturityDate = TuringDate(1, 1, endYear)
#     fixedCoupon = 0.04

#     # DEFINE THE DISCOUNT CURVE
#     discountCurve = TuringDiscountCurveFlat(valuationDate,
#                                          0.04,
#                                          TuringFrequencyTypes.ANNUAL)

#     swaptionVol = 15.54

#     liborSwaption = TuringIborSwaption(settlementDate,
#                                      exerciseDate,
#                                      maturityDate,
#                                      FinIborSwaptionTypes.PAY,
#                                      fixedCoupon,
#                                      TuringFrequencyTypes.ANNUAL,
#                                      TuringDayCountTypes.ACT_360)

#     model = TuringModelBlack(swaptionVol/100.0)
#     v_BLK = liborSwaption.value(valuationDate, discountCurve, model)

#     dt = 0.5
#     texp = 3.0
#     tmat = 10.0
#     a = int(2*texp)
#     b = int(2*tmat)
#     numFwds = 20
#     taus = np.array([dt] * numFwds)

#     r = 0.05
#     fwd0 = getForwardCurve(numFwds, r)
#     correl = getCorrelationMatrix(numFwds, 0.00000000000001, dt)

#     fwdRateVol = 0.20
#     zetas = getVolCurve(numFwds, dt, fwdRateVol)

#     seed = 1489
#     numPaths = 2000 # 100000
#     fwdsNF = LMMSimulateFwdsNF(numFwds, numPaths, fwd0,
#                                zetas, correl, taus, seed)
#     strike = r
#     PAYSwaption = 1
#     useSobol = 0
#     numeraireIndex = 0

#     fwds1F = LMMSimulateFwds1F(numFwds, numPaths, numeraireIndex, fwd0,
#                                zetas, taus, useSobol, seed)

#     for iExp in range(1, 10):

#         texp = float(iExp)
#         a = int(2*texp)
#         print(a, b)

#         swaptionPrice1F = LMMSwaptionPricer(strike, a, b, numPaths,
#                                             fwd0, fwds1F, taus, PAYSwaption)

#         swaptionPriceNF = LMMSwaptionPricer(strike, a, b, numPaths,
#                                             fwd0, fwdsNF, taus, PAYSwaption)

#         swaptionVol = LMMSwaptionVolApprox(a, b, fwd0, taus, zetas, correl)

#         swapVolSim1F = LMMSimSwaptionVol(a, b, fwd0, fwds1F, taus)
#         swapVolSimNF = LMMSimSwaptionVol(a, b, fwd0, fwdsNF, taus)

#         valuationDate = TuringDate(1, 1, 2010)
#         liborCurve = TuringDiscountCurveFlat(valuationDate, r,
#                                           TuringFrequencyTypes.QUARTERLY)
#         settlementDate = valuationDate
#         exerciseDate = settlementDate.addMonths(a*3)
#         maturityDate = settlementDate.addMonths(b*3)

#         fixedCoupon = strike
#         fixedFrequencyType = TuringFrequencyTypes.QUARTERLY
#         fixedDayCountType = TuringDayCountTypes.ACT_ACT_ISDA
#         floatFrequencyType = TuringFrequencyTypes.QUARTERLY
#         floatDayCountType = TuringDayCountTypes.ACT_ACT_ISDA
#         notional = 1.0

#         # Pricing a PAY
#         swaptionType = FinIborSwaptionTypes.PAY
#         swaption = TuringIborSwaption(settlementDate,
#                                     exerciseDate,
#                                     maturityDate,
#                                     swaptionType,
#                                     fixedCoupon,
#                                     fixedFrequencyType,
#                                     fixedDayCountType,
#                                     notional,
#                                     floatFrequencyType,
#                                     floatDayCountType)

#         model = TuringModelBlack(swaptionVol)
#         blackSwaptionPrice = swaption.value(valuationDate, liborCurve, model)

#         testCases.print("K:%6.5f texp:%8.2f FwdVol:%9.5f SimVol1F:%9.5f " +
#                         " SimVolNF:%9.5f RebVol:%9.5f SimPx1F:%9.5f SimPxNF:%9.5f Black Px:%9.5f" 
#               % (strike, texp, fwdRateVol, swapVolSim1F, swapVolSimNF,
#                  swaptionVol, swaptionPrice1F, swaptionPriceNF,
#                  blackSwaptionPrice))

###############################################################################


# def test_CapsFloors():

#     # Define the CAP
#     # The maturity date is in 10 years so the last caplet start time is in 9
#     # years which in our convention means we are modelling 10 forwards
#     startYear = 2020
#     endYear = 2030
#     valuationDate = TuringDate(1, 1, startYear)
#     settlementDate = valuationDate
#     capMaturityDate = TuringDate(1, 1, endYear)
#     freqType = TuringFrequencyTypes.ANNUAL
#     dayCountType = TuringDayCountTypes.ACT_360
#     capFloorRate = 0.04

#     # DEFINE THE DISCOUNT CURVE
#     discountCurve = TuringDiscountCurveFlat(valuationDate,
#                                          0.04,
#                                          TuringFrequencyTypes.ANNUAL)

#     capVol = 15.54

#     liborCap = TuringIborCapFloor(settlementDate,
#                                 capMaturityDate,
#                                 FinIborCapFloorTypes.CAP,
#                                 capFloorRate,
#                                 None,
#                                 TuringFrequencyTypes.ANNUAL,
#                                 TuringDayCountTypes.ACT_360)

#     model = TuringModelBlack(capVol/100.0)
#     v_BLK = liborCap.value(valuationDate, discountCurve, model)

#     ###########################################################################
#     # LMM VALUATION
#     ###########################################################################

#     lmmProducts = TuringIborLMMProducts(settlementDate,
#                                       capMaturityDate,
#                                       freqType,
#                                       dayCountType)

#     # Set up forward rate vol structure
#     capVolDates = []
#     capletVolTenor = "1Y"
#     capletDt = valuationDate
#     numForwards = endYear - startYear

#     # Capvol dates has numForwards + 1 elements including today
#     capVolDates.append(valuationDate)
#     for i in range(0, numForwards):
#         capletDt = capletDt.addTenor(capletVolTenor)
#         capVolDates.append(capletDt)

#     # Capvol dates has numForwards + 1 elements including zero today
#     capVolatilities = [capVol] * (numForwards+1)
#     capVolatilities[0] = 0.0
#     capVolatilities = np.array(capVolatilities)/100.0

#     dayCountType = TuringDayCountTypes.ACT_ACT_ISDA
#     volCurve = TuringIborCapVolCurve(valuationDate,
#                                    capVolDates,
#                                    capVolatilities,
#                                    dayCountType)

#     lambdas2FList = [[0.00, 0.1410, 0.1952, 0.1678, 0.1711, 0.1525,
#                       0.1406, 0.1265, 0.1306, 0.1236],
#                      [0.00, -0.0645, -0.0670, -0.0384, -0.0196, 0.00,
#                      0.0161, 0.0289, 0.0448, 0.0565]]
#     lambdas2F = np.array(lambdas2FList)

#     # Simulate paths of future Libor rates
#     numFactors = 1

#     testCases.header("NUMPATHS", "VLMM", "VBLK", "ERROR")

#     for numPaths in [10000, 20000, 50000, 100000, 200000, 400000, 1000000]:

#         if numFactors == 1:
#             lmmProducts.simulate1F(discountCurve, volCurve, numPaths, 0, True)
#         elif numFactors == 2:
#             lmmProducts.simulateMF(discountCurve, numFactors, lambdas2F,
#                                    numPaths, 0, True)

#         v_lmm = lmmProducts.valueCapFloor(settlementDate,
#                                           capMaturityDate,
#                                           FinIborCapFloorTypes.CAP,
#                                           capFloorRate,
#                                           TuringFrequencyTypes.ANNUAL,
#                                           TuringDayCountTypes.ACT_360)

#         err = v_lmm - v_BLK
#         testCases.print(numPaths, v_lmm, v_BLK, err)

###############################################################################


# test_CapsFloors()
# test_Swaptions()
testCases.compareTestCases()