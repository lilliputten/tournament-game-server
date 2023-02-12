<!--
 @since 2023.02.09, 16:49
 @changed 2023.02.09, 16:49
-->

# MarchTeam backend server


## Build info (auto-generated)

- Version: 0.0.1
- Last changes timestamp: 2023.02.13, 01:15
- Last changes timetag: 230213-0115


## Install

Install all required node dependencies:

```
npm i
```

Initialize python virtual environment:

```
sh utils/venv-init.sh
```


## Start dev server

Acivate virtual environment:

On windows:

```
call .venv/Scripts/activate
```

On unix:

```
. ./.venv/Scripts/activate
```

Start local flask server (can be located in browser with `http://localhost:5000/*`, but mostly using for api requests):

```
npm run start
```

Or just:

```
flask run
```


## API

Basic api structure:

TODO: Describe api here (for specific server version)


## Server urls

Remote server: `http://march-team-flask-site.march.team/`


## Server

Server runs on python/flask platform.

TODO: Describe basic server functionality.


## Python venv maintenance

Server command for creating venv:

```
virtualenv -p python3 ~/.venv-py3-flask
source ~/.venv-py3-flask/bin/activate
pip install -r requirements.txt
```

Local script for venv creating and initialization:

```
sh utils/util-venv-init.sh
```

Local command for activate venv:

```
call .venv/Scripts/activate
source .venv/Scripts/activate
```


## Python dependencies

```
pip install PKGNAME
pip install -r requirements-general.txt -r requirements-dev-only.txt
pip freeze > requirements-frozen.txt
```

Use `utils/venv-init.*` scripts.

