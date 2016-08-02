# plivo

#To run locally, do the usual:

Create Python 2.7 virtualenv

Activate new virtualenv

#Install dependencies:

pip install -r requirements.txt

Alternatively use the make task

make install

#Edit database settings:

Edit settings.py database credentilas according to your environment

Dump database files if required
psql -d {user} {database} < dump.pgsql

#Edit redis settings:

Edit settings.py redis credentials according to your environment

#Finally run the server:

make run

Use curl / web service tools to call rest apis for manual testing

For example,

curl http://127.0.0.1:8000/inbound/sms -X POST  -H "Content-Type: application/json" -d '{"to": "4924195509198", "frm":"4412244594268", "text":"STOP"}' -u plivo1:20S0KPNOIM

#Running the tests:

Tests uses django rest framework test suites

make test

or simply the usual test management command:

./manage.py test plivoapis

If issues in running tests
then may have to fix migrations of tables by
makemigrations plivoapis
migrate
