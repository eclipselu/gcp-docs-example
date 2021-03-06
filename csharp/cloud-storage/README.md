# Cloud Run for Anthos – Cloud Storage Events tutorial

This sample shows how to create a service that processes GCS events.

## Setup

Configure environment variables:

```sh
MY_RUN_SERVICE=gcs-service
MY_RUN_CONTAINER=gcs-container
MY_GCS_BUCKET=$(gcloud config get-value project)-gcs-bucket
```

## Quickstart

Deploy your Cloud Run service:

```sh
gcloud builds submit \
 --tag gcr.io/$(gcloud config get-value project)/${MY_RUN_CONTAINER}
gcloud run deploy ${MY_RUN_SERVICE} \
 --image gcr.io/$(gcloud config get-value project)/${MY_RUN_CONTAINER} \
 --allow-unauthenticated
```

Create a single region Cloud Storage bucket:

```sh
gsutil mb -p $(gcloud config get-value project) \
    -l us-central1 \
    gs://${MY_GCS_BUCKET}
```

Create Cloud Storage trigger:

```sh
gcloud beta events triggers create my-gcs-trigger \
  --destination-run-service ${MY_RUN_SERVICE} \
  --matching-criteria type=google.cloud.audit.log.v1.written \
  --matching-criteria methodName=storage.buckets.update \
  --matching-criteria serviceName=storage.googleapis.com \
  --matching-criteria resourceName=projects/_/buckets/"$MY_GCS_BUCKET"
```

## Test

Test your Cloud Run service by publishing a message to the topic:

```sh
gsutil defstorageclass set NEARLINE gs://${MY_GCS_BUCKET}
```

Observe the Cloud Run service printing upon receiving an event in
Cloud Logging:

```sh
gcloud logging read "resource.type=cloud_run_revision AND \
resource.labels.service_name=${MY_RUN_SERVICE}" --project \
$(gcloud config get-value project) --limit 30 --format 'value(textPayload)'
```
