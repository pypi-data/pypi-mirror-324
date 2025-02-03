# This script initializes the LaTeX author resources provided for
# Springer Nature journals based on the sn-jnl.cls document class.
# https://www.springer.com/journal/10851/submission-guidelines
# https://www.springernature.com/gp/authors/campaigns/latex-author-support

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://resource-cms.springernature.com/springer-cms/rest/v1/content/18782940/data/v11', junk = 2)

        # Convert the macOS-style line endings to unix-style line endings in sn-jnl.cls
        # to achieve compatibility with diff.
        utilities.mac2unix('sn-jnl.cls')

        # The file sn-mathphys-num.bst has some issues.
        # It replaces ~ by \texttildelow, which causes an error in the \url command of url.sty.
        # We apply a patch created via
        #   diff -u --ignore-trailing-space sn-mathphys-num.bst sn-mathphys-num-scoop.bst > sn-mathphys-num.bst.patch
        utilities.apply_patch('sn-mathphys-num.bst.patch')

        # The \bibliographystyle is loaded with a document class option.
        # We use sn-mathphys-num, which loads sn-mathphys-num.bst.
        # Since sn-mathphys-num.bst has some issues, we replace it by a patched
        # version and override \bibliographystyle once the sn-jnl.cls has been
        # loaded.
        # We apply a patch created via
        #   diff -u --ignore-trailing-space sn-jnl.cls sn-jnl-scoop.cls > sn-jnl.cls.patch
        utilities.apply_patch('sn-jnl.cls.patch')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
