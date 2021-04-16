import sys
sys.path.append("..")

from turing_models.products.bonds.bond_future import TuringBondFuture
from turing_models.products.bonds.bond import TuringBond
from turing_models.utilities.frequency import TuringFrequencyTypes
from turing_models.utilities.day_count import TuringDayCountTypes
from turing_models.utilities.date import TuringDate

from TuringTestCases import TuringTestCases, globalTestCaseMode
testCases = TuringTestCases(__file__, globalTestCaseMode)


def test_FinBondFuture():

    # Example taken from Martellini and Priaulet page 360
    freq = TuringFrequencyTypes.SEMI_ANNUAL
    basis = TuringDayCountTypes.ACT_ACT_ICMA
    issueDate = TuringDate(15, 2, 2004)

    bond1 = TuringBond(issueDate, TuringDate(15, 8, 2011), 0.0500, freq, basis)
    bond2 = TuringBond(issueDate, TuringDate(15, 2, 2011), 0.0500, freq, basis)
    bond3 = TuringBond(issueDate, TuringDate(15, 8, 2010), 0.0575, freq, basis)
    bond4 = TuringBond(issueDate, TuringDate(15, 2, 2010), 0.0650, freq, basis)
    bond5 = TuringBond(issueDate, TuringDate(15, 8, 2009), 0.0600, freq, basis)
    bond6 = TuringBond(issueDate, TuringDate(15, 5, 2009), 0.0550, freq, basis)
    bond7 = TuringBond(issueDate, TuringDate(15, 11, 2008), 0.0475, freq, basis)

    bonds = []
    bonds.append(bond1)
    bonds.append(bond2)
    bonds.append(bond3)
    bonds.append(bond4)
    bonds.append(bond5)
    bonds.append(bond6)
    bonds.append(bond7)

    firstDeliveryDate = TuringDate(1, 3, 2002)
    lastDeliveryDate = TuringDate(28, 3, 2002)
    contractSize = 100000
    contractCoupon = 0.06

    bondFutureContract = TuringBondFuture("TYH2",
                                          firstDeliveryDate,
                                          lastDeliveryDate,
                                          contractSize,
                                          contractCoupon)

    settlementDate = TuringDate(10, 12, 2001)

    # Get the Conversion Factors
    testCases.header("Bond Maturity", "Coupon", "Conversion Factor")
    for bond in bonds:
        cf = bondFutureContract.conversionFactor(bond)
        testCases.print(bond._maturityDate, bond._coupon * 100, cf)

    # Example from
    # https://www.cmegroup.com/education/files/understanding-treasury-futures.pdf

    testCases.banner("EXAMPLE FROM CME")
    testCases.banner("================")
    settlementDate = TuringDate(10, 10, 2017)

    bonds = []
    prices = []
    bond = TuringBond(issueDate, TuringDate(15, 8, 2027), 0.0225, freq, basis)
    bonds.append(bond)
    prices.append(99 + 1 / 32)
    bond = TuringBond(issueDate, TuringDate(15, 5, 2027), 0.02375, freq, basis)
    bonds.append(bond)
    prices.append(100 + 5 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 2, 2027), 0.0225, freq, basis)
    bonds.append(bond)
    prices.append(99 + 5 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 11, 2026), 0.02, freq, basis)
    bonds.append(bond)
    prices.append(97 + 7 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 8, 2026), 0.015, freq, basis)
    bonds.append(bond)
    prices.append(93 + 14 / 32)
    bond = TuringBond(issueDate, TuringDate(15, 5, 2026), 0.01625, freq, basis)
    bonds.append(bond)
    prices.append(94 + 21 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 2, 2026), 0.01625, freq, basis)
    bonds.append(bond)
    prices.append(94 + 29 / 32)
    bond = TuringBond(issueDate, TuringDate(15, 11, 2025), 0.0225, freq, basis)
    bonds.append(bond)
    prices.append(99 + 25 / 32)
    bond = TuringBond(issueDate, TuringDate(15, 8, 2025), 0.02, freq, basis)
    bonds.append(bond)
    prices.append(98 + 3 / 32)
    bond = TuringBond(issueDate, TuringDate(15, 5, 2025), 0.02125, freq, basis)
    bonds.append(bond)
    prices.append(99 + 5 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 2, 2025), 0.02, freq, basis)
    bonds.append(bond)
    prices.append(98 + 14 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 11, 2024), 0.0225, freq, basis)
    bonds.append(bond)
    prices.append(100 + 9 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 8, 2024), 0.02375, freq, basis)
    bonds.append(bond)
    prices.append(101 + 7 / 32 + 1 / 64)
    bond = TuringBond(issueDate, TuringDate(15, 8, 2024), 0.01875, freq, basis)
    bonds.append(bond)
    # There may be an error in the document says 98-01+
    prices.append(98 + 1 / 32)

    testCases.header("BOND MATURITY", "YIELD")
    for bond, cleanPrice in zip(bonds, prices):
        yld = bond.yieldToMaturity(settlementDate, cleanPrice)
        testCases.print(str(bond._maturityDate), yld)

    firstDeliveryDate = TuringDate(1, 12, 2017)
    lastDeliveryDate = TuringDate(28, 12, 2017)

    contractSize = 100000
    contractCoupon = 0.06

    bondFutureContract = TuringBondFuture("TYZ7",
                                          firstDeliveryDate,
                                          lastDeliveryDate,
                                          contractSize,
                                          contractCoupon)

    testCases.header("BOND MATURITY", "CF")
    for bond in bonds:
        cf = bondFutureContract.conversionFactor(bond)
        testCases.print(str(bond._maturityDate), cf)

    # Get the Invoice Prices
    futuresPrice = 125.265625

    testCases.header("BOND MATURITY", "PRINCIPAL INVOICE PRICE")
    for bond in bonds:
        pip = bondFutureContract.principalInvoicePrice(bond, futuresPrice)
        testCases.print(str(bond._maturityDate), pip)

    testCases.header("BOND MATURITY", "TOTAL INVOICE AMOUNT")
    for bond in bonds:
        tia = bondFutureContract.totalInvoiceAmount(
            settlementDate, bond, futuresPrice)
        testCases.print(str(bond._maturityDate), tia)

    ctd = bondFutureContract.cheapestToDeliver(bonds,
                                               prices,
                                               futuresPrice)

    testCases.header("CTD MATURITY", "CTD COUPON")
    testCases.print(str(ctd._maturityDate), ctd._coupon)

##########################################################################


test_FinBondFuture()
testCases.compareTestCases()
