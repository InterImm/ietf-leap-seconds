from urllib.request import urlretrieve
import json

data_url = 'https://www.ietf.org/timezones/data/leap-seconds.list'
data_file_path = '/tmp/leapseconds.list'
output_file_path = '/tmp/leapseconds.json'

downloader = urlretrieve(data_url, data_file_path)

leap_seconds = []
expires_on = ""
with open(data_file_path, 'r') as fp:
    for line in fp:
        if not line.startswith('#'):
            leap_seconds.append(line)
        elif 'File expires on' in line:
            expires_on = line.split(':')[1].strip()


def line_parser(one_line):
    """Parse one line from the leapseconds file
    """
    one_line_splitted = one_line.split('\t')

    if not len(one_line_splitted) == 3:
        raise Exception('Not enough columns in data file')
    else:
        res = {
            "epoch": one_line_splitted[0],
            "seconds": one_line_splitted[1],
            "description": one_line_splitted[2].replace('#','').replace('\n','').strip()
        }

    return res


META_DICT = {
    "description": [
        {
            "epoch": "epoch since 1900-01-01 00:00:00",
            "seconds": "Seconds to be added to UTC to calcualte TAI"
        }
    ],
    "source": "https://www.ietf.org/timezones/data/leap-seconds.list",
    "expires_on": expires_on
}

data = []
for line in leap_seconds:
    data.append(
        line_parser(line)
    )

json_result = {
    "meta": META_DICT,
    "data": data
}

with open(output_file_path, 'w') as outfile:
    json.dump(json_result, outfile)