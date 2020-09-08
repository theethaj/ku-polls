# Kasetsart Polls

Web application for conducting online polls and surveys.

## Project Documents

- [Requirements](../../wiki/Requirements)
- [Vision Statement](../../wiki/Vision%20Statement)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)

## Installation

1. Access `ku-polls` directory.
2. Install required packages. <pre class=output>pip install -r requirements.txt</pre>
3. Create `.env` in the root directory for setting configurations (`SECRET_KEY` and `DEBUG`).
4. Create the database. <pre class=output>py manage.py migrate</pre>

## Running

1. Access `ku-polls` directory.
2. Run server. <pre class=output>py manage.py runserver</pre>
