import csv
from helpers import InterpretedArgsIterable
from typing import Callable, Dict, List
from man import manpage

def process_data(data: Dict):
    data["PFS"] = data["PFS"] == "True"
    data["TAGS"] = data["TAGS"].split(", ")
    return data

with open("pathitems.csv", "r") as f:
    reader = csv.DictReader(f)
    data = [line_dict for line_dict in reader]

argmap: Dict[str, Callable[[List[str]], Callable[[Dict[str, str]], bool]]] = {}

def arg(func: Callable) -> Callable:
    argmap[func.__name__] = func
    return func

@arg
def price(args: List[str]) -> Callable[[Dict[str, str]], bool]:
    map = {
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
        "=": lambda x, y: x == y
    }

    def float_and_k(val: str):
        if len(val) > 1 and val[-1] == "k":
            return float(val[:-1]) * 1000
        else:
            return float(val)
    
    def price_individual_condition(condition: str) -> Callable[[float], bool]:
        try:
            func = map[condition[0]]
            val = float_and_k(condition[1:])

        except KeyError:
            raise ValueError("Unrecognised argument for price flag: " + condition[0])

        except ValueError:
            raise ValueError("Number not recognised for price flag: " + condition[1:])

        return lambda x: func(x, val)

    funclist = [price_individual_condition(condition) for condition in args]
    
    return lambda x: all(func(float_and_k(x["PRICE"])) for func in funclist)

def text_search(args: List[str]):
    def check_individual_name(name: str) -> Callable[[str], bool]:
        splitname = name.split("*")

        start = splitname[0]
        middle = splitname[1:-1] if len(splitname) > 2 else []
        end = splitname[-1] if len(splitname) > 1 else ""

        def handle_middle(name: str):
            if not middle:
                return True
            
            indices = [name.find(elem) for elem in middle]

            if any(index == -1 for index in indices):
                return False
            
            iterator = iter(indices)

            next(iterator)

            return all(a > b for a, b in zip(iterator, indices))

        return lambda x: x.startswith(start) and x.endswith(end) and handle_middle(x)

    funclist = [check_individual_name(condition.lower()) for condition in args]

    return funclist


@arg
def name(args: List[str]) -> Callable[[Dict[str, str]], bool]:
    funclist = text_search(args)
    return lambda x: all(func(x["NAME"].lower()) for func in funclist)
    
@arg
def description(args: List[str]) -> Callable[[Dict[str, str]], bool]:
    funclist = text_search(args)
    return lambda x: all(func(x["DESCRIPTION"].lower()) for func in funclist)

@arg
def slot(args: List[str]) -> Callable[[Dict[str, str]], bool]:
    funclist = text_search(args)
    return lambda x: all(func(x["SLOT"].lower()) for func in funclist)

@arg 
def tag(args) -> Callable[[Dict[str, str]], bool]:
    funclist = text_search(args)
    return lambda x: all(any(func(tag.lower()) for tag in x["TAGS"].split(", ")) for func in funclist)
    

def find(int_args: InterpretedArgsIterable):
    conditions = [argmap[key](value) for key, value in int_args]

    candidates = [elem for elem in data if all(condition(elem) for condition in conditions)]

    ret = "\n\n------\n\n".join("\n\n".join(key+"\n"+value for key, value in candidate.items() if value) for candidate in candidates)

    return ret

    
