# groundstaff

> simple script to automate futsal court reservations :calendar:

## Usage

### install deps

> pip install -r requirements

### Simple one-time-booking
```shell
# to see all options
python groundstaff.py --help

    Usage: groundstaff.py [OPTIONS]

    Options:
    --username TEXT       username
    --password TEXT       password
    --date TEXT           date in YYYY-MM-DD
    --timerange TEXT      for instance, 1800-2000
    --tel TEXT            mobile tel number to reserve in
    --indoor / --outdoor  set this if booking indoor court; defaults to outdoor
                            court


# Example to book for Bonfim indoor court from 1800 to 2000 for 31st Dec 2019
python groundstaff.py --username 0001 --password 50meSekreT! --date 2019-12-31 --timerange 1800-2000 --tel 080-9999-9999 --indoor
```

## TODOs

- [ ] Dockerize (containerization)
- [ ] CI builds
