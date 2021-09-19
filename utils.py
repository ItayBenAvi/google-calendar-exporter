import datetime


def generate_rfc_3339_timestamp(datetime_to_convert):
    return datetime_to_convert.isoformat()


if __name__ == '__main__':
    now = datetime.datetime.now(datetime.timezone.utc)
    print(generate_rfc_3339_timestamp(now))
