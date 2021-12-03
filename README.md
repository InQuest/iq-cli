# README

InQuest platform v3 Python client with CLI interface.

## Install with `pipenv`

This client includes a CLI interface. To set it up with `pipenv`:

1. Create a virtual environment and install `pipenv`:

```sh
python3 -m venv venv
. venv/bin/activate
pip install -U pip pipenv
```

2. Install dependencies with `pipenv`:

```
pipenv install
```

Follow the remaining steps only for CLI setup.

3. Create a configuration file from default template:

```
cp config.yml.dist config.yml
```

4. Edit `config.yml` and set up server details.

## InQuest Command Line Driver

```
Usage:
    ./iq-cli.py [options] session export <id>
    ./iq-cli.py [options] file search [--limit=<limit>] [--eventid=<eventid>] [--signature-name=<signature-name>] [--signature-category=<signature-category>]
    ./iq-cli.py [options] file download id <id> [--output=<output>] [--dfi-output=<dfi-output>]
    ./iq-cli.py [options] file download hash <(md5|sha1|sha256|sha512)> [--output=<output>] [--dfi-output=<dfi-output>]
    ./iq-cli.py [options] file scan <input>

Options:
    --api=<apikey>              Specify an API key.
    --host=<hostname>           API server hostname.
    --secure=<true|false>       Use HTTPS if true, HTTP if false [default: true].
    --verify-tls=<true|false>   Verify validity of TLS certificate when using HTTPS [default: true].

    --limit                     Maximum number of entries.
    --eventid                   Event ID of the Signature hit.
    --signature-name            Name of the Signature hit.
    --signature-category        Category of the Signature hit.
    --output=<output>           Target file. If not set, the file will be streamed to stdout.
    --dfi-output=<dfi-output>   Target location for DFI content. If not set, DFI content will not be downloaded.
```

### CLI examples

```sh
./iq-cli.py --api APIKEY --host SERVER --secure true --verify-tls true session export ID
./iq-cli.py --api APIKEY --host SERVER --secure true --verify-tls true file search --limit LIMIT --eventid EVENTID --signature-name SIGNATURE_NAME --signature-category SIGNATURE_CATEGORY
./iq-cli.py --api APIKEY --host SERVER --secure true --verify-tls true file download id ID --output /path/to/target/file --dfi-output /path/to/target/folder
./iq-cli.py --api APIKEY --host SERVER --secure true --verify-tls true file download hash HASH --output /path/to/target/file --dfi-output /path/to/target/folder
```

## API Interface

Configuration and examples:

```py
#!/usr/bin/env python
import simplejson as json

import api
from lib import client

client.config = {
    'apikey': '0000000000000000000000000000000000000000',
    'server': {
        'host': 'xxxxxx',
        'secure': True,
        'verify': False,
    },
}

# Get full session info by ID
entity = api.session.export(session_id=1)

# Search by Signature Category:
result = api.search.files(
    limit=2,
    signature_category='FileID',
)

# Search by Signature Name
result = api.search.files(
    limit=2,
    signature_name='Adobe PDF',
)

# Search by Signature EventID
result = api.search.files(
    limit=2,
    eventid=1000000,
)

# Iterate over search results
for file in result:
    print(json.dumps(file, indent=4))

# Download File by ID
api.file.download_by_id(1, output='/tmp/file.out', dfi_output='/tmp/dfi')

# Download File by Hash
api.file.download_by_hash('00000000000000000000000000000000', output='/tmp/file.out', dfi_output='/tmp/dfi')

# Scan File
api.file.scan('/tmp/file.in')
```
