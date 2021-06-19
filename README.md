# Youtube Query

Fampay Backend Engineer Assignment

## Usage

### Running the app

- `docker-compose up`

### More info:

The configurations can be found in [youtube/utils/config.py](https://github.com/shreyasbapat/Youtube-Scraper-Service/blob/master/youtube/utils/config.py).

I have added the key and query as default argument, which can be changed and ideally, should directly be taken from the environment.

After running the app, wait for some time for the DB to be populated, then run:



```bash
curl --location --request GET '127.0.0.1:9198/api/v1/youtube/videos?page=1&query=LIVE'
```

## Dependencies

Only `docker` needs to be setup in the system running this.

For setting up the dev environment, `pip install poetry` followed by `poetry update`. 

This will install all the dependencies from the lock file. 

This can be followed by `poetry shell` for local virtual environment.
