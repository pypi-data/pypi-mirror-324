# PublicHost

Make localhost public in one line.

## Installation

```bash
pip install publichost
```

## Usage

```python
from publichost import Tunnel

tunnel = Tunnel(port=3000)
print(f"Public URL: {tunnel}")  # https://x8k2p.publichost.dev
```

Need a custom subdomain?

```python
tunnel = Tunnel(port=3000, subdomain="myapp")
```

## Features

- 🚀 Single line to get public URL
- 🌐 Random or custom subdomains
- 💻 Works with any local web server

## License

MIT License - see LICENSE file for details.