
# testing is __Sweet__
    
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

    <sweet.Result run=2 errors=0 failures=0>



```python
    ct = 0
    def when_there_are_annotations(x: int):
        global ct
        ct +=1
        return x
```

    <sweet.Result run=1 errors=0 failures=0>



```python
    def after_hypothesis():
        global ct
        assert ct > 0
```

    <sweet.Result run=1 errors=0 failures=0>



```python
    if __name__ == '__main__':
        !jupyter nbconvert --to markdown readme.ipynb
        from sweet import Sweet
        result = Sweet().run()
        print(f"""The readme shows the {result}""")
        print(f"""and the source shows the {Sweet(module='sweet').run(result)}""")
        print("🏆")
```
