# This script initializes the LaTeX author resources provided for
# International Conference on Machine Learning 2025.
# https://icml.cc/Conferences/2025/CallForPapers

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get the LaTeX author resources from the publisher.
        utilities.get_archive('https://media.icml.cc/Conferences/ICML2025/Styles/icml2025.zip', junk = 1)

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'example_paper.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'example_paper.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
