debug_text: list[str] = []

def debug(*args, **kw_args) -> None:
    parts = [str(a) for a in args]
    parts += [f"{k}: {v}" for k,v in kw_args.items()]
    debug_text.append(", ".join(parts))

def render_debug() -> None:
    pen(15, 15, 15)
    cursor()
    for debug_line in debug_text:
        text(debug_line)
    debug_text.clear()