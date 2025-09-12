# https://realpython.com/python-enum/
from enum import Enum

HTTPMethod = Enum("HTTPMethod", ["GET", "POST", "PUSH", "PATCH", "DELETE"]
)



list(HTTPMethod)

def testMe(arg:HTTPMethod):
    if(arg == HTTPMethod.DELETE):
      print(arg.name)


testMe(HTTPMethod.GET)
testMe(HTTPMethod.DELETE)