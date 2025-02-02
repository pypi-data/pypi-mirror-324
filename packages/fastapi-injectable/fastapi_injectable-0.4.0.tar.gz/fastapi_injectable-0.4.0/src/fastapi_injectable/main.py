import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar, cast

from fastapi import FastAPI, Request
from fastapi.dependencies.utils import get_dependant, solve_dependencies

from .async_exit_stack import async_exit_stack_manager
from .cache import dependency_cache
from .exception import DependencyResolveError

logger = logging.getLogger(__name__)
T = TypeVar("T")
P = ParamSpec("P")
_app: FastAPI | None = None
_app_lock = asyncio.Lock()


async def register_app(app: FastAPI) -> None:
    """Register the given FastAPI app for constructing fake request later."""
    global _app  # noqa: PLW0603
    async with _app_lock:
        _app = app


def _get_app() -> FastAPI | None:
    """Get the registered FastAPI app."""
    return _app


async def resolve_dependencies(
    func: Callable[P, T] | Callable[P, Awaitable[T]], *, use_cache: bool = True, raise_exception: bool = False
) -> dict[str, Any]:
    """Resolve dependencies for the given function using FastAPI's dependency injection system.

    This function resolves dependencies defined via FastAPI's dependency mechanism
    and returns a dictionary of resolved arguments for the given function.

    Args:
        func: The function for which dependencies need to be resolved. It can be a synchronous
            or asynchronous callable.
        use_cache: Whether to use a cache for dependency resolution. Defaults to True.
        raise_exception: Whether to raise an exception when errors occur during dependency
            resolution. If False, errors are logged as warnings. Defaults to False.

    Returns:
        A dictionary mapping argument names to resolved dependency values.

    Raises:
        DependencyResolveError: If `raise_exception` is True and errors occur during dependency resolution.

    Notes:
        - A fake HTTP request is created to mimic FastAPI's request-based dependency resolution.
        - Dependency resolution errors are either logged or raised as exceptions based on `raise_exception`.
    """
    root_dep = get_dependant(path="command", call=func)
    fake_request_scope: dict[str, Any] = {
        "type": "http",
        "headers": [],
        "query_string": "",
    }
    app = _get_app()
    if app is not None:
        fake_request_scope["app"] = app
    fake_request = Request(fake_request_scope)
    root_dep.call = cast(Callable[..., Any], root_dep.call)
    async_exit_stack = await async_exit_stack_manager.get_stack(root_dep.call)
    cache = dependency_cache.get() if use_cache else None
    resolved = await solve_dependencies(
        request=fake_request,
        dependant=root_dep,
        async_exit_stack=async_exit_stack,
        embed_body_fields=False,
        dependency_cache=cache,
    )
    if cache is not None:
        cache.update(resolved.dependency_cache)
    if resolved.errors:
        if raise_exception:
            raise DependencyResolveError(resolved.errors)
        logger.warning(f"Something wrong when resolving dependencies of {func}, errors: {resolved.errors}")

    return resolved.values
