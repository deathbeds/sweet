
# testing is __Sweet__
    
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/deathbeds/sweet/master?filepath=readme.ipynb) 
   
__Sweet__ is an easy way to test interactive code. It combines unittest, doctest, and hypothesis to promoting better code health.


```python
    if __name__ == '__main__':
        %reload_ext sweet
```


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


```python
    def after_hypothesis():
        global ct
        assert ct > 0
```


```python
    if __name__ == '__main__':
        !jupyter nbconvert --to markdown readme.ipynb
        from sweet import Sweet
        result = Sweet().run()
        print(f"""The readme shows the {result}""")
        print(f"""and the source shows the {Sweet(module='sweet').run(result)}""")
        print("🏆")
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1119 bytes to readme.md
    The readme shows the <sweet.Result run=4 errors=0 failures=0>
    and the source shows the <sweet.Result run=8 errors=0 failures=0>
    🏆

