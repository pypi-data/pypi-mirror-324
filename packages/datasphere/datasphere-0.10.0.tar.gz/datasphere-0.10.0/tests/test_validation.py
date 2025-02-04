import os.path
from pathlib import Path
from typing import List, Optional

from pytest import raises

from datasphere.config import Config, VariablePath, Environment
from datasphere.pyenv import PythonEnv
from datasphere.validation import validate_inputs, validate_outputs


def test_validate_inputs(caplog):
    cwd = os.path.abspath(os.path.curdir)

    validate_inputs(
        _create_config(inputs=_variable_paths("relative", "other", "/absolute/path", "non-intersecting")),
        _create_env(modules=["some_module"]),
    )
    assert caplog.record_tuples == []

    validate_inputs(
        _create_config(inputs=_variable_paths("same", "module/input", "input")),
        _create_env(modules=["same", "module", "input/module"])
    )
    assert caplog.record_tuples == [
        ('datasphere.validation', 30, f"Local module '{cwd}/same' duplicating input '{cwd}/same'"),
        ('datasphere.validation', 30, f"Local module '{cwd}/module' includes input '{cwd}/module/input'"),
        ('datasphere.validation', 30, f"Input'{cwd}/input' includes module '{cwd}/input/module'"),
    ]
    caplog.clear()

    with raises(ValueError, match=f"Path '{cwd}/dir/content' is included in path '{cwd}/dir'"):
        validate_inputs(
            _create_config(inputs=_variable_paths("dir", "dir/content")),
            _create_env(),
        )
    assert caplog.record_tuples == []

    with raises(ValueError, match=f"Path '/abs/dir/content' is included in path '/abs/dir'"):
        validate_inputs(
            _create_config(inputs=_variable_paths("/abs/dir", "/abs/dir/content")),
            _create_env(),
        )
    assert caplog.record_tuples == []

    local_dir = str(Path(__file__).parent.absolute())
    local_file_in_dir = __file__
    with raises(ValueError, match=f"Path '{local_file_in_dir}' is included in path '{local_dir}'"):
        validate_inputs(
            _create_config(inputs=_variable_paths(local_dir, local_file_in_dir)),
            _create_env(),
        )
    assert caplog.record_tuples == []

    with raises(ValueError, match='Paths must be unique'):
        validate_inputs(
            _create_config(inputs=_variable_paths("path", "path")),
        )
    assert caplog.record_tuples == []

    with raises(ValueError, match=f"Path '{cwd}/base_dir/included_dir' is included in path '{cwd}/base_dir'"):
        validate_inputs(
            _create_config(inputs=_variable_paths("base_dir", "base_dir/included_dir")),
            _create_env()
        )
    assert caplog.record_tuples == []


def test_validate_outputs():
    validate_outputs(_create_config(outputs=_variable_paths("relative", "other", "/absolute/path", "non-intersecting")))
    validate_outputs(_create_config(outputs=_variable_paths(str(Path(__file__).parent), Path(__file__).name)))
    validate_outputs(_create_config(outputs=_variable_paths("/base_dir", "base_dir/file")))

    with raises(ValueError, match=f"Path 'base_dir/file' is included in path 'base_dir'"):
        validate_outputs(_create_config(outputs=_variable_paths("base_dir", "base_dir/file")))

    with raises(ValueError, match="Path '/base_dir/file' is included in path '/base_dir'"):
        validate_outputs(_create_config(outputs=_variable_paths("/base_dir", "/base_dir/file")))


def _create_config(
        inputs: Optional[List[VariablePath]] = None,
        outputs: Optional[List[VariablePath]] = None,
) -> Config:
    if inputs is None:
        inputs = []
    if outputs is None:
        outputs = []
    return Config(
        inputs=inputs,
        outputs=outputs,
        cmd="",
        args={},
        s3_mounts=[],
        datasets=[],
        env=Environment(None, None, None),
        cloud_instance_types=['c1.4'],
        attach_project_disk=False,
        content=""
    )


def _create_env(modules: Optional[List[str]] = None) -> PythonEnv:
    if modules is None:
        modules = []
    return PythonEnv(
        version="3.10",
        local_modules_paths=modules,
        requirements=[],
    )


def _variable_paths(*paths: str) -> List[VariablePath]:
    return [VariablePath(path=path) for path in paths]
