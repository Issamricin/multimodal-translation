# https://realpython.com/python-enum/
from enum import Enum

HTTPMethod = Enum("HTTPMethod", ["GET", "POST", "PUSH", "PATCH", "DELETE"])

list(HTTPMethod)

def test_me(arg:HTTPMethod):
  """testing..."""
  if arg == HTTPMethod.DELETE:
    print(arg.name)


test_me(HTTPMethod.GET)
test_me(HTTPMethod.DELETE)
