#!/usr/bin/env python3

from jsonrpcserver import Result, Success, serve, method, Error
import os
from warrens import gen_text
from helpers import InterpretedArgsIterable
from pathitem import find
from man import manpage

public_methods = set()
secret_methods = set()

def public_method(func):
    func = method(func)
    public_methods.add(func)

    return func

def secret_method(func):
    func = method(func)
    secret_methods.add(func)

    return func

@secret_method
def ping() -> Result:
    return Success("pong")

@secret_method
def darren() -> Result:
    return Success("darren")

@secret_method
def trigger_backup() -> Result:
    try:
        os.system(". /home/racso/vtts/bkup_new.sh")
        return Success("backup ran!")
    except:
        return Error("oh no! backup didn't run!")

@secret_method
def warren(name: str) -> Result:
    return Success(gen_text(name))

@public_method  
def cv() -> Result:
    with open("./cv/cv.txt", "r") as f:
        cv = f.read()
    return Success(cv)

@public_method
def ls() -> Result:
    ret = ", ".join(func.__name__ for func in public_methods)
    return Success(ret)

@public_method
def man(*args) -> Result:
    return Success("\n\n".join(manpage[arg] for arg in args))

@public_method
def website_info() -> Result:
    return Success("This website is implemented using https://terminal.jcubic.pl/ with a Python backend accessed via JSON-RPC. The server on which it is hosted runs Ubuntu, and Apache2 is used to serve the webpage.")

@secret_method
def pathitem(*args) -> Result:
    interpreted_args = InterpretedArgsIterable(*args)
    
    return Success(find(interpreted_args))


if __name__ == "__main__":
    serve()