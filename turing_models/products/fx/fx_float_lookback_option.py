


import numpy as np
from enum import Enum

from turing_models.utilities.mathematics import N
from turing_models.utilities.global_variables import gDaysInYear, gSmall
from turing_models.utilities.error import TuringError
from turing_models.models.gbm_process import TuringGBMProcess
from turing_models.products.fx.fx_option import TuringFXOption
from turing_models.utilities.helper_functions import checkArgumentTypes
from turing_models.utilities.turing_date import TuringDate
from turing_models.utilities.global_types import TuringOptionTypes
from turing_models.market.curves.discount_curve import TuringDiscountCurve

##########################################################################
# TODO: Attempt control variate adjustment to monte carlo
# TODO: Sobol for Monte Carlo
# TODO: TIGHTEN UP LIMIT FOR W FROM 100
# TODO: Vectorise the analytical pricing formula
##########################################################################


##########################################################################
# FLOAT STRIKE LOOKBACK CALL PAYS MAX(S(T)-SMIN,0)
# FLOAT STRIKE LOOKBACK PUT PAYS MAX(SMAX-S(T),0)
##########################################################################


class TuringFXFloatLookbackOption(TuringFXOption):
    ''' This is an FX option in which the strike of the option is not fixed
    but is set at expiry to equal the minimum fx rate in the case of a call
    or the maximum fx rate in the case of a put. '''

    def __init__(self,
                 expiryDate: TuringDate,
                 optionType: TuringOptionTypes):
        ''' Create the FloatLookbackOption by specifying the expiry date and
        the option type. '''

        checkArgumentTypes(self.__init__, locals())

        self._expiryDate = expiryDate
        self._optionType = optionType

##########################################################################

    def value(self,
              valueDate: TuringDate,
              stockPrice: float,
              domesticCurve: TuringDiscountCurve,
              foreignCurve: TuringDiscountCurve,
              volatility: float,
              stockMinMax: float):
        ''' Valuation of the Floating Lookback option using Black-Scholes using
        the formulae derived by Goldman, Sosin and Gatto (1979). '''

        t = (self._expiryDate - valueDate) / gDaysInYear

        df = domesticCurve._df(t)
        r = -np.log(df)/t

        dq = foreignCurve._df(t)
        q = -np.log(dq)/t

        v = volatility
        s0 = stockPrice
        smin = 0.0
        smax = 0.0

        if self._optionType == TuringOptionTypes.EUROPEAN_CALL:
            smin = stockMinMax
            if smin > s0:
                raise TuringError(
                    "Smin must be less than or equal to the stock price.")
        elif self._optionType == TuringOptionTypes.EUROPEAN_PUT:
            smax = stockMinMax
            if smax < s0:
                raise TuringError(
                    "Smax must be greater than or equal to the stock price.")

        if abs(r - q) < gSmall:
            q = r + gSmall

        dq = np.exp(-q * t)
        df = np.exp(-r * t)
        b = r - q
        u = v * v / 2.0 / b
        w = 2.0 * b / v / v
        expbt = np.exp(b * t)

        # Taken from Haug Page 142
        if self._optionType == TuringOptionTypes.EUROPEAN_CALL:

            a1 = (np.log(s0 / smin) + (b + (v**2) / 2.0) * t) / v / np.sqrt(t)
            a2 = a1 - v * np.sqrt(t)

            if smin == s0:
                term = N(-a1 + 2.0 * b * np.sqrt(t) / v) - expbt * N(-a1)
            elif s0 < smin and w < -100:
                term = - expbt * N(-a1)
            else:
                term = ((s0 / smin)**(-w))*N(-a1 + 2.0 *
                                             b*np.sqrt(t) / v) - expbt * N(-a1)

            v = s0 * dq * N(a1) - smin * df * N(a2) + s0 * df * u * term

        elif self._optionType == TuringOptionTypes.EUROPEAN_PUT:

            b1 = (np.log(s0 / smax) + (b + (v**2) / 2.0) * t) / v / np.sqrt(t)
            b2 = b1 - v * np.sqrt(t)

            if smax == s0:
                term = -N(b1 - 2.0 * b * np.sqrt(t) / v) + expbt * N(b1)
            elif s0 < smax and w > 100:
                term = expbt * N(b1)
            else:
                term = (-(s0 / smax)**(-w)) * \
                    N(b1 - 2.0 * b * np.sqrt(t) / v) + expbt * N(b1)

            v = smax * df * N(-b2) - s0 * dq * N(-b1) + s0 * df * u * term

        else:
            raise TuringError("Unknown lookback option type:" +
                              str(self._optionType))

        return v

##########################################################################

    def valueMC(
            self,
            valueDate,
            stockPrice,
            domesticCurve,
            foreignCurve,
            volatility,
            stockMinMax,
            numPaths=10000,
            numStepsPerYear=252,
            seed=4242):

        t = (self._expiryDate - valueDate) / gDaysInYear
        df = domesticCurve._df(t)
        r = -np.log(df)/t

        dq = domesticCurve._df(t)
        q = -np.log(dq)/t

        numTimeSteps = int(t * numStepsPerYear)
        mu = r - q

        optionType = self._optionType
        smin = 0.0
        smax = 0.0

        if self._optionType == TuringOptionTypes.EUROPEAN_CALL:
            smin = stockMinMax
            if smin > stockPrice:
                raise TuringError(
                    "Smin must be less than or equal to the stock price.")
        elif self._optionType == TuringOptionTypes.EUROPEAN_PUT:
            smax = stockMinMax
            if smax < stockPrice:
                raise TuringError(
                    "Smax must be greater than or equal to the stock price.")

        model = TuringGBMProcess()
        Sall = model.getPaths(
            numPaths,
            numTimeSteps,
            t,
            mu,
            stockPrice,
            volatility,
            seed)

        # Due to antithetics we have doubled the number of paths
        numPaths = 2 * numPaths
        payoff = np.zeros(numPaths)

        if optionType == TuringOptionTypes.EUROPEAN_CALL:
            SMin = np.min(Sall, axis=1)
            SMin = np.minimum(SMin, smin)
            payoff = np.maximum(Sall[:, -1] - SMin, 0.0)
        elif optionType == TuringOptionTypes.EUROPEAN_PUT:
            SMax = np.max(Sall, axis=1)
            SMax = np.maximum(SMax, smax)
            payoff = np.maximum(SMax - Sall[:, -1], 0.0)
        else:
            raise TuringError("Unknown lookback option type:" + str(optionType))

        v = payoff.mean() * np.exp(-r * t)
        return v

##########################################################################