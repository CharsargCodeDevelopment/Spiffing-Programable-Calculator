#import warnings
class ListLengthMismatch(Warning):
    def __init__(self,x,y,message="Length mishmatch: The list lengths are not equal, {0}({1})!={2}({3})",lst1 = "x",lst2 = "y"):
        self.message = message.format(len(x),lst1,len(y),lst2)
        super.__init__(self.message)
class CalculationError(Warning):
    def __init__(self,Calculation,message = "Calculation Error With {Caclulation} Please Ammend."):
        self.message = message.format(str(Calculation))
        super.__init__(self.message)