import datetime
import json
import io
import re
import os
import yaml








# ================================================================================
# H E L P E R   F U N C T I O N S

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def readJson(file):
    with open(file) as f:
        return json.load(f)

def readBytes(file):
    with open(file, "rb") as f:
        return f.read()

def readText(file):
    with open(file, "r") as f:
        return f.read()

def writeText(file, text):
    with open(file, "w") as f:
        f.write(text)

def findPath(relPath, throwIfNotFound=True):
    """
    Recursively search up the folder ancestry for a file of name @relPath.
    """
    relPath = relPath.replace("\\", os.sep).replace("/", os.sep)
    dir = os.path.dirname(relPath)
    while not os.path.exists(os.path.join(dir, relPath)):
        dir = os.path.abspath(os.path.join(dir, os.pardir))
        if dir == os.path.abspath(os.sep):
            if throwIfNotFound:
                raise FileNotFoundError(f"Could not find file '{relPath}' in the folder ancestry.")
            return None
    return os.path.join(dir, relPath)


def getJson(relPath):
    """
    Search up the folder ancestry for a configuration file of name '{relPath}.json'
    and return that as an object.
    @relPath : str : The relative path of the configuration file to search for. Example: "data/config" will search for "data/config.json"
    """
    if not relPath.endswith('.json'):
        relPath += '.json'
    path = findPath(relPath)
    with open(path) as f:
        return json.load(f)


def getYaml(relPath):
    """
    Search up the folder ancestry for a configuration file of name '{relPath}.json'
    and return that as an object.
    Throws FileNotFoundError if the file is not found.
    """
    if not relPath.endswith('.yaml'):
        relPath += '.yaml'
    path = findPath(relPath)
    with open(path) as f:
        return yaml.safe_load(f)

def g(o, path, default=None, sep='/'):
    """
    Get a value from a dictionary using a path string.
    Example: g(o, "a/b/c") is equivalent to o['a']['b']['c']
    """
    for k in path.split(sep):
        if o is None:
            return default
        try:
            k = int(k)
        except ValueError:
            if not k in o:
                return default
        o = o[k]
    return o

def fixJson(j):
    """
    Recursively resolve any value that is a string in the format "/Date(1234567890)/" to a datetime object.
    2147483647
    1729209600000
    Convert string values that are json into objects.
    """
    if isinstance(j, list):
        for i, v in enumerate(j):
            j[i] = fixJson(v)
    elif isinstance(j, dict):
        for k, v in j.items():
            j[k] = fixJson(v)
    elif isinstance(j, str):
        m = re.match(r"\/Date\((-?\d+)\)\/", j)
        if m:
            s = m.group(1)
            n = int(s)
            if n < 0:
                pass
            if len(s) >= 12:
                # Assume milliseconds and convert to seconds
                n = n / 1000
            date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=n)
            return date
        if j.startswith("{") and j.endswith("}"):
            try:
                return json.loads(j)
            except:
                pass
    return j







def ensurePath(path):
    "Guarantees a folder path exists. Creates it if it doesn't."
    if '.' in path:
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        else:
            pass
    else:
        os.makedirs(path, exist_ok=True)








# ================================================================================
# C A C H E   F U N C T I O N S

def clean_filename(s):
    "Get rid of invalid characters"
    invalid_chars = '<>:"?*'
    for char in invalid_chars:
        s = s.replace(char, "_")
    return s


def get_filename(key):
    "Get the filename for a given key, which is a slash-delimited path."
    key = clean_filename(key)
    path = f"{key}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_file(key):
    try:
        fn = get_filename(key)
        if os.path.exists(fn):
            with open(fn, 'r', encoding='utf-8') as f:
                if fn.endswith('.json'):
                    return json.load(f)
                else:
                    return f.read()
    except Exception as e:
        pass
    return None


def put_file(key, data):
    if isinstance(data, bytes):
        mode = "wb"
    else:
        mode = "w"
    fn = get_filename(key)
    with open(fn, mode) as f:
        if fn.endswith('.json'):
            json.dump(data, f, indent=4, cls=DateTimeEncoder)
        else:
            f.write(data or '')


def get_cache(key):
    return get_file(f"data/cache/{key}")



def put_cache(key, data):
    if not '.' in key:
        key += '.json'
    put_file(f"data/cache/{key}", data)


def cacheGet(fn, func, verbose=True):
    """
    Get the data from the cache if it exists, otherwise call the function to get the data.
    """
    j = get_cache(fn)
    if j:
        print(f"  Cache hit: {fn}")
    else:
        print(f"  Cache miss: {fn}")
        j = func()
        put_cache(fn, j)
    if not j:
        print(f"  Error: {fn}")
    return j








# ================================================================================
# A S S E R T S

def assert_type(o, t, hint=''):
    assert isinstance(o, t), f"Expected type {t}, got {type(o)}. {hint}".strip()
def assert_not_null(o, hint=''):
    assert o != None, f"Expected not null value. {hint}".strip()






# ================================================================================
# P A R Q U E T

def resolve_date_strings(j):
    """
    Recursively resolve any value that is a string in the format "/Date(1234567890)/" to a datetime object.
    2147483647
    1729209600000
    """
    if isinstance(j, list):
        for i, v in enumerate(j):
            j[i] = resolve_date_strings(v)
    elif isinstance(j, dict):
        for k, v in j.items():
            j[k] = resolve_date_strings(v)
    elif isinstance(j, str):
        m = re.match(r"\/Date\((-?\d+)\)\/", j)
        if m:
            s = m.group(1)
            n = int(s)
            if n < 0:
                pass
            if len(s) >= 12:
                # Assume milliseconds and convert to seconds
                n = n / 1000
            date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=n)
            return date
    return j

def to_date(s):
    """Convert a string to a date"""
    if s == None:
        return None
    if s == '':
        return None
    if isinstance(s, datetime.date):
        return s
    re = getRegex(r"\/Date\((?P<A>.+)\)\/")
    match = re.match(s)
    if match:
        s = int(match.group("A"))
        if s <= -62169984000:
            return datetime.datetime.min.isoformat()
        epoch = datetime.datetime(
            1970, 1, 1, tzinfo=datetime.timezone.utc
        )
        dt = epoch + datetime.timedelta(seconds=s)
        s = dt.isoformat().split("T")[0]
    elif "T" in s:
        s = s.split("T")[0]
    elif len(s) == 8:
        s = s[:4] + "-" + s[4:6] + "-" + s[6:]
    else:
        s = s[:10]
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()

def to_datetime(s):
    """Convert a string to a datetime"""
    if s == None:
        return None
    if s == '':
        return None
    if isinstance(s, datetime.date):
        return s
    re = getRegex(r"\/Date\((?P<A>.+)\)\/")
    match = re.match(s)
    if match:
        s = int(match.group("A"))
        if s <= -62169984000:
            return datetime.datetime.min.isoformat()
        epoch = datetime.datetime(
            1970, 1, 1, tzinfo=datetime.timezone.utc
        )
        dt = epoch + datetime.timedelta(seconds=s)
        s = dt.isoformat().split("T")[0]
    elif "T" in s:
        pass
    elif len(s) == 8:
        s = s[:4] + "-" + s[4:6] + "-" + s[6:]
    else:
        s = s[:10]

    for format in ["%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]:
        try:
            return datetime.datetime.strptime(s, format)
        except:
            pass
    return None

def to_int(s):
    if s == None:
        return 0
    return int(s)

def to_float(s):
    if s == None:
        return 0.0
    return float(s)

def to_string(o):
    if o == None:
        return ""
    s = str(o)
    if isinstance(o, datetime.datetime):
        return o.isoformat()
    re = getRegex(r"\/Date\((?P<A>.+)\)\/")
    match = re.match(s)
    if match:
        s = int(match.group("A"))
        if s <= -62169984000:
            return datetime.datetime.min.isoformat()
        epoch = datetime.datetime(
            1970, 1, 1, tzinfo=datetime.timezone.utc
        )
        dt = epoch + datetime.timedelta(seconds=s)
        s = dt.isoformat().split("T")[0]
    return s

def dump(obj, level=0, skipNulls=True, header=None):
    "Print out the non-null properties of an object in columnar format."
    if level == 0:
        print()
        header = header or obj.__class__.__name__
        print(header)

    if isinstance(obj, dict) or hasattr(obj, "__data__"):
        if hasattr(obj, "__data__"):
            items = obj.__data__.items()
        else:
            items = obj.items()
        for k,v in sorted(items):
            if k == "birthDate":
                pass
            if skipNulls and v == None:
                continue
            if isinstance(v, dict) or isinstance(v, list):
                print(f"  {'  ' * level}{k + ':'}")
                dump(v, level + 1, skipNulls)
            else:
                v = to_string(v) if v != None else ''
                print(f"  {'  ' * level}{k + ':':<30} {v[:200]}")
    elif isinstance(obj, list):
        if obj:
            for i,v in enumerate(obj):
                if isinstance(v, dict) or isinstance(v, list):
                    print(f"  {'  ' * level}[{i}]")
                    dump(v, level + 1, skipNulls)
                    if len(obj) > 1:
                        print(f"  {'  ' * level}...{len(obj) - i - 1} more")
                    break
                else:
                    print(f"  {'  ' * level}[{i}] = {to_string(v)}")
    else:
        raise Exception(f"Unknown type: {type(obj)}")








# ================================================================================
# R E G E X   F U N C T I O N S

regex = {}  # Cached compiled regex expressions

def getRegex(pattern):
    global regex
    if pattern not in regex:
        regex[pattern] = re.compile(pattern)
    return regex[pattern]


def getPatternRegex(s):
    prefix = r"\b"
    suffix = r"\b"
    if s.endswith("*"):
        s = s[:-1]
        suffix = ""
    if s.startswith("*"):
        s = s[1:]
        prefix = ""
    return getRegex(prefix + re.escape(s) + suffix)








def test_to_date():
    d = to_datetime("2025-03-28")
    assert str(d) == "2025-03-28 00:00:00"
    d = to_datetime("2025-03-28T18:26:06.948-04:00")
    assert str(d) == "2025-03-28 18:26:06.948000-04:00"
    d = to_datetime("2025-03-28T18:26:06.948Z")
    assert str(d) == "2025-03-28 18:26:06.948000+00:00"
    d = to_date("/Date(1234567890)/")
    assert str(d) == "2009-02-13"
    d = to_date("2009-02-13T00:00:00")
    assert str(d) == "2009-02-13"
    d = to_date("2009-02-13")
    assert str(d) == "2009-02-13"



if __name__ == "__main__":
    test_to_date()