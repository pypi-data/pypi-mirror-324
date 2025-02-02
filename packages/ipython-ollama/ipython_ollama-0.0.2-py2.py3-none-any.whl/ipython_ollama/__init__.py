def load_ipython_extension(ip):
    """API for IPython to recognize this module as an IPython extension."""
    from .magic import LLMMagics

    ip.register_magics(LLMMagics)
