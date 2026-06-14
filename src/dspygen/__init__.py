# import inject
# import EventKit
#
# # import inject
# # from dspygen.di_configure import configure
# #
# # inject.configure(configure)
#
# # Configure the injector
# def configure_injector(binder):
#     event_store = EventKit.EKEventStore.alloc().init()
#     binder.bind(EventKit.EKEventStore, event_store)
#
#
# inject.configure(configure_injector)

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("dspygen")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__all__ = ["__version__"]