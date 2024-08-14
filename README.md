# OmniStore

[![Latest Release](https://img.shields.io/github/v/release/inftyai/omnistore?include_prereleases)](https://github.com/inftyai/omnistore/releases/latest)

An unified python client to communicate with various kinds of object-store providers.

## How to use

### Installation

```cmd
pip install omnistore
```

### Methods

```python
from omnistore.objstore import StoreFactory

# Initialization
client = StoreFactory.new_client(
    provider=provider, endpoint=endpoint, bucket=bucket
)

# Upload
client.upload(src, dest)

# Download
client.download(src, dest)

# Exists
client.exists(filename)

# Delete
client.delete(filename)
```

## Supported List

- [Alibaba Cloud OSS](https://www.alibabacloud.com/help/en/oss/)

## Contributions

🚀 All kinds of contributions are welcomed ! Please follow [Contributing](./CONTRIBUTING.md). Thanks to all these contributors.

<a href="https://github.com/inftyai/omnistore/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=inftyai/omnistore" />
</a>
