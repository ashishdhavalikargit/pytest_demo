Prerequisite:
Python 3.9.1 or above

Steps to Set-up:
1 Create Python vertual environment:
python -m venv /path/to/new/virtual/environment

2 Activate Python vertual environment:

<path to new virtual environment>\Scripts\activate

3 Install required python3 packages
Navigate to home directory of project
pip3 install -r requirements.txt

Run the tests:
To execute all tests under example run:
python .\test_runner.py -f example
To execute a specific tests under example add -m and test marker :
python .\test_runner.py -f example -m tc_example

Reports:
After execution is completed reports will get generated under report folder with timestamp.
