import datetime as dt
from functools import wraps
import humanize
import inspect
import orjson
import json
from functools import partial
from typing import Callable, TypeVar, Any
import narwhals as nw

F = TypeVar('F', bound=Callable[..., Any])

def callback(callback_fn: Callable[[Any], None]) -> Callable[[F], F]:
    @wraps(callback_fn)
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            callback_fn(result)
            return result
        return wrapper
    return decorator


def print_step(
    func=None,
    *,
    time_taken=True,
    shape=True,
    names=True,
    dtypes=True,
    display_call=True,
    log_error=True,
    print_fn=lambda d: print(orjson.dumps(d).decode("utf-8")),
):
    """Decorates a function that transforms a dataframe to add automated logging statements.

    Parameters
    ----------
    func : Callable | None, default=None
        The function to decorate with logs. If None, returns a partial function with the given arguments.
    time_taken : bool, default=True
        Whether or not to log the time it took to run a function.
    shape : bool, default=True
        Whether or not to log the shape of the output result.
    names : bool, default=False
        Whether or not to log the names of the columns of the result.
    dtypes : bool, default=False
        Whether or not to log the dtypes of the result.
    print_fn : Callable, default=print
        Print function to use (default is `lambda d: print(orjson.dumps(d).decode("utf-8"))`)
    display_call : bool, default=True
        Whether or not to display the function call with all the arguments given to the function.
    log_error : bool, default=True
        Whether or not to add the Exception message to the log if the function fails.

    Returns
    -------
    Callable
        The decorated function.

    Examples
    --------
    ```py
    @log_step
    def remove_outliers(df, min_obs=5):
        pass
    ```
    """

    if func is None:
        return partial(
            print_step,
            time_taken=time_taken,
            shape=shape,
            names=names,
            dtypes=dtypes,
            print_fn=print_fn,
            display_call=display_call,
            log_error=log_error,
        )

    names = False if dtypes else names

    @wraps(func)
    def wrapper(*args, **kwargs):
        tic = dt.datetime.now()

        optional_strings = []
        try:
            result = nw.from_native(func(*args, **kwargs))
            outputs = {"step": func.__name__}
            if time_taken:
                outputs["time"] = humanize.naturaldelta(dt.datetime.now() - tic)
            if shape:
                outputs["n_obs"], outputs["n_col"] = result.shape
            if names:
                outputs["names"] = result.columns.to_list()
            if dtypes:
                schema = result.collect_schema()
                outputs["dtypes"] = {k: str(v) for k, v in zip(schema.names(), schema.dtypes())}
            if display_call:
                func_args = inspect.signature(func).bind(*args, **kwargs).arguments
                func_args_str = ",".join("{} = {!r}".format(*item) for item in list(func_args.items())[1:])
                outputs["func_call"] = f"{func.__name__}(" + func_args_str + ")"
            return result.to_native()
        except Exception as exc:
            optional_strings = [
                f"time={dt.datetime.now() - tic}" if time_taken else None,
                "FAILED" + (f" with error: {exc}" if log_error else ""),
            ]
            raise
        finally:
            print_fn(outputs)

    return wrapper

__all__ = [
    "print_step",
    "callback",
]
