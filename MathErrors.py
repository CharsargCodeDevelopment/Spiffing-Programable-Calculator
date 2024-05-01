import warnings
class ListLengthMismatch(Warning):
    def __init__(self,x,y,message="Length mishmatch: The list lengths are not equal, {0}({1})!={2}({3})",lst1 = "x",lst2 = "y"):
        self.message = message.format(len(x),lst1,len(y),lst2)
        super.__init__(self.message)