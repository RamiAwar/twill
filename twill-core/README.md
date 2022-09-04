

# Airplane
We use airplane for configuring runnable / scheduled tasks such as computing analytics once a day.

## Generating requirements for Airplane
Navigate to the project root ./ and export poetry dependencies:
```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

## Run example Airplane task locally
First, add a .env file to the top level directory, specifying all required env vars (twitter api credentials,  mongodb dsn, potentially redis url)

```bash
airplane dev twill/airplane/daily_sync.task.yaml
```

## Deploy Airplane task
```bash
airplane deploy twill/airplane/daily_sync.task.yaml
```

