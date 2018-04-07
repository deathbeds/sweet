
# testing is __Sweet__
    
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/deathbeds/sweet/master?filepath=readme.ipynb) 
   
__Sweet__ is an easy way to test interactive code. It combines unittest, doctest, and hypothesis to promoting better code health.


```python
    from sweet import Sweet
```


```python
    def test_no_params():
        """This function is tested because it has no parameters.  It is executed using FunctionTestCase

        >>> assert True

        The docstring is also tested.
        """
        assert True
```


```python
    if __name__ == '__main__':
        !jupyter nbconvert --to markdown readme.ipynb
        result = Sweet().run()
        print(result)
        print(Sweet(module='sweet').run(result))
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1004 bytes to readme.md
    <unittest.result.TestResult run=2 errors=0 failures=0>
    <unittest.result.TestResult run=4 errors=0 failures=0>

