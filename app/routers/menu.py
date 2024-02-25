from fastapi import Response,status,HTTPException, Depends, APIRouter,Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session , class_mapper
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import IntegrityError
from typing import List ,Dict ,Union
from .. import models, schemas ,oauth2
from ..database import get_db

router = APIRouter(
    prefix="/menu",
    tags=['Menu']
)
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    try:
        menu.created_by = current_user.username
        new_menu = models.MenuPermission(**menu.dict())
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=
                            "Menu item with the same 'pms_menu_name and to_name' alreay exists.")
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    menu_query = db.query(models.MenuPermission).filter(models.MenuPermission.id == id)
    menu = menu_query.first()

    if menu == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"menu with id {id} does not exist")
    menu_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success"})

@router.put("/{id}")
def update_menu(id: int, updated_menu: schemas.MenuCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    menu_query  = db.query(models.MenuPermission).filter(models.MenuPermission.id == str(id))
    menu = menu_query.first()
    if menu == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Menu with id {id} does not exist")
    menu_query.update(updated_menu.dict(),synchronize_session=False)
    db.commit()
    return menu_query.first()
# @router.get("/",response_model=Dict[str, Union[List[schemas.MenuAssignedRoleOut],str]])
@router.get("/")
def getmenu(db: Session = Depends(get_db),
                              current_user: int = Depends(oauth2.get_current_user)):
    query_results  = db.query(models.MenuPermission).all()
    # Retrieve all columns from the table
    table_columns = [column.name for column in class_mapper(models.MenuPermission).mapped_table.columns]
    data = []
    for item in query_results:
        item_data = {}
        for column in table_columns:
            item_data[column] = getattr(item, column)
        data.append(item_data)
    success_status = True if data else False
    response_data = {
        "data": data,
        "status": success_status,
    }
    return response_data

@router.get("/getmenuassignedrole")
async def getmenuassignedrole(db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    role_id = current_user.roleid
    menu_query = db.query(
            models.UspRuleNpmsAssign.pmsid,
            models.UspRuleNpmsAssign.roleid,
            models.UspRuleNpmsAssign.p_view,
            models.UspRuleNpmsAssign.p_view_data,
            models.UspRuleNpmsAssign.p_refresh,
            models.UspRuleNpmsAssign.p_search,
            models.UspRuleNpmsAssign.p_add,
            models.UspRuleNpmsAssign.p_edit,
            models.UspRuleNpmsAssign.p_delete,
            models.UspRuleNpmsAssign.p_save,
            models.UspRuleNpmsAssign.p_print,
            models.UspRuleNpmsAssign.p_import,
            models.UspRuleNpmsAssign.p_export,
            models.MenuPermission.pms_menu_name,
            models.MenuPermission.pms_menu_level,
            models.MenuPermission.pms_parent_id,
            models.MenuPermission.pms_menu_type,
            models.MenuPermission.to_name.label('pms_page_name'),
            models.MenuPermission.pms_menu_image,
            models.MenuPermission.pms_menu_index
        ).join(models.MenuPermission,models.UspRuleNpmsAssign.pmsid == models.MenuPermission.id, isouter=True
        ).filter(models.UspRuleNpmsAssign.roleid == role_id
        ).order_by(models.UspRuleNpmsAssign.id).all()
    if not menu_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role ID not found Your request messing!!")
    data = []
    for item in menu_query:
        item_data = {
            "pmsid": str(item.pmsid),
            "roleid": str(item.roleid),
            "p_view": str(item.p_view),
            "p_view_data": str(item.p_view_data),
            "p_refresh": str(item.p_refresh),
            "p_search": str(item.p_search),
            "p_add": str(item.p_add),
            "p_edit": str(item.p_edit),
            "p_delete": str(item.p_delete),
            "p_save": str(item.p_save),
            "p_print": str(item.p_print),
            "p_import": str(item.p_import),
            "p_export": str(item.p_export),
            "pms_menu_name": item.pms_menu_name,
            "pms_menu_level": str(item.pms_menu_level),
            "pms_parent_id": str(item.pms_parent_id),
            "pms_menu_type": str(item.pms_menu_type),
            "pms_page_name": item.pms_page_name,
            "pms_menu_image": item.pms_menu_image,
            "pms_menu_index": str(item.pms_menu_index)
        }
        data.append(item_data)
    success_status = True if data else False
    response_data = {
        "data": data,
        "status": success_status,
    }
    encoded_response = jsonable_encoder(response_data)
    return encoded_response
    
        # menu_query = db.query(models.UspRuleNpmsAssign,models.MenuPermission
    #                     ).join(models.MenuPermission,models.UspRuleNpmsAssign.pmsid == models.MenuPermission.pmsid, isouter=True
    #                     ).filter(models.UspRuleNpmsAssign.roleid == role_id
    #                     ).order_by(models.UspRuleNpmsAssign.rnpa_id).all()
    # uspRule_columns = [column.name for column in class_mapper(models.UspRuleNpmsAssign).mapped_table.columns]
    # menu_columns = [column.name for column in class_mapper(models.MenuPermission).mapped_table.columns]

    # data = []
    # for item in menu_query:
    #     item_data = {}
    #     for column in uspRule_columns:
    #         item_data[column] = getattr(item[0], column)
    #     for column in menu_columns:
    #         item_data[column] = getattr(item[1], column)
    #     data.append(item_data)
    # success_status = True if data else False
    # response_data = {
    #     "data": data,
    #     "status": success_status,
    # }
@router.get("/listmenubylevel")
def listmenubylevel():
    return {"status":"get data successfully"}

@router.get("/assignmenutorole")
def assignmenutorole():
    return {"status":"get data successfully"}





    