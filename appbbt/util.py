def args_to_str(args, kwargs):
    s = ', '.join((
        *map(repr, args),
        *('{}={!r}'.format(n, v) for n, v in kwargs.items())
    ))
    return s
