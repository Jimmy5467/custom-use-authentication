#!"E:\internship\Feature IT LLC\car_rental_3\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'myapi==0.0.1','console_scripts','cm'
__requires__ = 'myapi==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('myapi==0.0.1', 'console_scripts', 'cm')()
    )
