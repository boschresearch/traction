import os
import time

import uvicorn
from fastapi import FastAPI

from api.core.exception_handlers import add_exception_handlers
from api.endpoints.routes.webhooks import get_webhookapp
from api.core.config import settings
from api.innkeeper_main import get_innkeeperapp
from api.tenant_main import get_tenantapp
from acapy_wrapper.acapy_wrapper_main import get_acapy_wrapper_app

os.environ["TZ"] = settings.TIMEZONE
time.tzset()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
        middleware=None,
    )
    return application


app = get_application()
webhook_app = get_webhookapp()
app.mount("/webhook", webhook_app)

tenant_app = get_tenantapp()
app.mount("/tenant", tenant_app)

innkeeper_app = get_innkeeperapp()
app.mount("/innkeeper", innkeeper_app)

acapy_wrapper_app = get_acapy_wrapper_app()
app.mount("/tenant_acapy", acapy_wrapper_app)

add_exception_handlers(app)
add_exception_handlers(webhook_app)
add_exception_handlers(tenant_app)
add_exception_handlers(innkeeper_app)
add_exception_handlers(acapy_wrapper_app)


@app.get("/", tags=["liveness"])
def main():
    return {"status": "ok", "health": "ok"}


if __name__ == "__main__":
    print("main.")
    uvicorn.run(app, host="0.0.0.0", port=8080)
