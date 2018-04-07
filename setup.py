__import__('setuptools').setup(
    name="sweet",
    version="0.0.1",
    author="deathbeds", author_email="tony.fast@gmail.com",
    description="Interactive notebook testing.", 
    license="BSD-3-Clause",
    install_requires=['dataclasses', 'hypothesis'],
    include_package_data=True,
    packages=__import__('setuptools').find_packages(),
)