def checkResult(netSales, eps):
    crfo = float(netSales[0])
    prfo = float(netSales[1])
    lrfo = float(netSales[2])
    cqe = float(eps[0])
    pqe = float(eps[1])
    lqe = float(eps[2])
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