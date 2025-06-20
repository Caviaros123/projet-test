import httpx
import asyncio
import time

BASE_URL = "https://hire-game.pertimm.dev/api/v1.1"
REGISTER_URL = f"{BASE_URL}/auth/register/"
LOGIN_URL = f"{BASE_URL}/auth/login/"
APPLICATION_URL = f"{BASE_URL}/job-application-request/"

USERNAME = "princethierry2021+10@gmail.com"
PASSWORD = "11221122"
EMAIL = "princethierry2021+10@gmail.com"
FIRST_NAME = "Princethierry"
LAST_NAME = "Makwati"

async def runApp():
    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json={"email": USERNAME, "password": PASSWORD})

        if response.status_code != 200:
            return {
                "error": "Erreur de connexion",
                "status_code": response.status_code,
                "response_text": response.text
            }

        try:
            token = response.json().get("token")
        except Exception as e:
            return {"error": "Erreur", "exception": str(e), "text": response.text}

        if not token:
            return {"error": "token non trouvé"}

        headers = {"Authorization": f"Token {token}"}

        app_data = {"email": EMAIL, "first_name": FIRST_NAME, "last_name": LAST_NAME}
        response = await client.post(APPLICATION_URL, json=app_data, headers=headers)

        try:
            app_response = response.json()
        except Exception as e:
            return {"error": "Erreur", "exception": str(e), "text": response.text}

        status_url = app_response.get("url")
        if not status_url:
            return {"error": "Aucune URL de statut retournée"}

        confirmation_url = None
        start = time.time()
        while time.time() - start < 30:
            res = await client.get(status_url, headers=headers)
            try:
                data = res.json()
            except Exception as e:
                return {"error": "Erreur", "exception": str(e), "text": res.text}

            if data.get("status") == "COMPLETED":
                confirmation_url = data.get("confirmation_url")
                break
            await asyncio.sleep(3)

        if not confirmation_url:
            return {"error": "Not found"}

        confirm_data = {"confirmed": True}
        res = await client.patch(confirmation_url, json=confirm_data, headers=headers)

        try:
            confirm_data = res.json()
        except Exception as e:
            return {"error": "Erreur", "exception": str(e), "text": res.text}

        return {
            "status_code": res.status_code,
            "response": confirm_data
        }
