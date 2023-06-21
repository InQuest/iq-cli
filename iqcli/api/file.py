import hashlib
from pathlib import Path
import shutil
import sys

from iqcli.api import search
from iqcli.lib import client


def download_by_id(file_id, output=None, dfi_output=None):
    return _download_with_optional_dfi_contents(file_id, output, dfi_output)


def download_by_hash(file_hash, output=None, dfi_output=None):
    for record in search.files(file_hash=file_hash, limit=1):
        return _download_with_optional_dfi_contents(record['id'], output, dfi_output)


def scan(local_file_path):
    with client.post(
        '/scan/flee',
        files={'scanUpload': open(local_file_path, 'rb')},
        headers={'Content-Type': None},
    ) as r:
        r.raise_for_status()
        return r.text


def _download_with_optional_dfi_contents(file_id, output=None, dfi_output=None):
    _download_single_file(file_id, output)

    if not dfi_output:
        return

    Path(dfi_output).mkdir(exist_ok=True)

    with client.get('/files/single', params={'id': file_id}) as r:
        r.raise_for_status()
        parsed_data = r.json()
        
        if 'data' not in parsed_data or not len(parsed_data['data']):
            return
        
        record = parsed_data['data'][0]

    if 'browserable_roots' not in record:
        return

    queue = [r + '/' for r in record['browserable_roots']]
    
    for path in queue:
        full_path = f'{dfi_output}/{path}'
        
        if '/' == path[-1]:
            Path(full_path).mkdir(exist_ok=True)
            queue += [path + v for v in _browse(file_id, path)]
        else:
            _download_single_file(
                file_id,
                output=full_path,
                params={
                    'compressed': 0,
                    'downloadAs': path.split('/')[-1],
                    'path': path,
                },
            )


def _browse(file_id, prefix):
    with client.get(
        '/file/browse',
        params={'file_id': file_id, 'prefix': prefix}
    ) as r:
        r.raise_for_status()
        return r.json()


def _download_single_file(file_id, output=None, params=None):
    with client.get(
        '/file-download',
        params={'id': file_id, **(params or {})},
        stream=True
    ) as r:
        r.raise_for_status()
        
        if output:
            with open(output, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            for chunk in r.iter_content(2048):
                sys.stdout.buffer.write(chunk)


def _file_md5(local_file_path, blocksize=65536):
    result = hashlib.md5()
    
    with open(local_file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            result.update(chunk)
    
    return result.hexdigest()
