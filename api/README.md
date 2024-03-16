
## Build
```
docker build -t api .
```

## RUN
```
docker run --name api_a -p 8001:8000 -e PORT=8000 -e WEBSITE="website_a" -v "./:/app" --rm api
```