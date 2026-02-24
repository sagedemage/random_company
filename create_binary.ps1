pipenv run pyinstaller --noconfirm .\main.py
cp data dist/main -Recurse
cp images dist/main -Recurse