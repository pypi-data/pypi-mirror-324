import os
import shutil


class SafeCopyTree:
    @staticmethod
    def copy(src, dst):
        """
        Safely copies the contents of src directory to dst directory.
        """
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isdir(s):
                SafeCopyTree.copy(s, d)
            else:
                shutil.copy2(s, d)
