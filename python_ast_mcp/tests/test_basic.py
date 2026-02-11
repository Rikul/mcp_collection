import asyncio

from python_ast import server as srv


def test_list_imports_normalizes_imports():
    code = "import os\nfrom pathlib import Path as P\n"
    out = asyncio.run(srv.list_imports(code))
    assert "import os" in out
    assert "from pathlib import Path as P" in out


def test_list_definitions_finds_top_level_defs():
    code = """
class A:
    pass

def f():
    return 1

async def g():
    return 2
"""
    out = asyncio.run(srv.list_definitions(code))
    assert "class A" in out
    assert "def f" in out
    assert "async def g" in out


def test_extract_docstring_module_and_named():
    code = (
        '"""mod doc"""\n'
        "\n"
        "def f():\n"
        "    \"\"\"f doc\"\"\"\n"
        "    return 1\n"
    )
    mod = asyncio.run(srv.extract_docstring(code, name=""))
    fn = asyncio.run(srv.extract_docstring(code, name="f"))
    assert mod == "mod doc"
    assert fn == "f doc"
