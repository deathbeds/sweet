
# coding: utf-8

# dynamically types interactive code.
# 
# `sweet.typing` uses [Instagram's](https://github.com/Instagram/MonkeyType) to trace function calls
# in a running Jupyter instance or `__import__('__main__')`.  
# 
# The original is a [gist](http://nbviewer.jupyter.org/gist/tonyfast/81a14656f82e7aa31044c7fc5b1d4494).

# In[1]:


from monkeytype.tracing import CallTraceLogger as Logger, trace_calls
from monkeytype.stubs import build_module_stubs_from_traces
DUNDER = '__%s__'
from pathlib import Path
tracer = None


# In[2]:


class Tracer(Logger):
    def stubs(logger, modules=None, main=True): 
        modules = modules or []
        if main: 
            modules += [DUNDER%'main', 'main']
        stubs = build_module_stubs_from_traces(logger.data, True)
        return '\n'.join(stubs.get(module).render() for module in modules if stubs.get(module))

    def __enter__(Logger): 
        global __name__
        Logger.name = __name__
        if __name__ == '__main__':
            __name__ = 'main'
        Logger.ctx = trace_calls(Logger)
        Logger.ctx.__enter__()
        return Logger

    def __exit__(Logger, *args, **kwargs): 
        global __name__
        __name__ = Logger.name 
        Logger.ctx.__exit__(*args, **kwargs)    

    def __init__(Logger, data=None): 
        super().__init__()
        Logger.data, Logger.traces = None or [], []

    def log(Logger, trace): 
        if trace.func.__module__ in ('__main__', 'main'):
            Logger.traces.append(trace)

    def flush(Logger): 
        Logger.traces = Logger.data.extend(Logger.traces) or []


# # IPython magic.

# In[3]:


def typing(line, cell=None):
    global tracer

    if cell:
        tracer = Tracer()
        tracer.__enter__()
        get_ipython().run_cell(cell)

    elif not line.strip():
        tracer = Tracer()
        return tracer.__enter__()

    tracer.__exit__(None, None, None)
    if all(map('.'.__eq__, line.strip())): print(tracer.stubs())
    else: Path(line.strip()).write_text(tracer.stubs())


# In[4]:


def load_ipython_extension(ip=__import__('IPython').get_ipython()):
    ip.register_magic_function(typing, 'line_cell')

def unload_ipython_extension(ip=__import__('IPython').get_ipython()):
    ...


# In[6]:


if __name__ == '__main__':
    print('✅🚫'[bool(__import__('doctest').testmod().failed)])
    get_ipython().system('jupyter nbconvert --to python typing.ipynb')
    load_ipython_extension()
#     !source activate p6 && pytest tests/test_typing.ipynb


# In[7]:


if __name__ == '__main__':
    def f(x):
        return str(x)
    get_ipython().run_line_magic('typing', '')
    f(10)
    f(10.)
    f('asdf')
    f(__import__('pandas').util.testing.makeDataFrame())
    get_ipython().run_line_magic('typing', '.')

