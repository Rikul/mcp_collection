import asyncio
import json

from codeblock_tools import server as srv


def test_list_and_extract_blocks():
    md = """text

```python
print('hi')
```

```txt
hello
```
"""
    listed = json.loads(asyncio.run(srv.list_fenced_code_blocks(md)))
    assert len(listed) == 2
    assert listed[0]["language"] == "python"

    first = asyncio.run(srv.extract_fenced_code_block(md, index=0))
    assert "print('hi')" in first


def test_strip_blocks_by_language():
    md = """a

```python
x=1
```

b
"""
    stripped = asyncio.run(srv.strip_fenced_code_blocks(md, language="python"))
    assert "x=1" not in stripped
    assert "a" in stripped and "b" in stripped
