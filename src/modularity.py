import functools as ft
import inspect, re, asyncio

registered_functions = {}

ret = None

# DECORATOR: @modular

    # What we need to do:
    # Get every single line of a function marked with @modular as a string separated by newlines
    # Put in registered_functions: "func_name": {"func": (function object), "src": (src), "line_count": (len(src))}

def modular(async_: bool = True, no_call: bool = False, globals_: dict = {}):
    """
    A decorator marking a function as modular.
    
    When applied to a function, it registers the function along with its source code
    in the global dictionary `registered_functions`.
    """

    if not async_:
        def decorator(f):
            # Get the function's source code
            src = inspect.getsource(f)
            
            # Count the number of lines in the function
            line_count = len(src.split('\n'))
            
            # Store the function and its details in the dictionary
            registered_functions[f.__name__] = {
                "func": f,
                "src": "\n".join([line for line in src.split("\n") if not line.strip().startswith("@modular") and not line.strip().startswith("@module")]),
                #"src": src,
                "line_count": line_count
            }

            # Create ANOTHER function that executes the function source code as a string instead of the real deal
            @ft.wraps(f)
            def f2(*args, **kwargs):
                print("f2")
                global ret
                #nonlocal f
                #ret = "test"
                # I am aware this is an extremely dangerous call.
                # Unfortunately, there is no way to circumvent it.
                # Any 'modularity' system is inherently dangerous if misused.
                # It's up to the user to ensure that the modules they're inserting into the program are safe to run.
                strargs = str(*args)
                strkwargs = str(**kwargs)
                strtotal = f"{strargs}{", " if strargs.strip() != "" else ""}{strkwargs}"

                exec(f"{registered_functions[f.__name__]["src"]}{f'\nret = {f.__name__}({strtotal})' if not no_call else ''}", globals_, globals_)
                return ret
            return f2
        return decorator

    else:
        def decorator(f):
            # Get the function's source code
            src = inspect.getsource(f)
            
            # Count the number of lines in the function
            line_count = len(src.split('\n'))
            
            # Store the function and its details in the dictionary
            registered_functions[f.__name__] = {
                "func": f,
                #"src": [line for line in src if not line.startswith("@")],
                "src": "\n".join([line for line in src.split("\n") if not line.strip().startswith("@modular") and not line.strip().startswith("@module")]),
                "line_count": line_count
            }


            # Create ANOTHER function that executes the function source code as a string instead of the real deal
            @ft.wraps(f)
            async def f2(*args, **kwargs):
                print("f2")
                global ret
                #nonlocal f
                #ret = "test"
                # I am aware this is an extremely dangerous call.
                # Unfortunately, there is no way to circumvent it.
                # Any 'modularity' system is inherently dangerous if misused.
                # It's up to the user to ensure that the modules they're inserting into the program are safe to run.
                strargs = ", ".join(*args)
                strkwargs = ", ".join(f'{str(k)}={str(v)}' for k, v in kwargs.items())
                strtotal = f"{strargs}{", " if strargs.strip() != "" else ""}{strkwargs}"
                wrapfn = f"""async def wrapper(*args, **kwargs):
    global ret
    ret = await {f.__name__}({strtotal})
    return ret"""
                exec(f"{registered_functions[f.__name__]["src"]}{f'\n{wrapfn}' if not no_call else ''}", globals_, globals_)
                return ret
            return f2
        return decorator

# DECORATOR: @module
def module(function_name: str, line: int):
    """Mark this function as a module. Modules modify the source code of other functions.
    
    NOTE: If your module is decorated, this MUST be the first decorator. That way, the other decorators run before this one.
    If you do not do this, expect heavily undefined behavior.
    
    NOTE 2: Source code of modular functions includes their decorators and signatures. ``line`` probably shouldn't be 0.
    
    NOTE 3: Other modules' line numbers will have to account for this one adding lines."""

    #print("facstart")
    def decorator(f):
        #print("wrapstart")
        # Grab this function's dict, or, well, try.
        func_obj = registered_functions.get(function_name)

        if not func_obj:
            raise NameError(f"Function '{function_name}' not found in registered module functions.")

        # Verify the type of line.
        if not isinstance(line, int):
            raise TypeError(f"Line number '{line}' is not an integer.")

        # Get to work - First, the source code.
        func_src = func_obj["src"]
        func_line_count = func_obj["line_count"]
        func_src_split = func_src.split("\n") # Split it into a list of lines.

        if line + 1 > func_line_count or line < -func_line_count:
            raise IndexError(f"Index out of range (line '{line}' is larger than the function being patched)")

        # Get the source code of our module.
        module_src = inspect.getsource(f)
        #module_src = re.sub(r'^\s*(?:@[\w\s,]+)?\s*', '', module_src)
        #module_src = re.sub(r'^def\s+\w+\s*\([^)]*\)\s*:', '', module_src)
        module_src = "\n".join(line for line in module_src.split("\n") if not line.strip().startswith("@") and not line.strip().startswith(f"def {f.__name__}("))
        #print(module_src)

        # Insert new module source code at the specified index.
        func_src_split.insert(line, module_src)

        #print("\n".join(func_src_split))
        #print(func_src_split) # DEBUG

        registered_functions[function_name]["src"] = "\n".join(func_src_split)
        registered_functions[function_name]["line_count"] = len(func_src_split)
    #print("facend")
    return decorator

#@modular()
#def somefunc():
#    """bla bla"""
#
#    # We should be getting all of the lines in this function
#    a = 1
#    b = 2
#
#    return a + b
#
#@module("somefunc", 7)
#def somefunc_mod():
#    # ha ha ha ha ha ha ha
#    b = 3
#
#    def funny():
#        print("funny")
#
#    funny()
#
#print(somefunc())
#print(registered_functions)