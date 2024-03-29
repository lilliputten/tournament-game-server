<!--
 @since 2023.02.09, 16:49
 @changed 2023.07.12, 16:53
-->

# Tournament game backend server


## Client & server

Server repo: https://github.com/lilliputten/tournament-game-server

Client repo: https://github.com/lilliputten/tournament-game-client


## Questions file

Questions are stored in `questions.yaml` file in yaml format, in the next form:

```
questions:
  - question: 'Question 1'
    id: 'Test1'
    answers:
      - text: 'Answer text 1'
      - text: 'Answer text 2'
        correct: True
      - text: 'Answer text 3'
  - question: 'Question 2'
    answers:
      - text: 'Answer text 1'
        correct: True
      - text: 'Answer text 2'
```

See `questions.SAMPLE.yaml` for example.


## Build info (auto-generated)

- Version: 0.0.4
- Last changes timestamp: 2023.03.19, 01:29
- Last changes timetag: 230319-0129


## TODO

Describe used techologies & their relations.


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

Remote server: `https://tournament-game-build.march.team/` (with built app)

Use local flask server instance for local nextjs server development.


## Server

Server runs on python/flask platform.

TODO: Describe basic server functionality.


## Python venv maintenance

Server command for creating venv:

```
virtualenv -p python3 ~/.venv-py3.10-flask
source ~/.venv-py3.10-flask/bin/activate
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

