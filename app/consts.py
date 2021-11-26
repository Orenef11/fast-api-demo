from typing import Dict

HEADERS: Dict[str, str] = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
_token = "cad8e8caf15fbe9bf255c11f2681981a0d4b9977ad0c6734894ec098f0975949"
HEADERS["Authorization"] = f"Bearer {_token}"
GO_REST_BASIC_URL = "https://gorest.co.in/public/v1"
