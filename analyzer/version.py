import requests
from pkg_resources import parse_version


def check_version():
    """Check that you have the latest CVXPY version.
    """
    # Gets the latest version on PyPi accompanied by a source distribution
    url = "https://pypi.org/pypi/cvxpy/json"
    r = requests.get(url)
    if r.ok:
        data = r.json()
        releases = data["releases"]
        versions = [
            v
            for v in releases.keys()
            if "sdist" in [rel["packagetype"] for rel in releases[v]]
        ]
        versions.sort(key=parse_version)
        remote_version = versions[-1]
        import cvxpy

        local_version = cvxpy.__version__
        print("Latest CVXPY version:", remote_version)
        print("Local CVXPY version:", local_version)
        return parse_version(local_version) == parse_version(remote_version)
    else:
        msg = "The request to pypi returned status code" + str(r.status_code)
        raise RuntimeError(msg)
