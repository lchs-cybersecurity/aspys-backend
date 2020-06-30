export SECRET_KEY=$(python -c "import os ; print(os.urandom(32))")
echo Set SECRET_KEY to $SECRET_KEY.
