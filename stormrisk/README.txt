You can check the progress of devolopment on our remote server, following the link: https://sido-dev.herokuapp.com/

OR create a local environment following the steps below:

1.	Clone the respiratory
2.	From main directory (sidoCheck) run: source sido/bin/activate
3.	Run: pip install -r requirements.txt
4.	Install posgresql following these steps: https://linode.com/docs/databases/postgresql/how-to-install-postgresql-on-ubuntu-16-04/
5.	run createdb cutcheck
6.	Go to the config file and change the USER and PASSWORD in line 11 to your postgres credentials/ SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/cutcheck'
7.	Now you can run the app locally with python run.py
8.	To run tests: python test.py