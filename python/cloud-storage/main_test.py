# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
import json
from uuid import uuid4

import pytest

import main

binary_headers = {
    "ce-id": str(uuid4),
    "ce-type": "com.pytest.sample.event",
    "ce-source": "<my-test-source>",
    "ce-specversion": "1.0",
    "ce-subject": "test-subject"
}

binary_data = {
    "kind": "storage#object",
    "id": "objectid",
    "selfLink": "https://example.com/object.txt",
    "name": "object.txt",
    "bucket": "test-bucket",
    "generation": "1610564600595212",
    "metageneration": "1",
    "contentType": "application/octet-stream",
    "timeCreated": "2021-01-13T19:03:20.603Z",
    "updated": "2021-01-13T19:03:20.603Z",
    "storageClass": "STANDARD",
    "timeStorageClassUpdated": "2021-01-13T19:03:20.603Z",
    "size": "1682",
    "md5Hash": "DqB0N1pmMRX4mjv1llfoWQ==",
    "mediaLink": "https://example.com/download/test-bucket/o/go-test-123.txt",
    "contentLanguage": "en",
    "crc32c": "mA33eA==",
    "etag": "CIyGoNfMme4CEAE="
}


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_endpoint(client, capsys):
    r = client.post('/', headers=binary_headers, data=json.dumps(binary_data))
    assert r.status_code == 200

    out, _ = capsys.readouterr()
    assert f"Detected change in GCS bucket: {binary_data['bucket']}, object: {binary_data['name']}" in out
