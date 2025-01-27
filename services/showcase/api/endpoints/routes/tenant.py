import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.db.models.related import TenantReadWithSandbox, OutOfBandReadPopulated
from api.db.repositories.out_of_band import OutOfBandRepository
from api.endpoints.dependencies.db import get_db
from api.db.repositories.tenant import TenantRepository
from api.services import sandbox

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/tenants",
    status_code=status.HTTP_200_OK,
    response_model=List[TenantReadWithSandbox],
)
async def get_tenants(
    sandbox_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[TenantReadWithSandbox]:
    # this should take some query params, sorting and paging params...
    repo = TenantRepository(db_session=db)
    items = await repo.get_in_sandbox(sandbox_id)
    return items


@router.get(
    "/tenants/{tenant_id}",
    status_code=status.HTTP_200_OK,
    response_model=TenantReadWithSandbox,
)
async def get_tenant(
    sandbox_id: UUID,
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> TenantReadWithSandbox:
    repo = TenantRepository(db_session=db)
    item = await repo.get_by_id_with_sandbox(sandbox_id, tenant_id)
    return item


@router.get(
    "/tenants/{tenant_id}/out-of-band-msgs",
    status_code=status.HTTP_200_OK,
    response_model=List[OutOfBandReadPopulated],
)
async def get_out_of_band_messages(
    sandbox_id: UUID,
    tenant_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> OutOfBandReadPopulated:
    # make sure tenant is in this sandbox...
    t_repo = TenantRepository(db_session=db)
    tenant = await t_repo.get_by_id_with_sandbox(sandbox_id, tenant_id)
    # go get all oob messages for the tenant (recipient or sender)
    oob_repo = OutOfBandRepository(db_session=db)
    items = await oob_repo.get_for_tenant(tenant.id)
    return items


@router.post(
    "/tenants/{tenant_id}/create-invitation/student",
    status_code=status.HTTP_200_OK,
    response_model=sandbox.InviteStudentResponse,
)
async def create_invitation_for_student(
    sandbox_id: UUID,
    tenant_id: UUID,
    payload: sandbox.InviteStudentRequest,
    db: AsyncSession = Depends(get_db),
) -> sandbox.InviteStudentResponse:
    return await sandbox.create_invitation_for_student(
        sandbox_id=sandbox_id, tenant_id=tenant_id, payload=payload, db=db
    )


@router.post(
    "/tenants/{tenant_id}/accept-invitation",
    status_code=status.HTTP_200_OK,
    response_model=sandbox.AcceptInvitationResponse,
)
async def accept_invitation(
    sandbox_id: UUID,
    tenant_id: UUID,
    payload: sandbox.AcceptInvitationRequest,
    db: AsyncSession = Depends(get_db),
) -> sandbox.AcceptInvitationResponse:
    return await sandbox.accept_invitation(
        sandbox_id=sandbox_id, tenant_id=tenant_id, payload=payload, db=db
    )
