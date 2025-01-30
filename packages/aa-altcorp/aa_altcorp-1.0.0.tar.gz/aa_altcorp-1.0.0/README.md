# Example plugin app for Alliance Auth - LAWN Version

This is an example plugin app for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) (AA) that can be used as starting point to develop custom plugins.
It is a modified version of [allianceauth-example-plugin](https://gitlab.com/ErikKalkoken/allianceauth-example-plugin), that has been modified to hold our preffered setup.
The instructions have been modified to fit our use case.

## Features

- The plugin can be installed, upgraded (and removed) into an existing AA installation using PyInstaller.
- It has it's own menu item in the sidebar.
- It has one view that shows a panel and some text
- Comes with CI pipeline pre-configured

## Installing

Structure Timers is a plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth). If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

This app requires [AA-Discordbot](https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot) in order to DM corp ceo's about their compliance. It is not mandatory, but the DM's will not function if it is not installed.

```bash
pip install aa-altcorp
```

Configure your Auth settings (`local.py`) as follows:

- Add `'structuretimers'` to `INSTALLED_APPS`
- Add the following lines to your settings file:

```python
AC_ALT_ALLIANCE = 123456 # alt alliance ID
AC_WEBHOOK = "https://discord.com/" # webhook required for manager notifications
CELERYBEAT_SCHEDULE['altcorp_update'] = {
    'task': 'altcorp.update_corp_requests_for_alliance(',
    'schedule': crontab(minute=0, hour=3),
    'apply_offset': True,
}
```

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for Auth

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your Auth settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name | Description | Default
-- | -- | --
`AC_ALT_ALLIANCE`| The ID of the alt alliance. | `123456`
`AC_ALLIANCE_IDS`| A list of alliance ID's. Toons in an alt corp must have their users main character as part of one of theses alliances. Blank ignores this check and will allow anyone to be in an alt corp | `[]`
`AC_WEBHOOK`| Webhook for sending manager notifications` | ``
`AC_REVOKE_DAYS`| Days of non compliance before the app tells you to remove a corp from alt alliance | `7`
`AC_IGNORE_CORPS`| A list of corps in the alt alliance to ignore. Use to ignore executor or other corps that don't require checks. | `[]`

## Permissions

Here are all relevant permissions:

Codename | Description
-- | --
`general - Can access this app and see timers` | Basic permission required by anyone to access this app and request an alt corp.
`general - Can manage alt corp requests` | Users with this permission can manage requests.
