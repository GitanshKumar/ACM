echo "BUILD START"
pip install -r requirements.txt
pip3 install db-sqlite3
python3.9 manage.py collectstatic
echo "BUILD END"