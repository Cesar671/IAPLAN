import enum

def parse_tuple(predicate, start="(", end=")") -> str:
  ans = ""
  first = True
  second = True
  for elem in predicate:
    if first:
      first = False
      ans += elem + start
    elif second:
      second = False
      ans += __parse_name(elem)
    else:
      ans += "," + __parse_name(elem)
  return ans + end

def __parse_name(predicate_val):
  cad = ""
  if isinstance(predicate_val, enum.Enum):
    cad = predicate_val.name
  else:
    cad = str(predicate_val)
  return cad