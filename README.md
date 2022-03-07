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

How to pass args to extractor:
In the dockerfile, modify `python {your extractor.py} to include parameters`, For example: `python wordcount.py --heartbeat 1`
Available default args include:
```
 # create the actual extractor
self.parser = argparse.ArgumentParser(description=self.extractor_info['description'])
self.parser.add_argument('--connector', '-c', type=str, nargs='?', default=connector_default,
                         choices=["RabbitMQ", "HPC", "Local"],
                         help='connector to use (default=RabbitMQ)')
self.parser.add_argument('--logging', '-l', nargs='?', default=logging_config,
                         help='file or url or logging coonfiguration (default=None)')
self.parser.add_argument('--pickle', nargs='*', dest="hpc_picklefile",
                         default=None, action='append',
                         help='pickle file that needs to be processed (only needed for HPC)')
self.parser.add_argument('--clowderURL', nargs='?', dest='clowder_url', default=clowder_url,
                         help='Clowder host URL')
self.parser.add_argument('--register', '-r', nargs='?', dest="registration_endpoints",
                         default=registration_endpoints,
                         help='Clowder registration URL (default=%s)' % registration_endpoints)
self.parser.add_argument('--rabbitmqURI', nargs='?', dest='rabbitmq_uri', default=rabbitmq_uri,
                         help='rabbitMQ URI (default=%s)' % rabbitmq_uri.replace("%", "%%"))
self.parser.add_argument('--rabbitmqQUEUE', nargs='?', dest='rabbitmq_queuename',
                         default=rabbitmq_queuename,
                         help='rabbitMQ queue name (default=%s)' % rabbitmq_queuename)
self.parser.add_argument('--rabbitmqExchange', nargs='?', dest="rabbitmq_exchange", default=rabbitmq_exchange,
                         help='rabbitMQ exchange (default=%s)' % rabbitmq_exchange)
self.parser.add_argument('--mounts', '-m', dest="mounted_paths", default=mounted_paths,
                         help="dictionary of {'remote path':'local path'} mount mappings")
self.parser.add_argument('--input-file-path', '-ifp', dest="input_file_path", default=input_file_path,
                         help="Full path to local input file to be processed (used by Big Data feature)")
self.parser.add_argument('--output-file-path', '-ofp', dest="output_file_path", default=output_file_path,
                         help="Full path to local output JSON file to store metadata "
                              "(used by Big Data feature)")
self.parser.add_argument('--sslignore', '-s', dest="sslverify", action='store_false',
                         help='should SSL certificates be ignores')
self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')
self.parser.add_argument('--no-bind', dest="nobind", action='store_true',
                         help='instance will bind itself to RabbitMQ by name but NOT file type')
self.parser.add_argument('--max-retry', dest='max_retry', default=max_retry,
                         help='Maximum number of retries if an error happens in the extractor')
self.parser.add_argument('--heartbeat', dest='heartbeat', default=heartbeat,
                         help='Time in seconds between extractor heartbeats (default=%d)' % heartbeat)
```
