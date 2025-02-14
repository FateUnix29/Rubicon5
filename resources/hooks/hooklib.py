#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                                                                                                                 ##
##                                   HookLib.py - Modify code of functions at runtime for modularity and 'mods'.                                   ##
##                                       Authored by Kalinite (https://github.com/FateUnix29, @kalthelunatic)                                      ##
##                                                                                                                                                 ##
##                                                                                                                                                 ##
##                                             Find it on GitHub: https://github.com/FateUnix29/HookLib                                            ##
##                                                                                                                                                 ##
#####################################################################################################################################################



# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #
### --                                                        Built-In Python Libraries                                                        -- ###
# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

# functools                                                               | Higher-order functions and operations on higher-order functions.
import functools as ft

# inspect                                                                 | Utilities for obtaining information about live objects.
import inspect

# re                                                                      | Regular expression operations. Oh boy.
import re

# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #
### --                                                            External Libraries                                                           -- ###
# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

# ...

# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #
### --                                                   Globals (Pre-Function Definitions)                                                    -- ###
# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

hooklib_tracked_functions = {}

# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #
### --                                                                Functions                                                                -- ###
# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

## Regular Functions ##

# None.

# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

## Decorators ##

def modular_fn(current_globals: dict):
    """A decorator that adds this function as a modifiable target for HookLib.<br>
    Think IL hooking.<br><br>
    
    NOTE: It is heavily recommended that this be the only decorator of a function, as extra decorators will confuse HookLib, unless the function is in the same file as these functions.<br>
    If you need a function with extra decorators, say, a Discord.py bot, just have the function call a function that's only decorated with modular_fn.<br>
    Alternatively, you may be able to declare the function with extra decorators *within* the function decorated with modular_fn. Unlikely, but possible."""

    def decorator(f):

        # We need to un-intent the source code until at least one line is touching the left margin.
        # Once at least one line is no longer indented, we must stop immediately to preserve indentations of say, function contents.

        # note: src will be in a different file thats importing this one
        try:

            src = inspect.getsource(f)

        except OSError:
            # If src is in a different file, we can't get the source code. This is a problem.
            #raise OSError("Tried to get source code of a function that is not in the same file.")

            # Let's try anyway.
            filename = inspect.getfile(f)
            print("If you see this, HookLib is unable to retrieve source code and is failing. See the docstring of `module_fn` for more information on how you should resolve this.\n"
                  "Any odd prints after this one are likely attempts to debug before just silently crashing.\n")
            print(filename)
            return

        hooklib_tracked_functions[f.__name__] = {
            "function": f,
            "source": src,
            "line_count": len(src.split('\n')),
            #"_return_value": None # No more globals!
        }


        if inspect.iscoroutinefunction(f):

            @ft.wraps(f)
            async def run(*args, **kwargs):

                src = hooklib_tracked_functions[f.__name__]["source"]

                split_src = src.split("\n")

                i_want_out = False

                while True:

                    for i in range(len(split_src)):

                        if not split_src[i].startswith(" ") and not split_src[i].startswith("\t") and split_src[i].strip() != "" and not i_want_out and not split_src[i].startswith("#"):
                            i_want_out = True
                            break

                        split_src[i] = split_src[i][1:]

                    if i_want_out:
                        break

                corrected_src = "\n".join(split_src)

                # This ensures that exec has a clean environment every single time.
                exec_globals = current_globals
                exec_locals = {}

                sanitized_src = re.sub(r"@modular_fn\(.*?\)\)", "", corrected_src)

                exec(sanitized_src, exec_globals, exec_locals)

                # Since exec_locals now has this function, let's try and call it via it's name:
                fn = exec_locals.get(f.__name__, exec_globals.get(f.__name__, exec_globals.get("hooklib_tracked_functions", {}).get(f.__name__, {}).get("function", None)))

                if not fn:
                    raise NameError(f"Function '{f.__name__}' was not found in the global (nor locals) scope.")

                return await fn(*args, **kwargs)

        else:

            @ft.wraps(f)
            def run(*args, **kwargs):

                src = hooklib_tracked_functions[f.__name__]["source"]

                split_src = src.split("\n")

                i_want_out = False

                while True:

                    for i in range(len(split_src)):

                        if not split_src[i].startswith(" ") and not split_src[i].startswith("\t") and split_src[i].strip() != "" and not i_want_out and not split_src[i].startswith("#"):
                            i_want_out = True
                            break

                        split_src[i] = split_src[i][1:]

                    if i_want_out:
                        break

                corrected_src = "\n".join(split_src)

                # This ensures that exec has a clean environment every single time.
                exec_globals = current_globals
                exec_locals = {}

                sanitized_src = re.sub(r"@modular_fn\(.*?\)\)", "", corrected_src)

                exec(sanitized_src, exec_globals, exec_locals)

                # Since exec_locals now has this function, let's try and call it via it's name:
                fn = exec_locals.get(f.__name__, exec_globals.get(f.__name__, exec_globals.get("hooklib_tracked_functions", {}).get(f.__name__, {}).get("function", None)))

                if not fn:
                    raise NameError(f"Function '{f.__name__}' was not found in the global (nor locals) scope.")

                return fn(*args, **kwargs)

        return run

    return decorator

# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #

def module(fn_name: str, line: int):
    """Use this function to modify a specified valid HookLib target.
    The function specified must be decorated with @modular_fn.

    NOTE: It is heavily recommended that this be the first decorator of any function you want to modify.
    If you do not do this, expect heavily undefined behavior.

    Additionally, line 0 starts at the first line after the function signature, including whitespace."""

    def decorator(f):

        fn_obj = hooklib_tracked_functions.get(fn_name)

        if not fn_obj:
            raise NameError(f"Function '{fn_name}' not found in tracked functions.")

        if not isinstance(line, int):
            raise TypeError(f"Line number '{line}' is not an integer.")

        # Get to work - First, the source code.
        fn_src = fn_obj["source"]
        fn_line_count = fn_obj["line_count"]
        fn_src_split = fn_src.split("\n")

        if line + 1 > fn_line_count or line < -fn_line_count:
            raise IndexError(f"Index out of range (line '{line}' is larger than the function being patched)")

        # Get the source code of our module.
        module_src = inspect.getsource(f)
        module_src_split = module_src.split("\n")

        skipped_line_count = 0

        banned_lines = [line for line in module_src_split if line.strip().startswith("@") or line.strip().startswith(f"def {f.__name__}(") or \
                        line.strip().startswith(f"async def {f.__name__}(")]

        # XOR the list with module_src
        module_src = "\n".join(line for line in module_src_split if line not in banned_lines)

        skipped_line_count = len(banned_lines)

        # Insert new module source code at the specified index.
        fn_src_split.insert(line + skipped_line_count, module_src)

        hooklib_tracked_functions[fn_name]["source"] = "\n".join(fn_src_split)
        hooklib_tracked_functions[fn_name]["line_count"] = len(fn_src_split)

        return f

    return decorator


# ++ ------------------------------------------------------------------------------------------------------------------------------------------- ++ #


if __name__ == "__main__":
    # Test.

    @modular_fn()
    def testing_fn(): # Line -1
        a = 5 # Line 0
        b = 6
        print("hello!")
        print(a)
        print(b)
        c = a + b
        print(c)
        return c

    @module("testing_fn", 6)
    def testing_fn_mod():
        def nested_function_testing(c):
            return c + 7

        c = nested_function_testing(c)

    print(hooklib_tracked_functions["testing_fn"]["source"])

    # attempt running it

    print(testing_fn())