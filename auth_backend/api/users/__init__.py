from fastapi import APIRouter

from .common import UserResponse
from .login import login as login_endpoint
from .register import register_user as register_user_endpoint


router = APIRouter()


router.add_api_route(
    "/login",
    login_endpoint,
    methods={"POST", },
)


router.add_api_route(
    "/registrate",
    register_user_endpoint,
    methods={"POST", },
)
