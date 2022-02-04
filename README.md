# Fear No Factor
An online app to help students learn reverse multiplication, i.e. factoring.

## Installation
Fear No Factor is a Flask app. It is deployed as a WSGI application.

It is recommended that you use a virtual Python environment. The required dependencies are included in [requirements.txt](requirements.txt), and may be install with the command `pip install -r requirements.txt`.

### Setup config.py
In the main directory (i.e. in the same folder as [initialize_database.py](initialize_database.py), create a file called `config.py`. Add the following contents, substituting in your own credentials:
```
DB_USER = 'myUser'
DB_PASSWORD = 'myPassword'
DB_IP = '000.000.000.000'
DB_NAME = 'myDatabase'
GOOGLE_CLIENT_ID = 'client-id-from-google'
GOOGLE_CLIENT_SECRET = 'client-secret-from-google'
```

### Setup Google Sign-In
Fear No Factor uses Google Sign-In. You will need to set up a project in the Google developers console and include the client id and secret in the config file described above.

Once you have created a project, generate OAuth 2.0 credentials. Add the hosting domain to the Authorized Javascript origins list. Add the hosting domain with the suffix `/login/callback` to the Authorized redirect URIs list.

### Setup Database
Fear No Factor requires a MySQL database. Once you have the database user, password, ip, and name in the config file, simply run `python3 initialize_database.py` to setup the database.

### Deploy
At this point, the installation of Fear No Factor becomes dependent on your production environment. The included `run.py` is only for debugging, and should not be used for final deployment. Some options for deploying can be found [here](https://flask.palletsprojects.com/en/2.0.x/deploying/). Installation is also possible on cPanel, as described [here](https://docs.cpanel.net/knowledge-base/web-services/how-to-install-a-python-wsgi-application/).
  
