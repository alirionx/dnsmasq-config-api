import uuid
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pysystemd import ServiceManager, ServiceStatus
import uvicorn
from typing import Literal

from settings import settings
import tools
from models import (
    ApiStatus,
    SystemdStatus,
    HostRecord
)


#-Build and prep the App--------------------------------------------
tags_metadata = [
    {
        "name": "api-control",
        "description": "API status and testing",
    },
    {
        "name": "host-records",
        "description": "manage local dns host records",
    },
    {
        "name": "systemd",
        "description": "manage systemd service for DnsMasq",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

#-Custom Middleware Functions----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
) 

#-The Routes--------------------------------------------------------
@app.get("/api/status", tags=["api-control"], response_model=ApiStatus)
async def api_status_get(request:Request):
    item = ApiStatus(
        hostname=request.url.hostname,
        method=request.method,
        base_url=str(request.base_url),
        url_path=request.url.path,
        message="Hello from the 'DNSMasq Config Rest API'"
    )
    return item

#----------------------------------------------
@app.get("/api/dns/host-records", tags=["host-records"], response_model=list[HostRecord])
async def api_dns_host_records_get():
    items = tools.dns_host_records_get()
    return items

#------
@app.post("/api/dns/host-record", tags=["host-records"], response_model=HostRecord)
async def api_dns_host_record_post(item:HostRecord):
    hns = tools.dns_get_all_hostnames()
    for hn in item.hostnames:
        if hn in hns:
            raise HTTPException(
                status_code=409, 
                detail=f"An host record with hostname '{hn}' already exsists"
            )
    tools.dns_host_record_add(item=item)
    return item

#------
@app.put("/api/dns/host-record/{id}", tags=["host-records"], response_model=HostRecord)
async def api_dns_host_record_put(id:uuid.UUID, item:HostRecord):
    if id not in [ item.id for item in tools.dns_host_records_get() ]:
        raise HTTPException(
            status_code=404, 
            detail=f"Host record with id '{id}' not found"
        )
    new_item = tools.dns_host_record_change(id=id, item=item)
    return new_item

#------
@app.delete("/api/dns/host-record/{id}", tags=["host-records"], response_model=uuid.UUID)
async def api_dns_host_record_delete(id:uuid.UUID):
    if id not in [ item.id for item in tools.dns_host_records_get() ]:
        raise HTTPException(
            status_code=404, 
            detail=f"Host record with id '{id}' not found"
        )
    tools.dns_host_record_delete(id=id)
    return id

#------


#------

#----------------------------------------------
@app.get("/api/dns/systemd", tags=["systemd"], response_model=SystemdStatus)
async def api_systemd_get():
    from pysystemd import ServiceStatus
    status = ServiceStatus(settings.systemd_service_name)
    item = SystemdStatus(
        name=settings.systemd_service_name,
        enabled=status.is_enabled(),
        running=status.is_running()
    )
    return item

#------
@app.post("/api/dns/systemd", tags=["systemd"], response_model=SystemdStatus)
async def api_systemd_post(action:Literal["enable", "disable", "start", "stop", "reload", "restart"]):
    svc = ServiceManager(settings.systemd_service_name)
    map = {
        "enable": svc.enable, 
        "disable": svc.disable, 
        "start": svc.start, 
        "stop": svc.stop, 
        "reload": svc.reload, 
        "restart": svc.restart
    }
    chk = map[action]()
    if not chk:
        raise HTTPException(
            status_code=500,
            detail=f"failed to {action} {settings.systemd_service_name}"
        )
    status = ServiceStatus(settings.systemd_service_name)
    item = SystemdStatus(
        name=settings.systemd_service_name,
        enabled=status.is_enabled(),
        running=status.is_running()
    )
    return item

#------

#------

#----------------------------------------------





#-The Runner----------------------------------------------
if __name__ == "__main__":
    tools.helper_check_conf_files()
    uvicorn.run(
        app="__main__:app", 
        host="0.0.0.0", 
        port=settings.app_port, 
        reload=settings.app_debug
    )