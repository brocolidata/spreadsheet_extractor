# Spreadsheet Extractor Development 

## Manage project using Poetry
We are using [Poetry](https://python-poetry.org/docs/) to package the libaries and manage their dependencies.
All settings are defined in a `pyproject.toml` and all dependencies locked in a `poetry.lock`.

## Work with this package
- You must be inside the Dev Container
- You must activate the Python Virtualenv created by Poetry. To display the path of your Python virtualenv, run `poetry env info -p`

## Manage dependencies

### Add a new dependency
```
poetry add a_pip_installable_package
```
### Install dependencies
```
poetry install
```
### Update dependencies
```
poetry update
```
### Remove a dependency
```
poetry remove a_pip_installable_package
```

## Setup tests

In order to run tests in the Virtualenv created by Poetry, you need to set the Visual Studio Code Python interpreter path to the path of the Poetry Python interpreter :

1. Run `poetry env info` and copy the value of `Path` key inside the `Virtualenv` section.
2. Open any `.py` file and click on the Python version in the ribbon (bottom of the window, see image below)
![Python ribbon image](https://img-blog.csdnimg.cn/20190416163401771.png)
3. Click on `+ Enter interpreter path...`, paste the Poetry Python interpreter path you copied in **step 1**, and hit Enter
![Select interpreter image](https://code.visualstudio.com/assets/docs/python/environments/interpreters-list.png)

Your Visual Studio Code environment is now configured to run Python tests in the Virtualenv created by Poetry.