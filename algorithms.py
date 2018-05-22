def checkResult(netSales, eps):
    try:
        crfo = float(netSales[0])
    except:
        crfo = 0.0
    try:
        prfo = float(netSales[1])
    except:
        prfo = 0.0
    try:
        lrfo = float(netSales[2])
    except:
        lrfo = 0.0
    try:
        cqe = float(eps[0])
    except:
        cqe = 0.0
    try:
        pqe = float(eps[1])
    except:
        pqe = 0.0
    try:
        lqe = float(eps[2])
    except:
        lqe = 0.0
    if(cqe > lqe and crfo > prfo):
        if(cqe <= 1 and (cqe >= pqe + 0.25)):
            return True
        elif(cqe <= 2 and (cqe >= pqe+0.5)):
            return True
        elif(cqe <= 10 and cqe > 2 and (cqe >= pqe+1)):
            return True
        elif(cqe > 10 and (cqe >= pqe + 1.5)):
            return True
    return False