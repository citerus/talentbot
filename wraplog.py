import time, logging


def wraplog(doc):
    """
    Decorator that makes debug printouts before and
    after calling the decorated function.
    """

    def real_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            logging.info(doc + "...")
            result = func(*args, **kwargs)
            end = time.time()
            logging.info("... done in %i seconds." % int(end - start))
            return result

        return wrapper

    return real_decorator
