from aiogram import Router


def setup_message_routers() -> Router:
    from . import catch_bill, cmd_start, unknown_message

    router = Router()
    router.include_router(cmd_start.router)
    router.include_router(catch_bill.router)
    router.include_router(unknown_message.router)
    # router.include_router(errors.router)

    return router
