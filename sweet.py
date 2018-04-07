
# coding: utf-8

# In[1]:


from hypothesis import assume, HealthCheck, Verbosity, settings

from unittest import TestLoader, TestResult, TestSuite, TestCase
from dataclasses import dataclass, field
from functools import partial
doctest = True
unittest = True
loader = TestLoader()
from types import ModuleType
from ast import NodeTransformer



# In[2]:


def discover(module='__main__', suite=None, *, doctest=doctest, unittest=unittest, loader=loader):
    from doctest import DocTestSuite
    if isinstance(module, str): module = __import__('importlib').import_module(module)
    if suite is None:
        return Sweet(module=module, doctest=doctest, unittest=unittest, loader=loader)    
    
    for name, object in vars(module).items():
        if unittest:
            if isinstance(object, type) and issubclass(object, TestCase):
                suite.addTests(loader.loadTestsFromTestCase(object)._tests)
            
            if callable(object) and not isinstance(object, (partial, type)):
                function_test_case = infer(object)
                if function_test_case:
                    suite.addTest(function_test_case)
                
    if doctest:
        suite.addTests(DocTestSuite(module)._tests)
    return suite


# In[3]:


def infer(object)->TestCase:
    """Use the hypothesis inference systems to create automated types from the annotations or ghetto typing.
    
    
    >>> def f(int, b:int): ...
    >>> test = infer(f)
    """
    from unittest import FunctionTestCase
    from inspect import getfullargspec
    from hypothesis import given, strategies as st, find
    spec = getfullargspec(object)
    annotations = dict(**spec.annotations)
    returns = annotations.pop('return', None)
    
    if not spec.args: return FunctionTestCase(object)
    
            
    if not (spec.defaults or spec.kwonlydefaults):
        annotations = {
            str: st.from_type(object) if isinstance(object, type) and getattr(object, '__name__', '') != 'object'
            else object if isinstance(object, st.SearchStrategy)
            else st.one_of(list(map(st.just, object)))
            for str, object in annotations.items()
        }
        if annotations:
            return FunctionTestCase(given(**annotations)(object))
            
            
    if (returns is not None) and callable(returns) ^ isinstance(returns, type) and len(annotations) is 1:
        return FunctionTestCase(partial(find, *annotations.values(), lambda x: returns(object(x))))


# In[4]:


class Result(TestResult):
    def __repr__(Result, *, str=""""""):
        if Result.errors: str += f"""\n{dict(Result.errors)}"""
        if Result.failures: str += f"""\n{dict(Result.failures)}"""
        return '\n'.join((super().__repr__(), str)).rstrip()


# In[5]:


@dataclass
class Sweet(TestSuite):
    """A TestSuite.
    """
    _tests: list = field(default_factory=list)
    module: __import__('types').ModuleType = field(default=__import__('__main__'))
    loader: TestLoader = field(default_factory=TestLoader, repr=False)
    result: TestResult = field(default_factory=Result)
    doctest: bool = True
    unittest: bool = True
    
    def __post_init__(Discover): 
        global doctest, unittest
        from importlib import import_module
        TestSuite.__init__(Discover)
        if isinstance(Discover.module, str): 
            Discover.module = import_module(Discover.module)
        if not Discover._tests:
            Discover.discover()  
        
    def discover(Discover): 
        return discover(module=Discover.module, suite=Discover, doctest=Discover.doctest, unittest=Discover.unittest)
    
    def run(Discover, result=None, debug=False):
        try: return super().run(result or Discover.result, debug=debug)
        except type('Quack', (BaseException,), {}): ...
        finally: Discover._tests = list(filter(bool, Discover._tests))


# In[6]:


settings.register_profile('sweet', settings(
        suppress_health_check=(HealthCheck.return_value,),
        verbosity=Verbosity.normal,))

settings.load_profile('sweet')


# In[7]:


@dataclass
class Testing(NodeTransformer):
    """Testing must be callable so it can be using as an {IPython.core.events.EventManager}
    >>> assert callable(Testing())
    """
    objects = list()
    def visit_FunctionDef(Testing, node): 
        """Identify FunctionDef and ClassDef as potentially testable objects.            
        
        >>> visitor = Testing()
        >>> assert visitor.visit(__import__('ast').parse('def f(): ...'))
        >>> assert visitor.objects
        """
        Testing.objects.append(node.name)
        return node
    
    visit_ClassDef = visit_FunctionDef
    
    def __call__(Testing):
        main, module = __import__('__main__'), ModuleType('__interactive')
        while Testing.objects:
            name = Testing.objects.pop(0)
            if hasattr(main, name): setattr(module, name, getattr(main, name))
        sweet = Sweet(module=module)
        if sweet._tests:
            print(repr(sweet.run()))


# In[8]:


def unload_ipython_extension(ip=None):
        ip = ip or get_ipython()
        ip.events.callbacks['post_run_cell'] = [object for object in ip.events.callbacks['post_run_cell'] if not isinstance(object, Testing)]


# In[9]:


def load_ipython_extension(ip=get_ipython()):
        object = Testing()
        ip.ast_transformers.append(object)        
        ip.events.register('post_run_cell', object)


# In[10]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python sweet.ipynb readme.ipynb')
    result = Sweet(module='readme').run()
    get_ipython().system('rm readme.py')
    print(result)
    print(Sweet(module=__name__).run(result))
    unload_ipython_extension()
    load_ipython_extension()

