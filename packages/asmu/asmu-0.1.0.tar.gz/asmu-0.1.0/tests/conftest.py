"""conftest.py
Custom PyTest configuration.
"""

def pytest_addoption(parser):
    parser.addoption("--buffer", action="store_true", help="test all possible buffer settings")

def pytest_generate_tests(metafunc):
    # test both in_buffer settings (where possible)
    if "in_buffer" in metafunc.fixturenames:
        if metafunc.config.getoption("buffer"):
            in_buffer = [True, False]
        else:
            in_buffer = [True]
        metafunc.parametrize("in_buffer", in_buffer)
    # test both out_buffer settings (where possible)
    if "out_buffer" in metafunc.fixturenames:
        if metafunc.config.getoption("buffer"):
            out_buffer = [False, True]
        else:
            out_buffer = [False]
        metafunc.parametrize("out_buffer", out_buffer)
