from fastapi import APIRouter, Depends , status, HTTPException , Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   #instead : schemas.UserLogin
from sqlalchemy.orm import Session
from .. import database, schemas, models,utils, oauth2
from datetime import datetime, timedelta, timezone
# from .. encryption_utils import encrypt, decrypt
# from .. generate_utills import generate_reset_token
from ..email_utils import send_reset_email, send_reviewaml_email
from .. config import settings
from ..utils import decrypt, generate_reset_token
import time

router = APIRouter(
    tags=['Authentication']
)

# @router.post("/logins")
# def login(user_credentail: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
#     user = db.query(models.User).filter(models.User.email == user_credentail.email).first()

#     if user.status == False:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Inactive")
#     # if not user:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#     #                         detail=f"Invalid Credentails")
#     # if not utils.verify(user_credentail.password , user.password):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#     #                         detail=f"Invalid Credentails")
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#                             detail=f"Invalid Credentails (Username)")
#     if not utils.verify(user_credentail.password , user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
#                             detail=f"Invalid Credentails (Password)")
    
#     # create token
#     # retuern token

#     # access_token = oauth2.create_access_token(data={"user_id": user.id})
#     # return {"access_token": access_token, "token_type": "bearer"}
#     return {"status":"successed"}

@router.post("/login",response_model=schemas.Token)
def login(user_credentail: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentail.username).first()

    if user.status == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Inactive")
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentails (Username)")
    if not utils.verify(user_credentail.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentails (Password)")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token,"user": user}

# @router.put("/changepwd")
# def change_password(user_credentail: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db),
#                     current_user: int = Depends(oauth2.get_current_user)):
#     user = db.query(models.User).filter(models.User.email == user_credentail.username).first()

#     if not utils.verify(user_credentail.password, user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect current password")

#     # user.password = utils.hash_password(new_password)
#     # db.commit()
#     print(user_credentail.newpasswd)
#     return {"status": "Password changed successfully"}

@router.put("/changepwd")
def change_password(user_credentail: schemas.ChangePasswordRequest,
                    db: Session = Depends(database.get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.email == user_credentail.username).first()

    if not utils.verify(user_credentail.currentassword, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect current password")
    user.last_pwd_modified_date = datetime.now()
    user.password = utils.hash(user_credentail.newpassword)
    db.commit()

    return {"message": "Password changed successfully","status":True}

@router.post("/resetpwd")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Generate a password reset token
    reset_token = generate_reset_token()

    # Save the reset token in the user's record or a separate reset token table (depending on implementation)
    user.reset_token = reset_token
    user.reset_token_expiration = datetime.now() + timedelta(hours=1)
    db.commit()
    # Send the password reset link to the user's email
    send_reset_email(user.email, reset_token)
    return {"status": True,"message": "Password reset link sent successful"}

@router.post("/amlreview")
def reviewaml_email(request: schemas.SentEmailReviewAmlList, db: Session = Depends(database.get_db)):

    for mail_data in request.email_data:
        # Send the password reset link to the user's email
        subject = f'Review User AML/CFT System for {mail_data.branchname} Branch'
        send_reviewaml_email(
            subject=subject, 
            email_to = mail_data.email_to, 
            cc_email = mail_data.cc_email, 
            pdfimage = mail_data.pdfimage
        )
        time.sleep(5)  # Sleep for 2 minutes (120 seconds)
    return {"status": True,"message": "Password reset link sent successful"}

@router.get("/resetpwd/{param}")
def verify_reset_token(param: str, db: Session = Depends(database.get_db)):
    
    # Replace "-" with "/"
    param = param.replace("-", "/")
    try:
        # Decrypt the value using the key
        decrypted_param = decrypt(param, settings.secret_key)
        print(decrypted_param)
        # Split the decrypted value using "_"
        split_string = decrypted_param.split("_")
        credential = split_string[0]
        token = split_string[1]
    except Exception as e:
        # Handle decryption or other errors
        raise HTTPException(status_code=422, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.email == credential).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.reset_token != token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
    
    if user.reset_token_expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expired reset token")
    
    return {"credential": credential, "status": True, "message": "Token verification successful" }

@router.put("/resetpwd")
def verify_reset_token_bylink(request: schemas.VerifyResetTokenRequestByLink, 
                       db: Session = Depends(database.get_db)):
    # Replace "^" with "/"
    request.token = request.token.replace("-", "/")

    # Decrypt the value using the key
    request.token = decrypt(request.token, settings.secret_key)
    # Split the value using "_"
    split_string = request.token.split("_")

    # Assign the split values to variables
    credential = split_string[0]
    token = split_string[1]
    print(token)
    user = db.query(models.User).filter(models.User.email == credential).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.reset_token != token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
    
    if user.reset_token_expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expired reset token")

    # Reset token is valid, allow the user to update their password
    if request.password == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="New Password Require")
    user.password = utils.hash(request.password)
    user.reset_token = None
    user.reset_token_expiration = None
    user.last_pwd_modified_date = datetime.now()
    db.commit()

    return {"status": True}

