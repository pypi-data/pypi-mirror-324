import multiprocessing
import os
import threading
from multiprocessing import forkserver
from reboot.aio.once import Once


def _initialize_multiprocessing_start_method():
    # We don't want any threads to be running when we try and spawn
    # the forkserver via `multiprocessing.set_start_method()`, but we
    # make an exception (for now) when we're getting called
    # from nodejs as those threads *must* be created in order to call
    # into us in the first place.
    #
    # See 'reboot/nodejs/python.py'.
    allowed_thread_amount = 1

    if os.environ.get(
        'REBOOT_NODEJS_EVENT_LOOP_THREAD',
        'false',
    ).lower() == 'true':
        allowed_thread_amount = 2

    if threading.active_count() > allowed_thread_amount:
        raise RuntimeError(
            'Reboot must be initialized before creating any threads'
        )

    multiprocessing_start_method = multiprocessing.get_start_method(
        allow_none=True
    )

    if multiprocessing_start_method is None:
        # We want to use 'forkserver', which should be set before any
        # threads are created, so that users _can_ use threads in
        # their tests and we will be able to reliably fork without
        # worrying about any gotchas due to forking a multi-threaded
        # process.
        multiprocessing.set_start_method('forkserver')
    elif multiprocessing_start_method != 'forkserver':
        raise RuntimeError(
            f"Reboot requires the 'forkserver' start method but you "
            f"appear to have configured '{multiprocessing_start_method}'"
        )

    # We need to ensure the forkserver is running before we start
    # creating any threads. Otherwise forkserver might inherit some threads from
    # the parent process.
    forkserver.ensure_running()

    assert threading.active_count() == allowed_thread_amount, (
        'Reboot must be initialized before creating any threads'
    )


# We're using a global here because we only want to initialize the
# multiprocessing start method once per process.
initialize_multiprocessing_start_method_once = Once(
    _initialize_multiprocessing_start_method
)
