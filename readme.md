
# testing and typing is __Sweet__
    
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/deathbeds/sweet/master?filepath=readme.ipynb) 
   
__Sweet__ is an easy way to test interactive code. It combines unittest, doctest, and hypothesis to promoting better code health.


```python
    if __name__ == '__main__':
        %reload_ext sweet
```

Because creating a function or class should do more than create a name.


```python
    def test_no_params():
        """This function is tested because it has no parameters.  It is executed using FunctionTestCase

        >>> assert True

        The docstring is also tested.
        """
        assert True
```

    <sweet.test.Result run=2 errors=0 failures=0>



```python
    ct = 0
    def when_there_are_annotations(x: int):
        global ct
        ct +=1
        return x
```

    <sweet.test.Result run=1 errors=0 failures=0>



```python
    def after_hypothesis():
        global ct
        assert ct > 0
```

    <sweet.test.Result run=1 errors=0 failures=0>


# Interactive typing 

Using [__monkeytype__]()


```python
    %load_ext sweet.typing
    def f(x):
        return str(x)
    %typing
    f(10)
    f(10.)
    f('asdf')
    f(__import__('pandas').util.testing.makeDataFrame())
    after_hypothesis()
    %typing readme.pyi
    __import__('IPython').display.Pretty(filename='readme.pyi')
```

    The sweet.typing extension is already loaded. To reload it, use:
      %reload_ext sweet.typing





    from pandas.core.frame import DataFrame
    from typing import Union
    
    
    def after_hypothesis() -> None: ...
    
    
    def f(x: Union[float, DataFrame, str, int]) -> str: ...



# Developer.


```python
    if __name__ == '__main__':
        !jupyter nbconvert --to markdown readme.ipynb
        from sweet import Sweet
        result = Sweet().run()
        print(f"""The readme shows the {result}""")
        print(f"""and the source shows the {Sweet(module='sweet').run(result)}""")
        print("🏆")
```
