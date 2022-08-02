import math

h_l, h_h = 0, 1

def harmDist(x):  # Probability distribution function MINUS ATOM AT 0
    return 1 if 0 <= x <= 1 else 0


def punishProb(harm, threshold, error):  # Returns probability that a player punishes
    return (harm - threshold + error)/(2 * error)


def trapIntegrate(integrand, bottom, top, step=0.005):  # Uses trapezoidal integration to approximate integral
    if top <= bottom:
        return 0

    currentPos = bottom
    totalArea = 0
    while currentPos <= top:  # TODO check for exact steps
        botValue = integrand(currentPos)
        currentPos += step
        topValue = integrand(currentPos)

        totalArea += (botValue + topValue) * step / 2

    return totalArea


def generatePayoffs(myThreshold, yourThreshold, values):
    *p, errorRange = values

    if myThreshold < yourThreshold - 2 * errorRange:  # Will never experience overlap as there is a gap of 2 * error
        payoff = noOverlap(myThreshold, yourThreshold, errorRange, p, A)
    elif myThreshold < yourThreshold + 2 * errorRange:  # Overlap is present
        payoff = overlap(myThreshold, yourThreshold, errorRange, p, A)
    else:  # No overlap in the opposite direction
        payoff = noOverlap(myThreshold, yourThreshold, errorRange, p, A)

    return payoff

def noOverlap(myThresh, yourThresh, error, param):

    if myThresh < yourThresh:
        lesser, greater = myThresh, yourThresh
        a, b, c, d = param
    else:
        lesser, greater = yourThresh, myThresh
        a, c, b, d = param

    totalPayoff = 0

    totalPayoff += d * trapIntegrate(harmDist, h_l, lesser - error)
    # Both never punish [h_l, lesser - error]

    lesserSometimesPunish = trapIntegrate(lambda x: harmDist(x)*punishProb(x, lesser, error), lesser - error, lesser + error)
    lesserSometimesDont = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, lesser, error)), lesser - error, lesser + error)

    totalPayoff += c * lesserSometimesPunish
    totalPayoff += d * lesserSometimesDont
    # Lesser sometimes punishes [lesser - error, lesser + error]

    totalPayoff += c * trapIntegrate(harmDist, lesser + error, greater - error)
    # Lesser punishes, greater does not punish [lesser + error, greater - error]

    greaterSometimesPunish = trapIntegrate(lambda x: harmDist(x)*punishProb(x, greater, error), greater - error, greater + error)
    greaterSometimesDont = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, greater, error)), greater - error, greater + error)

    totalPayoff += a * greaterSometimesPunish
    totalPayoff += c * greaterSometimesDont
    # Lesser punishes, greater sometimes punishes [greater - error, greater + error]

    totalPayoff += a * trapIntegrate(harmDist, greater + error, h_h)
    # Both always punish [greater + error, h_h]

    return totalPayoff


def overlap(myThresh, yourThresh, error, param):
    if myThresh < yourThresh:
        lesser, greater = myThresh, yourThresh
        a, b, c, d = param
    else:
        lesser, greater = yourThresh, myThresh
        a, c, b, d = param  # Switched to take other player into account

    totalPayoff = 0

    totalPayoff += d * trapIntegrate(harmDist, h_l, lesser - error)
    # Both never punish [h_l, lesser - error]

    lesserSometimesPunish = trapIntegrate(lambda x: harmDist(x)*punishProb(x, lesser, error), lesser - error, greater - error)
    lesserSometimesDont = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, lesser, error)), lesser - error, greater - error)

    totalPayoff += c * lesserSometimesPunish
    totalPayoff += d * lesserSometimesDont
    # Lesser sometimes punishes [lesser - error, greater - error]

    lessPunGreatPun = trapIntegrate(lambda x: harmDist(x)*punishProb(x, lesser, error)*punishProb(x, greater, error), greater - error, lesser + error)
    lessDontGreatPun = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, lesser, error))*punishProb(x, greater, error), greater - error, lesser + error)
    lessPunGreatDont = trapIntegrate(lambda x: harmDist(x)*punishProb(x, lesser, error)*(1 - punishProb(x, greater, error)), greater - error, lesser + error)
    lessDontGreatDont = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, lesser, error))*(1 - punishProb(x, greater, error)), greater - error, lesser + error)

    totalPayoff += a * lessPunGreatPun
    totalPayoff += b * lessPunGreatDont
    totalPayoff += c * lessDontGreatPun
    totalPayoff += d * lessDontGreatDont
    # Both have a chance of punishing [greater - error, lesser + error]

    greaterSometimesPunish = trapIntegrate(lambda x: harmDist(x)*punishProb(x, greater, error), lesser + error, greater + error)
    greaterSometimesDont = trapIntegrate(lambda x: harmDist(x)*(1 - punishProb(x, greater, error)), lesser + error, greater + error)

    totalPayoff += a * greaterSometimesPunish
    totalPayoff += c * greaterSometimesDont
    # Lesser punishes, greater sometimes punishes [lesser + error, greater + error]

    totalPayoff += a * trapIntegrate(harmDist, greater + error, h_h)
    # Both always punish [greater + error, h_h]

    return totalPayoff