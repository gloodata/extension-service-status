# Service Status Explorer (Gloodata Extension)

A Python extension for [Gloodata](https://gloodata.com/) to explore service status for services that provide them via an HTTP API.

[🎥 Watch Youtube Demo](https://www.youtube.com/watch?v=7fam5OxI-PU)

![Extension Preview](https://raw.githubusercontent.com/gloodata/extension-service-status/refs/heads/main/resources/ext-preview.webp)

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/)
- [Gloodata](https://gloodata.com/download/)

Check that you are in a recent version of `uv`:

```bash
uv self update
```

## Run

```sh
uv run src/main.py
```

Available environment variables and their defaults:

- `EXTENSION_PORT`: `8086`
- `EXTENSION_HOST`: `localhost`

For example, to change the port:

```sh
EXTENSION_PORT=6677 uv run src/main.py
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.
