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

# [START gcs_server]
import os
import uuid

from flask import Flask, request, make_response
from cloudevents.http import CloudEvent, from_http, to_structured

app = Flask(__name__)
# [END gcs_server]


# [START gcs_handler]
@app.route('/', methods=['POST'])
def index():
    # Gets the GCS bucket name from the CloudEvent header
    # Example: "storage.googleapis.com/projects/_/buckets/my-bucket"
    event = from_http(request.headers, request.get_data())
    print(f"Detected change in GCS bucket: {event['subject']}")

    attributes = {
        "id": str(uuid.uuid4()),
        "source": "https://localhost",
        "specversion": "1.0",
        "type": "com.example.kuberun.events.received",
    }
    data = {"message": "Hello World!"}
    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)

    response = make_response(body, 200)
    response.headers.update(headers)
    return response


# [END gcs_handler]

# [START gcs_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END gcs_server]
