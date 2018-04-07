
# coding: utf-8

# In[1]:


from hypothesis import assume, HealthCheck, Verbosity, settings

from unittest import TestLoader, TestResult, TestSuite, TestCase
from dataclasses import dataclass, field
from functools import partial
doctest = True
unittest = True
loader = TestLoader()


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


@dataclass
class Sweet(TestSuite):
    """A TestSuite.
    """
    _tests: list = field(default_factory=list)
    module: __import__('types').ModuleType = field(default=__import__('__main__'))
    loader: TestLoader = field(default_factory=TestLoader, repr=False)
    result: TestResult = field(default_factory=TestResult)
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


# In[5]:


settings.register_profile('sweet', settings(
        suppress_health_check=(HealthCheck.return_value,),
        verbosity=Verbosity.normal,))

settings.load_profile('sweet')
def load_ipython_extension(ip=None):
    ...


# In[8]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python sweet.ipynb readme.ipynb')
    result = Sweet(module='readme').run()
    get_ipython().system('rm readme.py')
    print(result)
    print(Sweet(module=__name__).run(result))

