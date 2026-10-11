import os

from hamcrest import assert_that, contains_inanyorder

from jev_gate.directory import PackDirectory


def test_loads_every_bundled_pack():
    assert_that(
        [
            pack.label
            for pack in PackDirectory(
                os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "jev_gate", "packs"
                )
            )
            .packs()
            .items
        ],
        contains_inanyorder(
            "python",
            "javascript",
            "typescript",
            "java",
            "rust",
            "ruby",
            "csharp",
            "cpp",
        ),
        "All eight language packs must be bundled",
    )
