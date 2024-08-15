# OmniStore

[![Latest Release](https://img.shields.io/github/v/release/inftyai/omnistore?include_prereleases)](https://github.com/inftyai/omnistore/releases/latest)

An unified python client to communicate with various kinds of object-store providers.

## How to use

### Installation

```cmd
pip install omnistore
```

### Usage

```python
from omnistore.objstore import StoreFactory

# Initialization
client = StoreFactory.new_client(
    provider=<provider>, endpoint=<endpoint>, bucket=<bucket>
)

# Create a directory
client.create_dir(dir_name)

# Delete a directory with all its files
client.delete_dir(dir_name)

# Upload
client.upload(src, dest)

# Upload a directory with all its files
client.upload_dir(src_dir, dest_dir)

# Download
client.download(src, dest)

# Download a directory with all its files
client.download_dir(src_dir, dest_dir)

# Exists
client.exists(filename)

# Delete
client.delete(filename)
```

## Supported Providers

### [Alibaba Cloud OSS](https://www.alibabacloud.com/help/en/oss/)

Usage:

```python
client = StoreFactory.new_client(
    provider="OSS", endpoint=<endpoint>, bucket=<bucket>
)
```

Required environment variables:

```yaml
OSS_ACCESS_KEY_ID=
OSS_ACCESS_KEY_SECRET=
```

## Development

Once you want to run the integration tests, you should have a `.env` file locally, similar to the `.env.example`.

## Contributions

🚀 All kinds of contributions are welcomed ! Please follow [Contributing](./CONTRIBUTING.md). Thanks to all these contributors.

<a href="https://github.com/inftyai/omnistore/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=inftyai/omnistore" />
</a>
