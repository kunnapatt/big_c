
## Build
```
docker build -t analytics .
```

## RUN
```
docker run --name analytics -p 8501:8501 -v "./:/app" --rm analytics
```