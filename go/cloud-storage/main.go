// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// [START gcs_handler]

// Sample cloud-storage is a Cloud Run service which handles events from Cloud Storage
package main

import (
	"context"
	"fmt"
	"log"

	cloudevents "github.com/cloudevents/sdk-go/v2"
	storage "github.com/googleapis/google-cloudevents-go/cloud/storage/v1"
)

// Receive simply print the Ce-Subject header out
func Receive(event cloudevents.Event) {
	// do something with event.
	e, err := storage.UnmarshalStorageObjectData(event.Data())
	if err != nil {
		panic(err)
	}
	fmt.Printf("Detected change in GCS bucket: %s, object name: %s\n", *e.Bucket, *e.Name)
}

// [END gcs_handler]
// [START gcs_server]

func main() {
	// The default client is HTTP.
	c, err := cloudevents.NewDefaultClient()
	if err != nil {
		log.Fatalf("failed to create client, %v", err)
	}
	log.Fatal(c.StartReceiver(context.Background(), Receive))
}

// [END gcs_server]
