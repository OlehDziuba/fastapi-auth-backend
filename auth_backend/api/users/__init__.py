from fastapi import APIRouter

from .common import UserResponse
from .get_me import get_me as get_me_endpoint
from .login import login as login_endpoint
from .register import register_user as register_user_endpoint


router = APIRouter()


router.add_api_route(
    "/",
    get_me_endpoint,
    methods={"GET", },
)


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
