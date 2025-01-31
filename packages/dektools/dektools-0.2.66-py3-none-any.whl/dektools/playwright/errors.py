error_default_returned = type('error_default_returned', (), {})


def _sure(x, default):
    if x is error_default_returned:
        return default
    return x


async def async_safe_process(
        func, default=None, closed=None, timeout=None, message=None, others=None, messages=None, stealth=True,
        args=None, kwargs=None):
    if stealth:
        from patchright._impl._errors import Error, is_target_closed_error, TimeoutError
    else:
        from playwright._impl._errors import Error, is_target_closed_error, TimeoutError
    try:
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs
        return _sure(await func(*args, **kwargs), default)
    except Error as e:
        if is_target_closed_error(e):
            if closed:
                return _sure(await closed(e), default)
        elif isinstance(e, TimeoutError):
            if timeout:
                return _sure(await timeout(e), default)
        else:
            cursor = None
            if messages:
                for msg in messages:
                    if msg in e.message:
                        cursor = msg
                        break
            if cursor is not None:
                if message:
                    return _sure(await message(e, cursor), default)
            else:
                if others:
                    return _sure(await others(e), default)
                else:
                    raise e from None
    return default


async def async_none(e, *args):
    pass


async def async_raise(e, *args):
    raise e from None


def sync_safe_process(
        func, default=None, closed=None, timeout=None, message=None, others=None, messages=None, stealth=True,
        args=None, kwargs=None):
    if stealth:
        from patchright._impl._errors import Error, is_target_closed_error, TimeoutError
    else:
        from playwright._impl._errors import Error, is_target_closed_error, TimeoutError
    try:
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs
        return _sure(func(*args, **kwargs), default)
    except Error as e:
        if is_target_closed_error(e):
            if closed:
                return _sure(closed(e), default)
        elif isinstance(e, TimeoutError):
            if timeout:
                return _sure(timeout(e), default)
        else:
            cursor = None
            if messages:
                for msg in messages:
                    if msg in e.message:
                        cursor = msg
                        break
            if cursor is not None:
                if message:
                    return _sure(message(e, cursor), default)
            else:
                if others:
                    return _sure(others(e), default)
                else:
                    raise e from None
    return default


def sync_none(e, *args):
    pass


def sync_raise(e, *args):
    raise e from None
