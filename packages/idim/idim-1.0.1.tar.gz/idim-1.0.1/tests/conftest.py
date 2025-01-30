import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--run-coverage", action="store_true", default=False, help="run coverage tests"
    )
    parser.addoption(
        "--run-property", action="store_true", default=False, help="run property tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "coverage: mark test as coverage test to run")
    config.addinivalue_line("markers", "property: mark test as property test to run")


def pytest_collection_modifyitems(config, items):
    rs = config.getoption("--run-slow")
    rc = config.getoption("--run-coverage")
    rp = config.getoption("--run-property")
    if rs and rc and rp:
        return
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    skip_coverage = pytest.mark.skip(reason="need --run-coverage option to run")
    skip_property = pytest.mark.skip(reason="need --run-property option to run")
    for item in items:
        if "slow" in item.keywords and not rs:
            item.add_marker(skip_slow)
        if "coverage" in item.keywords and not rc:
            item.add_marker(skip_coverage)
        if "property" in item.keywords and not rp:
            item.add_marker(skip_property)
