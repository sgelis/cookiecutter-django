# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2023-02-11

### Changed

- Upgraded dependencies.
- Use Docker compose v2 in project's README.

## [2.1.0] - 2022-12-16

### Changed

- Updated Gulpfile to the latest syntax.

## [2.0.0] - 2022-12-16

### Added

- Angular client front-end.
- A `build:dev` Gulp task to avoid uglifying statics when developing.

### Changed

- Updated documentation.
- Updated dependencies.

### Fixed

- Display Django debug toolbar when running the project in Docker.
- Correct `Content-Type` for root project files (`robots.txt` and others).

## [1.0.0] - 2022-11-30

### Added

- Docker support.
- `.editorconfig` file (see [here](https://editorconfig.org/) for reference).

### Changed

- Updated documentation.
- Updated dependencies.

### Fixed

- Error in example environment variables.

### Removed

- PyCharm file watchers for front-end assets. They have been moved to the Gulp `watch` (or `dev`) task.
