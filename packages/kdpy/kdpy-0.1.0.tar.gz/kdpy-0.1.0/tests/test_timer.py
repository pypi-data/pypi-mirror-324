import time
import re
from kdpy import measure_time

@measure_time
def dummy_function():
    time.sleep(1)
    return "Hello"

def test_measure_time(capsys):
    dummy_function()
    captured = capsys.readouterr()
    assert re.search(r"Function 'dummy_function' executed in \d+\.\d+ seconds", captured.out)
