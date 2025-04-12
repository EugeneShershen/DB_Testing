def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="Environment to run test against (local, docker)")
