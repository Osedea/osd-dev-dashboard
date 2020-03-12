# OSD Developer Dashboard

This is a Conky dashboard for developers

## Installation

```
git clone git@github.com:Osedea/osd-dev-dashboard.git osd-dev-dashboard
cd osd-dev-dashboard/
sudo ./install.sh
```

(Optional) delete the folder after installation
```
cd ../
rm -rf osd-dev-dashboard/
```

### Google Calendar integration

You will need to parameter your google account to allow access to gcalcli (https://github.com/insanum/gcalcli)

- Open the google developer console : https://console.developers.google.com/

- Make a new project for gcalcli

- Click "Enable API and services", then enable the google calendar API

- On the sidebar click Credentials

- Create a new Client ID. Set the type to Installed Application and the subtype to Other. You will be asked to fill in some consent form information, but what you put here isn't important. It's just what will show up when gcalcli opens up the OAuth website. Anything optional can safely be left blank.

- Go back to the credentials page and grab your ID and Secret.

- Create a file named .gcalclirc in ~/

- Fill it with your information

```
--client_id=xxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
--client_secret=xxxxxxxxxxxxxxxxxxxxxx
--defaultCalendar=YOUR_CALENDAR_NAME
```

### Gmail integration

You have to allow your google account to be accessed by the script, and generate some identifiers for it.

Please follow the steps 1 & 2 on this link :
https://developers.google.com/gmail/api/quickstart/python

You will have to place the generated client_secret.json in the src/modules/gmail/security/ folder.

### Weather integration

Register your own private API key on OpenWeatherMap to get weather data.

Place the API key in the config.ini file, in the WEATHER section.

#### City, if you're not in Montreal

Find the ID of your city and place it inside the template7 variable inside the conkyrc_weather file. http://bulk.openweathermap.org/sample/

### Github integration

- Go to your github tokens : https://github.com/settings/tokens
- Create a new token for osd-dev-dashboard
- Give it access to :
    - repo 
        - repo:status
        - repo_deployment
        - public_repo
        - repo:invite
    - notifications
    - user
        - read:user
        The others are not required, so leave them empty
- Create a .token file inside the src/modules/github/security/ folder
- Paste directly your token in there.

### Toggl integration

Go to your "Profile settings" in Toggl
Your API token is already there, waiting for you.
- Copy it.
- Create a new file named .toggl_token, in the src/modules/toggl/security/ folder.
- Paste directly your token in there.

### Network monitor integration

Nmap is required to scan the network devices, to install:
MacOS: brew install nmap
Linux: apt-get install nmap

## Usage

```
conky -c ~/.conky/conkyrc
```

## Development

Keep your installation folder, run the following to reload the configuration and kill running conky instances
```
./reload.sh
```

## License

The OSD Dev Dashboard is licensed under the terms of the GPLv3 license.

## Contributing

Contributions are welcome from anyone.

Please read CONTRIBUTING.md for guidelines on contributing to the OSD Dev Dashboard.
