"""unittests package"""

import re
from pathlib import Path

from vhelpers import vdate, vdict, vpath, vre

ROOT = Path(__file__).parent.parent
PYPROJECT_D = vdict.pyproject_d(ROOT)


def test_version__readme():
    """Version in README, URL."""
    expected = PYPROJECT_D["tool"]["poetry"]["version"]
    package = PYPROJECT_D["tool"]["poetry"]["name"].replace("_", "-")
    readme = PYPROJECT_D["tool"]["poetry"]["readme"]
    readme_text = Path.joinpath(ROOT, readme).read_text(encoding="utf-8")
    url_toml = "pyproject.toml project.urls.DownloadURL"
    url_text = PYPROJECT_D["tool"]["poetry"]["urls"]["Download URL"]

    for source, text in [
        (readme, readme_text),
        (url_toml, url_text),
    ]:
        regexes = [fr"{package}.+/(.+?)\.tar\.gz", fr"{package}@(.+?)$"]
        versions = [v for s in regexes for v in re.findall(s, text, re.M)]
        assert expected in versions, f"version {expected} not in {source}"


def test_version__changelog():
    """Version in CHANGELOG."""
    version_toml = PYPROJECT_D["tool"]["poetry"]["version"]
    path = Path.joinpath(ROOT, "CHANGELOG.rst")
    text = path.read_text(encoding="utf-8")
    regex = r"(.+)\s\(\d\d\d\d-\d\d-\d\d\)$"
    version_log = vre.find1(regex, text, re.M)
    assert version_toml == version_log, f"version in {path=}"


def test_last_modified_date():
    """Last modified date in CHANGELOG."""
    path = Path.joinpath(ROOT, "CHANGELOG.rst")
    text = path.read_text(encoding="utf-8")
    regex = r".+\((\d\d\d\d-\d\d-\d\d)\)$"
    date_log = vre.find1(regex, text, re.M)
    files = vpath.get_files(ROOT, ext=".py")
    last_modified = vdate.last_modified(files)
    assert last_modified == date_log, "last modified file"
