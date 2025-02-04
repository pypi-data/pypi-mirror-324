import logging
import sys
from unittest.mock import call

from envzy import AutoExplorer
from pytest import fixture, raises

from datasphere.utils import (
    query_yes_no, humanize_bytes_size, is_python_interpreter, parse_python_main_module, PythonModule,
    get_requirements_for_modules
)


def test_query_yes_no(mocker):
    for choice, default, expected in (
            ('', True, True),
            ('y', True, True),
            ('N', True, False),
            ('Yes', False, True),
            ('', False, False),
            ('no', False, False),
    ):
        mocker.patch('datasphere.utils.input', lambda _: choice)
        assert query_yes_no('do stuff?', default=default) is expected


def test_humanize_bytes_size():
    for size, expected in (
            (1, '1.0B'),
            (900, '900.0B'),
            (2500, '2.4KB'),
            (1 << 20, '1.0MB'),
            (10 * (1 << 30), '10.0GB'),
    ):
        assert humanize_bytes_size(size) == expected


@fixture
def python_symlink(tmp_path):
    link = tmp_path / 'bydhon'
    link.symlink_to(sys.executable)
    return link


@fixture
def text_file(tmp_path):
    tf = tmp_path / 'text.txt'
    tf.write_text('hi')
    tf.chmod(0o777)
    return tf


def test_is_python_interpreter(tmp_path, python_symlink, text_file):
    assert is_python_interpreter(sys.executable)
    assert not is_python_interpreter('ls')
    assert is_python_interpreter(str(python_symlink))
    assert not is_python_interpreter(str(text_file))


@fixture
def python_script_with_shebang(tmp_path):
    script = tmp_path / 'shebang_script.py'
    script.write_text("""
#!/usr/bin/env python3
print('hi')
    """.strip())
    script.chmod(0o0777)
    return script


@fixture
def python_script_with_missing_file_shebang(tmp_path):
    script = tmp_path / 'missing_file_shebang_script.py'
    script.write_text("""
#!/missing/file
print('hi')
    """.strip())
    script.chmod(0o0777)
    return script


@fixture
def python_entry_point(tmp_path):
    ep = tmp_path / 'datacylinder'
    ep.write_text(f"""
#! {sys.executable}
print('hi')
    """.strip())
    ep.chmod(0o0777)
    return ep


@fixture
def binary_file(tmp_path):
    bf = tmp_path / 'binary'
    bf.write_bytes(b'\xb6')
    bf.chmod(0o777)
    return bf


def test_parse_python_main_module(
        tmp_path, caplog, python_symlink, python_script_with_shebang, python_script_with_missing_file_shebang,
        python_entry_point, binary_file, text_file,
):
    with raises(ValueError, match='`cmd` is empty'):
        parse_python_main_module('')
    with raises(ValueError, match=f'file `/missing/file` was not found'):
        parse_python_main_module('/missing/file')
    with raises(ValueError, match=f'file `{python_script_with_missing_file_shebang}` was not found'):
        parse_python_main_module(str(python_script_with_missing_file_shebang))
    with raises(ValueError, match='`python` must be followed by other arguments'):
        parse_python_main_module('python  ')

    caplog.set_level(logging.DEBUG)

    for cmd, expected_module, expected_logs in (
            (
                    'python main.py',
                    PythonModule(path='main.py'),
                    ['`python` is detected as Python interpreter path by common name'],
            ),
            (
                    'python3 main.py',
                    PythonModule(path='main.py'),
                    ['`python3` is detected as Python interpreter path by common name'],
            ),
            (
                    'python3.10 main.py',
                    PythonModule(path='main.py'),
                    ['`python3.10` is detected as Python interpreter path by common name'],
            ),
            (
                    'Python.exe main.py',
                    PythonModule(path='main.py'),
                    ['`Python.exe` is detected as Python interpreter path by common name'],
            ),
            (
                    f'{python_symlink} main.py',
                    PythonModule(path='main.py'),
                    [f'`{python_symlink}` is detected as Python interpreter by '
                     f'`{python_symlink} --version` stdout'],
            ),
            (
                    'python2.7m -v -O -m venv my-venv',
                    PythonModule(path='venv', is_name=True),
                    ['`python2.7m` is detected as Python interpreter path by common name'],
            ),
            (
                    f'{python_script_with_shebang}',
                    PythonModule(path=str(python_script_with_shebang)),
                    [f'shebang `#!/usr/bin/env python3` in file `{python_script_with_shebang}` '
                     f'is detected as Python script'],
            ),
            (
                    f'{python_entry_point} --epochs 5',
                    PythonModule(path=str(python_entry_point)),
                    # TODO: if unit tests Python interpreter name is not standard, log about its detection through
                    #   execution with `--version` will be added and this case will fail, but it is unlikely
                    [f'shebang `#! {sys.executable}` in file `{python_entry_point}` is detected as Python script']
            ),
            (str(binary_file), None, [f'`{binary_file}` is non-unicode file so it is not a Python program']),
            (str(text_file), None, [f'`{text_file}` is not recognized as Python program']),
    ):
        assert parse_python_main_module(cmd) == expected_module
        assert [t[2] for t in caplog.record_tuples] == expected_logs
        caplog.clear()

@fixture
def main_module():
    return PythonModule(path='main.py')

@fixture
def main_namespace():
    return {'foo': 'bar'}

@fixture
def auto_explorer_mock(mocker):
    auto_explorer = mocker.patch('datasphere.utils.AutoExplorer')()
    auto_explorer.get_pypi_packages.side_effect = [
        {'tensorflow-macos': '', 'pandas': '2.0'}
    ]
    return auto_explorer

@fixture
def get_module_namespace_mock(mocker, main_namespace):
    get_module_namespace = mocker.patch('datasphere.utils._get_module_namespace')
    get_module_namespace.side_effect = [main_namespace]
    return get_module_namespace

def test_get_requirements_for_modules(get_module_namespace_mock, main_module, main_namespace, auto_explorer_mock):
    requirements = get_requirements_for_modules([main_module], auto_explorer_mock)

    assert requirements == ['pandas==2.0', 'tensorflow-macos']
    get_module_namespace_mock.assert_has_calls([call(main_module)])
    auto_explorer_mock.get_pypi_packages.assert_has_calls([call(main_namespace)])