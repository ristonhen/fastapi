from fastapi import Response,status,HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from .. import models, schemas ,oauth2
from ..database import get_db
from sqlalchemy.orm import aliased,Session
from sqlalchemy import select, case



session = Session()

router = APIRouter(
    prefix="/index",
    tags=['Tesing']
)


@router.get("/")
def get_post(db: Session = Depends(get_db)):

    p = aliased(models.UspPermission)
    pp = aliased(models.UspPermission)

    query = db.query(
        p,
        pp.pms_menu_name.label("pms_parent_name")
    ).outerjoin(
        pp,
        p.pms_parent_id == pp.pmsid
    ).order_by(
        p.pms_menu_type.asc(),
        case([(p.pms_parent_id.is_(None), p.pmsid)], else_=p.pms_parent_id).asc(),
        case([(p.pms_parent_id.is_(None), 0)], else_=p.pms_menu_index).asc()
    )

    menu_permissions = query.all()

    return menu_permissions