import io
import shutil
import sys

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageChops, UnidentifiedImageError

from app.core.settings import BASE_DIR, UPLOAD_DIR, get_settings
from app.main import app

client = TestClient(app)


"""def test_get_home():
    response = client.get("/")
    assert response.status_code == 200"""


VALID_IMG_EXT = ["png", "jpeg", "jgp"]


def test_img_echo_with_token():
    img_save_dir = BASE_DIR.parent / "tests/images"
    settings = get_settings()
    for path in img_save_dir.glob("*"):
        try:
            img = Image.open(path)
        except UnidentifiedImageError:
            img = None
        response = client.post(
            "/v1/img",
            files={"file": open(path, "rb")},
            headers={"access-token": settings.app_auth_token},
        )
        # fext = str(path.suffix).replace('.', '')
        if img is None:
            assert response.status_code == 400
            # assert fext in response.headers['content-type']
        else:
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None
    shutil.rmtree(UPLOAD_DIR)  # delete upload dir


def test_img_echo_without_token():
    img_save_dir = BASE_DIR.parent / "tests/images"
    for path in img_save_dir.glob("*"):
        response = client.post("/v1/img", files={"file": open(path, "rb")})
        assert response.status_code == 401


@pytest.mark.skipif(sys.platform == "win32", reason="Not running on Windows os")
def test_prediction_upload_with_token():
    settings = get_settings()
    img_save_dir = BASE_DIR.parent / "tests/images"
    for path in img_save_dir.glob("*"):
        try:
            img = Image.open(path)
        except UnidentifiedImageError:
            img = None
        response = client.post(
            "/v1/predict",
            files={"file": open(path, "rb")},
            headers={"access-token": settings.app_auth_token},
        )
        # fext = str(path.suffix).replace('.', '')
        if img is None:
            assert response.status_code == 400
            # assert fext in response.headers['content-type'] !
        else:
            assert response.status_code == 200
            data = response.json()
            assert len(data.keys()) == 2


@pytest.mark.skipif(sys.platform == "win32", reason="Not running on Windows os")
def test_prediction_upload_without_token():
    img_save_dir = BASE_DIR.parent / "tests/images"
    for path in img_save_dir.glob("*"):
        response = client.post("/v1/predict", files={"file": open(path, "rb")})
        assert response.status_code == 401
