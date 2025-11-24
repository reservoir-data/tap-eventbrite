# `tap-eventbrite`

Singer tap for Eventbrite.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Supported Python Versions

* 3.12
* 3.13
* 3.14

## Supported streams

* `organizations`
* `events`

> [!IMPORTANT]
> New streams will be added on demand. Please open an issue if you need a new stream.

## Settings

| Setting    | Required | Default                    | Description                        |
| :--------- | :------- | :------------------------- | :--------------------------------- |
| token      | True     | None                       | API Token for Eventbrite           |
| base_url   | False    | https://api.eventbrite.com |                                    |
| start_date | False    | None                       | Earliest datetime to get data from |

### Built-in settings

| Setting                           | Required | Default | Description                                                                                                                                                                                                                                              |
| :-------------------------------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| stream_maps                       | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html).                                                                                                              |
| stream_map_config                 | False    | None    | User-defined config values to be used within map expressions.                                                                                                                                                                                            |
| faker_config                      | False    | None    | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an addtional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed                 | False    | None    | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator                                                                                                                                |
| faker_config.locale               | False    | None    | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization                                                                                                                                    |
| flattening_enabled                | False    | None    | 'True' to enable schema flattening and automatically expand nested properties.                                                                                                                                                                           |
| flattening_max_depth              | False    | None    | The max depth to flatten schemas.                                                                                                                                                                                                                        |
| batch_config                      | False    | None    |                                                                                                                                                                                                                                                          |
| batch_config.encoding             | False    | None    | Specifies the format and compression of the batch files.                                                                                                                                                                                                 |
| batch_config.encoding.format      | False    | None    | Format to use for batch files.                                                                                                                                                                                                                           |
| batch_config.encoding.compression | False    | None    | Compression format to use for batch files.                                                                                                                                                                                                               |
| batch_config.storage              | False    | None    | Defines the storage layer to use when writing batch files                                                                                                                                                                                                |
| batch_config.storage.root         | False    | None    | Root path to use when writing batch files.                                                                                                                                                                                                               |
| batch_config.storage.prefix       | False    | None    | Prefix to use when writing batch files.                                                                                                                                                                                                                  |

A full list of supported settings and capabilities is available by running: `tap-eventbrite --about`

### Source Authentication and Authorization

Follow the instructions in the [Eventbrite API documentation](https://www.eventbrite.com/platform/api#/introduction/authentication) to obtain an API token.

## Usage

You can easily run `tap-eventbrite` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-eventbrite --version
tap-eventbrite --help
tap-eventbrite --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
uv tool install --with tox-uv tox
```

### Create and Run Tests

Run integration tests:

```bash
tox -e 3.14
```

You can also test the `tap-eventbrite` CLI interface directly:

```bash
tox -e sync -- --about --format=json
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Go ahead and [install Meltano](https://docs.meltano.com/getting-started/installation/) if you haven't already.

1. Install all plugins

   ```bash
   meltano install
   ```

1. Check that the extractor is working properly

   ```bash
   meltano invoke tap-eventbrite --version
   ```

1. Execute an ELT pipeline

   ```bash
   meltano run tap-eventbrite target-jsonl
   ```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
