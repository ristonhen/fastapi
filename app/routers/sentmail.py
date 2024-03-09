from fastapi import APIRouter, Depends , status, HTTPException , Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   #instead : schemas.UserLogin
from sqlalchemy.orm import Session
from .. import database, schemas, models,utils, oauth2
from datetime import datetime, timedelta, timezone
# from .. encryption_utils import encrypt, decrypt
# from .. generate_utills import generate_reset_token
from ..email_utils import send_reset_email, send_reviewaml_email
from .. config import settings
from ..utils import decrypt, generate_reset_token,encrypt
import time
from typing import List
router = APIRouter(
    prefix="/api",
    tags=['SentMail']
)

@router.post("/amlreview/")
def reviewaml_email(
                    # ids: List[int], 
                    request: schemas.SentEmailReviewAmlList, 
                    db: Session = Depends(database.get_db),
                    current_user: int = Depends(oauth2.get_current_user)):

    query = db.query(
        models.EmailSenderInfor.password_encrypt, 
        models.EmailSenderInfor.secret_key, 
        models.User.email
    ).join(models.User).filter(models.EmailSenderInfor.user_id == models.User.id).first()
    
    sender_name = current_user.username
    sender_email = query.email
    secret_key = query.secret_key
    password_encrypt =query.password_encrypt
    sender_password = ""
    
    sender_password = decrypt(password_encrypt, secret_key)
    
    # existing = db.query(models.EmailData).filter(models.EmailData.id.in_(ids)).all()
    
    for mail_data in request.email_data:
        # Send the password reset link to the user's email
        subject = f'Review User AML/CFT System for {mail_data.branchname} Branch'
        sent = send_reviewaml_email(
            branchname= mail_data.branchname,
            sender_name = sender_name,
            sender_email= sender_email,
            sender_password= sender_password,
            subject= subject, 
            email_to = mail_data.email_to, 
            cc_email = mail_data.cc_email, 
            pdfimage = mail_data.pdfimage
        )
        time.sleep(5)  # Sleep for 2 minutes (120 seconds)
    return {"status": True,"message": "AML sent mail to .. successfully"}

@router.post("/senderinfor/")
def createmailSender(request: schemas.EmailSenderInfor, db: Session = Depends(database.get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    
    hashpass = db.query(models.User.password).filter(models.User.id == request.user_id).first()
    # print(f"hashpass.password: { hashpass.password }")
    
    # print(f"Plaintext: {request.password_encrypt}")
    
    encrypted = encrypt(request.password_encrypt, hashpass.password, length=32)
    # print(f"password encrypt: {encrypted}")
    
    # decrypted = decrypt(encrypted,hashpass.password)
    # print(decrypted)
    
    request.created_by = current_user.username
    request.created_date = datetime.now()
    request.password_encrypt = encrypted
    request.secret_key = hashpass.password
    
    new_sender = models.EmailSenderInfor(**request.dict())
    db.add(new_sender)
    db.commit()
    db.refresh(new_sender)

    return {"status": True,"message": "", "data": request}