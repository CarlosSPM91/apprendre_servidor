
from fastapi import HTTPException, status


def manage_role_except(e: HTTPException):
    if e.status_code == status.HTTP_409_CONFLICT:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= {
                    "status": "error",
                    "message": "Role already exist"
                }
            )
    if e.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= {
                    "status": "error",
                    "message": "Role not found"
                }
            )
    raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

def manage_user_except(e: HTTPException):
    if e.status_code == status.HTTP_409_CONFLICT:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= {
                    "status": "error",
                    "message": "User already exist"
                }
            )
    if e.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= {
                    "status": "error",
                    "message": "User not found"
                }
            )
    raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

def manage_auth_except(e: HTTPException):
    raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )