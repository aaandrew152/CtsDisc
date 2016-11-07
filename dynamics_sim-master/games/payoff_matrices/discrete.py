import math

def generatePayoffs(myThreshold, yourThreshold, values):
    a, b, c, d, e, n = values

    myPayoff = 0

    for i in range(1, n+1):  # Cycles harm from 1 to n
        signals = signalsPossible(i, e, n)

        props = propPunish(signals, signals, myThreshold, yourThreshold)

        myPayoff += a * props[0] + b * props[1] + c * props[2] + d * props[3]

    return myPayoff


def signalsPossible(harm, error, n): # Don't allow harm error to be <1 and > n
    integerError = int(math.floor(error))

    signals = []

    if harm - integerError < 1:
        for i in range(1, harm + integerError + 1):
            signals.append(i)

    elif harm + integerError > n:
        for i in range(harm - integerError, n+1):
            signals.append(i)

    else:
        for i in range(harm - integerError, harm + integerError + 1):
            signals.append(i)

    return signals

def propPunish(mySignals, yourSignals, myThresh, yourThresh):
    AA = 0
    AB = 0
    BA = 0
    BB = 0

    for i in mySignals:
        for j in yourSignals:
            if i > myThresh:
                if j > yourThresh:
                    AA += 1
                else:
                    AB += 1
            else:
                if j > yourThresh:
                    BA += 1
                else:
                    BB += 1

    total = AA + AB + BA + BB

    return AA/total, AB / total, BA/total, BB/total