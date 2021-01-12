## Running the Tests

```sh
# Run unit tests.
npm run test

# Run system tests.
SAMPLE=[SAMPLE_TO_TEST]
CONTAINER_IMAGE=gcr.io/$GOOGLE_CLOUD_PROJECT/${SAMPLE}:manual
gcloud builds submit --tag $CONTAINER_IMAGE
SERVICE_NAME=${SAMPLE} npm run system-test
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/${SAMPLE}:manual
```

## Deploying

```sh
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
gcloud run deploy ${SAMPLE} \
  # Needed for Manual Logging sample.
  --set-env-var GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
  --image gcr.io/${GOOGLE_CLOUD_PROJECT}/${SAMPLE}
```
