import re
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import pycuda.autoinit


def preprocess_module(module: str, args: dict, no_extern_c=False):
    '''Replaces special markers <<...>> in cuda source code with
       values provided in the args dictionary.

    '''
    def repl(match):
        contents = match.group(1)
        if contents in args:
            return str(args[contents])
        else:
            raise Exception("Failed to replace a placeholder in the source code")


    module = re.sub('<<([a-zA-Z][\w]*?)>>', repl, module)
    return SourceModule(module, no_extern_c=no_extern_c)


def load_cuda_modules(**args):
    with open("cumsum.cu", "r") as f:
        cumsum = f.read()

    with open("resample.cu", "r") as f:
        resample = f.read()

    return {
        "cumsum": preprocess_module(cumsum, args),
        "resample": preprocess_module(resample, args, no_extern_c=True),
    }
