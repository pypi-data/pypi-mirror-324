from typing import Any

import pytest
from fastapi import FastAPI

from anydi import Container
from anydi.ext.fastapi import Inject, install


def test_inject_param_missing_interface() -> None:
    param = Inject()

    with pytest.raises(TypeError) as exc_info:
        _ = param.interface

    assert str(exc_info.value) == "Interface is not set."


def test_install_without_annotation() -> None:
    container = Container(strict=True)

    @container.provider(scope="singleton")
    def message() -> str:
        return "Hello"

    app = FastAPI()

    @app.get("/hello")
    def say_hello(message=Inject()) -> Any:  # type: ignore[no-untyped-def]
        return message

    with pytest.raises(TypeError) as exc_info:
        install(app, container)

    assert str(exc_info.value) == (
        "Missing `tests.ext.fastapi.test_ext.test_install_without_annotation"
        ".<locals>.say_hello` parameter `message` annotation."
    )


def test_install_unknown_annotation() -> None:
    container = Container(strict=True)

    app = FastAPI()

    @app.get("/hello")
    def say_hello(message: str = Inject()) -> Any:
        return message

    with pytest.raises(LookupError) as exc_info:
        install(app, container)

    assert str(exc_info.value) == (
        "`tests.ext.fastapi.test_ext.test_install_unknown_annotation"
        ".<locals>.say_hello` has an unknown dependency parameter `message` "
        "with an annotation of `str`."
    )
