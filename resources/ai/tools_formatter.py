import inspect

def add_tool(fn: callable, args: dict[str, str] | None = None, **kwargs) -> dict:
    """Add a tool. `fn` is expected to be some form of callable.
    
    `args` is a dictionary with the argument names being the key and their descriptions being the value.
    Example: ``{"arg_x": "This is argument X."}``
    If an argument is found in the function signature but not given a description in args, it's description will be set to 'No info.'
    
    Returns an object representing the generated tool.
    
    If needed, you may provide a "type" kwarg to the function to override the default of 'function'."""

    tooltype = kwargs.get("type", "function") # Get the type.

    fn_info = inspect.signature(fn)
    fn_name = fn.__name__
    fn_desc = fn.__doc__ or "No description."
    fn_params = fn_info.parameters

    param_vals = list(fn_params.values())

    f_param_objs = {
        "type": "object",
        "properties": {},
        "required": []
    }

    param_type_map = {"str": "string", "int": "integer"}

    for param in param_vals:
        f_param_obj = {}

        param_name = param.name
        param_type = param.annotation.__name__ if hasattr(param.annotation, '__name__') else 'unknown'

        #print(param_type)
        #print(param_name)
        #print(param)
        #print(param.annotation)

        param_req = param.default is not None
        #print(param_req, param.default)
        
        if args is not None:
            param_doc = args.get(param_name, "No info.") 
        
        else:
            param_doc = "No info."

        f_param_obj["type"] = param_type_map.get(param_type, param_type)

        if param_doc:
            f_param_obj["description"] = param_doc
        
        else:
            f_param_obj["description"] = "No info."
        
        f_param_objs["properties"][param_name] = f_param_obj

        if param_req:
            f_param_objs["required"].append(param_name)
    
    final_f_obj = {
        "fn": fn,
        "struct": {
            "type": tooltype,
            "function": {
                "name": fn_name,
                "description": fn_desc,
                "parameters": f_param_objs
            }
        }
    }

    return final_f_obj