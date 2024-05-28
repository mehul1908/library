
echo "BUILD END"
python3.10 -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"
