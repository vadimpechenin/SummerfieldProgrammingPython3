import re

with open("map.xml", "r") as f:
    lat = []
    lon = []
    for text in f:
        match = re.search(r"<point\s+[^>]*?lon=([\"\'])(?P<lon>[0-9.,]+)\1\s+[^>]*lat=([\"\'])(?P<lat>[0-9.,]+)\1",
                          text)
        if match:
            v = match.groupdict()
            if "lon" in v and "lat" in v:
                lon.append(v["lon"])
                lat.append(v["lat"])

    print(lon, lat, sep="\n")