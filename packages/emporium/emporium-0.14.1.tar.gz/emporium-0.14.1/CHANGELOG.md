# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added type hints for the most of the simple methods `list`, `substore` and
  `location`.
- Added `remove` method to abstract interface. Add implementation for the
  `InMemoryStore` and throw `NotImplementedError` for all others.
- Added `clear` method that removes all files in the store. Only works for
  `InMemoryStore`.

### Changed

- Moved the project to PDM and updated the structure.
- Changed `Store` to be the abstract interface, instead of just a type alias of
  `AbstractStore`.

## [0.12.0] - 2021-01-14

### Changed

- Have `LocalStore`, `InMemoryStore` and `RemoteStoreS3` throw `NoSuchFile`
  exceptions when the file to read does not exist, to make it easier for clients
  to deal with this case generically.

## [0.11.0] - 2021-01-13

### Added

- Add `Cached` decorator that writes to the first store, but updates the second
  store on read, and prefers reading from the second store. The second store
  functions as a cache for the first one.

## [0.10.0] - 2020-11-09

### Added

- Add `Store` as an alias for `AbstractStore` for cleaner type signatures.

## [0.9.0] - 2020-09-09

### Added

- Add list() method for GCS. This method lists the entries that are in the
  store.

## [0.8.4] 2020-09-09

### Fixed

- Pass on the domain (S3) and url (GCS) when creating the substore

## [0.8.3] - 2020-06-29

### Fixed

- Wrap context manager directly, instead of using a contextmanager decorator and
  a yield statement. The latter leads to issues when using the wrapping
  contexmanager in ExitStack-like situations, since it forces the `__exit__`
  function to be called. The store for S3 still wraps smartopen in the former
  way, since there is postprocessing to be done on the stored object.

## [0.8.1] - 2020-02-06

### Fixed

- Fix bug when prefix is None

## [0.8.0] - 2020-01-27

### Added

- Add list() method. This method lists the entries that are in the store.

## [0.7.0] - 2020-01-24

### Added

- Add support for Google Cloud Storage.

## [0.6.3] - 2019-11-20

### Changed

- The `substore` method returns the same class even for subclasses. That way,
  new properties of a subclass are also on the substore.

## [0.6.2] - 2019-11-12

### Changed

- Updated substore to deal with a possible empty prefix

## [0.6.1] - 2019-10-11

### Changed

- Made `path` parameter to location of `LocalStore` optional (as it should have
  been).

## [0.6.0] - 2019-10-11

### Added

- Add location method to stores. This method returns a client-understandable
  location of a path in the store, e.g. for the RemoteStoreS3 it returns the URL
  of the file at path.

## [0.5.0] - 2019-09-18

### Added

- Allow setting ACL when writing to S3 store. Note that this requires the client
  to check whether it is writing to an S3 store. Passing the argument to the
  open or write method of any other store results in an exception.

## [0.4.0] - 2019-08-16

### Added

- Allow assuming role in S3 store.

## [0.3.1] - 2019-07-26

### Added

- Substore example to the documentation.

### [0.3.0] - 2019-07-26

### Added

- Documentation, including a usage example.

### Changed

- Updated and enabled `InMemoryStore`.

## [0.2.0] - 2019-07-19

### Added

- Method `open` on abstract store that mimics the semantics of `open` in Python.
- Method `substore` that creates a substore on a relative path within the store.

### Changed

- Implementation of `RemoteStoreS3` and `LocalStore` to make use of the
  `smart_open` library.
- Disabled `InMemoryStore`. Methods now throw `NotImplementedError`.

## [0.1.0] - 2019-07-15

### Added

- AbstractStore
- LocalStore
- RemoteStoreS3
- InMemoryStore
