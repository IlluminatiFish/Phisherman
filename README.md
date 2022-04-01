# Phisherman

Phisherman is a synchronous wrapper around the [Phisherman API](https://phisherman.gg)

## ✔️ Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Phisherman.

```bash
pip install Phisherman
```

## ✨ Usage

```python
from phisherman import Phisherman

# Your Phisherman API key
key = 'KEY'

# Phisherman API client
phisherman = Phisherman(key)

# Check if the specified domain is Phisherman's database
phisherman.check_domain('suspicious.test.phisherman.gg')

# Get information about the specified domain from the Phisherman database
phisherman.get_domain_info('suspicious.test.phisherman.gg')

# Reports a phish caught given a domain and the id of the guild the phish was caught in
phisherman.report_caught_phish('verified.test.phisherman.gg', 1)
```

## 🚩 License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
