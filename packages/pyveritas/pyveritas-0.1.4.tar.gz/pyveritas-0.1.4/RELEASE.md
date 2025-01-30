Set up a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Unix
venv\Scripts\activate     # For Windows
```

Install the requirements:

```bash
pip3 install -r dev-requirements.txt
```

Update the documentation:

```bash
sphinx-apidoc -o docs/ pyveritas
make html
```

Update the version number in the pyproject.toml file:

```toml
version = "x.x.x"
```

Build the distribution:

```bash
flit build
```

Publish the distribution:

```bash
flit publish
```


