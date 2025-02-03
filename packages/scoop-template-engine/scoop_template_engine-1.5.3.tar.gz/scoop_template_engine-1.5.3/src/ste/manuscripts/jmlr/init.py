# This script initializes the LaTeX author resources provided for
# Journal of Machine Learning Research (JMLR).
# https://github.com/JmlrOrg/jmlr-style-file

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get the LaTeX author resources from the publisher.
        utilities.get_archive('https://github.com/JmlrOrg/jmlr-style-file/archive/refs/heads/master.zip', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
