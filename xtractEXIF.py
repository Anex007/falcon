from PIL import Image
from PIL.ExifTags import TAGS


def getMetaData(imgName):
    metaData = {}
    try:
        imgFile = Image.open(imgName)
        info = imgFile._getexif()
    except AttributeError:
        return {}
    except OSError:
        return {}
    if not info:
        return {}
    for tag, value in info.items():
        tagName = TAGS.get(tag, tag)
        metaData[tagName] = value

    return metaData


def translateGPS(val):
    lat = None
    lon = None
    latN = None
    lonN = None
    keys = list(val.values())
    for i, x in enumerate(keys):
        if x == 'N' or x == 'S':
            latN = x
            lat = keys[i + 1]
        elif x == 'W' or x == 'E':
            lonN = x
            lon = keys[i + 1]
    if not lat or not lon:
        return None
    lat = [dat for dat, _ in lat]
    lon = [dat for dat, _ in lon]
    dlat = int(lat[0]) + (int(lat[1]) / 60.0) + (int(lat[2]) / 3600.0)
    dlon = int(lon[0]) + (int(lon[1]) / 60.0) + (int(lon[2]) / 3600.0)
    return {'latitude': {'direction': latN, 'value': dlat}, 'longitude': {'direction': lonN, 'value': dlon}}


def getMostOcuuring(gpsInfos):
    for file, gps in gpsInfos.items():
        if closeEnough(gps, gpsInfos):
            pass
        else:
            pass


def getGPS(imgName):
    metaData = getMetaData(imgName)
    for tag in metaData.keys():
        if tag == 'GPSInfo':
            return translateGPS(metaData[tag])
    return None
