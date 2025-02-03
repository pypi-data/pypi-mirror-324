# Desription
_drf_bf_protect_ X is the rudimentary implementation of a system for the Django REST framework to slow down a bruteforce attack by blocking logins. To not cut of users from the application, it uses a device cookie that is set on successfull login, to allow users to login from trusted devices even if their login is blocked.

# Special Features
* A login is blocked
  * ... regardless of whether it really exists.
  * ... if the attemps comes from different devices.
* The login from a trusted device of the user is still available.

If a user logins successfully a device cookie is created and saved through the browser. This identifies the device a trusted one on logins in the future.
So if a brute force attack agains that username starts, it will be locked after several attemps. The user is not longer able to logi. _Except_ from a trusted device. There is a different counter for attemps with a valid device cookie.
If the login with a valid device cookie fails several times, it is set invalid. So a valid device cookie for a user does not allow a brute force attack.

# Installation and configuration
## Install
Install the module using pip or add it to your requirements.
```
pyton -m pip install drf-bf-protect
```
## Add to settings.py
Add the app to your INSTALLED_APPS:
```python
INSTALLED_APPS  = [
# ...
'drf_bf_protect',
# ...
]
```
The following entry configures the module:
```python
BF_PROTECT_SETTINGS  = {
    "cookie_name": "did",
    "failures_before_lock": 5,
    "lock_time_minutes": 30,
    "reset_failure_count_seconds": 300,
    "backend": "drf_bf_protect.backend.DatabaseBackend"
}
```
**cookie_name**: The name of the cookie in the broweser. (default: "did")
**failures_before_lock**: How many attemps to a username, before the login is blocked (default: 5)
**lock_time_minutes**: How many minutes is the username blocked. After this time a login attemp from an untrusted device is possible again. (default: 30)
**reset_failure_count_seconds**: The time window in seconds in which the failed logins must appear to lock the login (default: 300)
**backend**: Allows to specify another backend to handle the procedure. In the project exists only the DatabaseBackend at the moment.

So the default configuration from the example means: If a user successfully logs in, a cookie with the name '_did_' is set. If for a username fails _5_ logins in _300_ seconds this username is locked for _30_ minutes.


Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.

## Decorate login view
To make sure that the login is protected, we decorate the login view you are using. It is possible that you need to create your own login view to make that possible.
```python
from  drf_bf_protect.decorators  import  bf_protect

@bf_protect(fieldname='username', case_sensitiv=True)
def your_login_view(request, *args, **kwargs):
   . ..
```
**fieldname**: The name of the field of the incoming data. (default: 'username')
**case_sensitiv**: If True, the username is interpreted case_sensitiv ('SpamHam' != 'spamham'). If set to False it is not ('SpamHam' = 'spamham'). **This is important!** Be sure your configuration here matches the configuration of you app. If there names are not case sensitiv but here they are, a brute force attack is possible to use different uppercase letters.

# Administration
There are entries in Django's admin area.
To unlock a user, delete its entry from the Locks there.
