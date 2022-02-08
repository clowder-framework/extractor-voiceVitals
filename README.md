## What an extractor needs:

1. Dockerfile
2. extractor_info.json
3. Extractor python file itself
4. requirements.txt that includes all python libraries needed


## How to build this extractor
Run `docker build . -t <image_name>:<image_version>`. 

e.g. `docker build . -t open-smile-extractor:latest`


## How to add it to Clowder
1. add below to `docker-compose.extractors.yml` :

```
opensmileaudio:
    image: open-smile-extractor:latest
    restart: unless-stopped
    networks:
      - clowder
    depends_on:
      - rabbitmq
      - clowder
    environment:
      - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
```

2. Run `docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.extractors.yml up`
For more details, follow the instruction: https://clowder-framework.readthedocs.io/en/latest/userguide/installing_clowder.html 
   

### Notes:
The shape of the resource object in pyclowder:
https://github.com/clowder-framework/pyclowder/blob/master/pyclowder/connectors.py#L208