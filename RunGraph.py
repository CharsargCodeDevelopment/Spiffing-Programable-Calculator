#import MicroTurtle as turtle
#import grid
from math import *
#from DisplaySystem import *
def RunCalculate(calculation,variables = {"x":5},functions = []):
    subsituted = calculation.split("=")[-1]
    for variable in variables:
        value = str(variables[variable])
        subsituted = value.join(subsituted.split(variable))

    #print(subsituted)

    result = eval(subsituted)

    if len(calculation.split("=")) == 2:
        subsituted = calculation.split("=")[0]+"="+subsituted

    #print(subsituted)
    #print(result)
    return int(result)




"""
calculation = ""
calculations = []
while calculation != "start":
    calculation = input()
    if calculation != "start":
        calculations.append(calculation)

#"""

def ProscsessGraph(calculations,variables,H=600,W=600,XRange=10,YRange = 10,pos = (0,0),res = 10,center=(80,64),zoom = 1):
    output = []
    for calculationData in calculations:
        X,Y = [],[]
        calculation = calculationData[0]
        #print(calculation)
        color = calculationData[1]
        BottomX = -int(XRange/2)
        TopX = int(XRange/2)
        #print(TopX)
        for x in range(BottomX*res,TopX*res):
            x = x/res
            variables['x'] = (x*zoom)+pos[0]
            value = RunCalculate(calculation,variables)
            if len(calculation.split("=")) == 2:
                if calculation.split("=")[0] == "y":
                    y=value+pos[1]
                else:
                    variables[calculation.split("=")[0]] = value
                    y=value
            y = y*zoom
            x1 = H*(x/XRange)
            y1 = W*(y/XRange)
            if int(x1) < -center[0]:
                continue
            if int(y1) < -center[1]:
                continue
            if int(x1) > center[0]:
                continue
            if int(y1) > center[1]:
                continue
            if int(x1) in X:
                if int(y1) in Y:
                    continue
            X.append(int(x1))
            Y.append(int(y1))
        output.append([X,Y,color])
    del X
    del Y
    return output

if __name__ == '__main__':
    calculations = [["y=x",(0,0,255)],["y=cos(x)",(0,0,255)],["y=sin(x)",(255,0,0)]]
    variables = {}
    #turtle.penup()
    H = 160
    W = 128
    XRange = 16
    YRange = 12
    result = ProscsessGraph(calculations,variables,H,W,XRange,YRange)