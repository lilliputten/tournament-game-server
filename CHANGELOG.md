<!--
@changed 2022.04.03, 21:46
-->

# Changelog

- 2022.04.03, 21:46 -- Mail sending minor changes: added `legalOrigins` hosts for `localhost` only in dev mode, updated mail message styles, tried to add links for favicons (in message body).
- 2022.04.02, 18:26 -- Mail message: added formatting, content preview (as plain body), footer.
- 2022.04.02, 17:55 -- Excplicitly set encoding as `utf-8` for config helper methods `readFiletoString` and `updateConfigWithYaml`. Specified parameters `encoding='UTF-8'`` and `ensure_ascii=False` for json datafile opening in `RequestsStorage`.
- 2022.04.02, 17:13 -- Send mail using `smtp.fullspace.ru` server and account `site@march.team`.
- 2022.04.02, 16:16 -- Added more sophisticated session processng. Session tokens checks at start with checkToken=False flag. Other api methods must process verification with checkToken=True (default) value.
- 2022.04.02, 16:13 -- Used march.team.realty google account for mail sending. Disabled actual mail sending for dev server.
- 2022.03.29, 23:23 -- Added request origin checks for `blueprintRequests` module api.
- 2022.03.29, 23:20 -- Use `Token` instead `sessionId`. Added api methods verificartion for `origin` header and compare it for `config.legalOrigins`. Removed static app serve functinality (slow and buggy).
- 2022.03.28, 15:35 -- Using production build.
- 2022.03.28, 15:32 -- v.0.0.2: Renamed project from `march-team-back` to `march-team-flask-site`.
- 2022.03.28, 00:03 -- Moved mail address constants to config, added dev-mode mail sending only to bcc addresses.
- 2022.03.27, 23:43 -- Advanced errors processing (returns such request data as url, protocol, method). check request data for `requests/add` request.
- 2022.03.27, 21:37 -- Moved core server code to `blueprintCoreSite` and `app` modules. Support for static spa app build pages.
- 2022.03.27, 19:38 -- Added `html-app*` folder support for spa app bundle.
- 2022.03.26, 04:47 -- Using CORS (Flask-Cors).
- 2022.03.26, 02:28 -- Minor changes (config, auto timestamps in RequestsStorage, api password).
- 2022.03.26, 02:08 -- Configuration for google mail server and mail message styles.
- 2022.03.26, 01:16 -- Added mail sending functionality.
- 2022.03.25, 23:05 -- Minimal api (root, records), requests database (using tinydb).
- 2022.02.27, 02:45 -- RecordsStorage using TinyDB (fully worked code & tests).
- 2022.02.26, 05:31 -- Using TinyDB for data engine in `RecordsStorage` (in progress: basic methods and tests are ready).
- 2022.02.24, 00:55 -- v.0.0.5: Moved `lib` to `core/lib` scope (extract to shared submodule in future). Using pylint as project-wide linter (fixed all linter issues).
- 2022.02.23, 00:24 -- RecordsStorage: remove outdated records during findng (in `processRecords`), added metod for rorced remove of outdated records (`removeOutdatedRecords`).
- 2022.02.22, 02:30 -- RecordsStorage, Record: Basic records and records storage routines and tests.
- 2022.02.21, 23:06 -- Test support utilities (`getTrace`). Restuctured utils module.
- 2022.02.15, 06:12 -- v.0.0.4: Created automatic tests & linters for python code.
- 2022.02.15, 03:53 -- Helper modules moved to lib folder.
- 2022.02.14, 04:45 -- Experimental sessions support.
- 2022.02.12, 04:52 -- Implemented simple socket.io tests. Relocated cdn files.
- 2022.02.12, 02:58 -- v.0.0.3: Restructured server application (extracted several blueprint modules for different apis).
- 2022.02.08, 06:19 -- Device server shot creation method.
- 2022.02.08, 01:51 -- Fixed logger async (non-atomic) print issuesm server: starting only once (skip first initialization in debug mode, when app is initialized twice), templates: temporarily removed unused assets.
- 2022.02.07, 22:33 -- Local device server start scripts (via gunicorn, see `utils/rpi-start-server.sh`).
- 2022.02.07, 03:24 -- Readme venv instructions, disable basic auth in htaccess.
