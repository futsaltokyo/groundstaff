# NOTE: just handling Bonfim court for now

# starting point
# args:
#   court number
#   date in YYYY-MM-DD
#   hour_from in 24H format
#   hour_to in 24H format
RESERVATION_FORM_URL = (
    'https://labola.jp/reserve/facility/',
    '{}/reserve/normal/{}-{}-{}'
)

INDOOR_COURT_NO = 2024
OUTDOOR_COURT_NO = 2025


def get_url(date, hour_from, hour_to, indoor=True):
    return RESERVATION_FORM_URL.format(
        INDOOR_COURT_NO if indoor else OUTDOOR_COURT_NO,
        date,
        hour_from,
        hour_to
    )
