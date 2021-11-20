
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"