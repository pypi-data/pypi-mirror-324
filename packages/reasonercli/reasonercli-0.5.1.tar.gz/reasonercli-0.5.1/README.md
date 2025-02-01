
# Reasoner CLI

## Local development

To run locally:
```
uv run python -m src.reasoner.cli upload --path=/path/to/docs
```

## Building for pip
```
uv pip sync pyproject.toml
uv run python -m build
uv run pip install --editable .

# this will install into a temporary location e.g. /Users/username/.pyenv/versions/3.12.7/bin/reasoner
```

## Publishing to pypi
```
python3 -m build

# publish onto pypi
python3 -m twine upload dist/*

# publish onto testpypi
python3 -m twine upload --repository testpypi dist/*

# to install via testpypi
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple reasonercli
```

## Building standalone executable
```
uv pip sync pyproject.toml
uv run pyinstaller --clean --onefile --name reasoner entry.py

cd dist
./reasoner
```

## Testing with older versions of python
```
pipenv --python 3.8 shell
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple reasonercli
reasonercli auth
```
