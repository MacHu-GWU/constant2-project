#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from constant2 import Constant


class File(Constant):
    id = None
    ext = None
    type = "File"


class FileType(Constant):
    class Image(File):
        id = 1
        ext = ".jpg"

    class Music(File):
        id = 2
        ext = ".mp3"

    class Video(File):
        id = 3
        ext = ".avi"


class TestFileType(object):
    def test(self):
        assert FileType.Image.Items() == [
            ("ext", ".jpg"), ("id", 1), ("type", "File")
        ]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
