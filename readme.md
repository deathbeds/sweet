
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
        
    ct = 0
    def when_there_are_annotations(x: int):
        global ct
        ct +=1
        return x

    def after_hypothesis():
        global ct
        assert ct > 0
```


```python
    if __name__ == '__main__':
        !jupyter nbconvert --to markdown readme.ipynb
        result = Sweet().run()
        print(result)
        print(Sweet(module='sweet').run(result))
```
