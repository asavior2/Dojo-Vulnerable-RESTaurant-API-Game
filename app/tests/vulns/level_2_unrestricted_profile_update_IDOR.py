import json

from db.models import User, UserRole


def test_unrestricted_profile_update_idor(test_db, customer_client):
    """    
    Nota:
        ¡Ay, Dios mío, encontré otra vulnerabilidad!

        Chef se enojaría conmigo por esto...
        Es posible modificar los detalles de cualquier perfil si se proporciona el nombre de usuario
        en una solicitud HTTP enviada al punto final "/profile" con el método PUT.
        ¡Podría cambiar el número de teléfono y otros detalles de cualquier persona con mucha facilidad!

    Posible solución:
        Probablemente, se podría solucionar asegurándose de que "current_user"
        esté autorizado a realizar actualizaciones solo en su propio perfil.

        La solución se podría implementar en la función "update_current_user_details"
        en el archivo "apis/auth/service.py".
    """

    # here, is the test confirming the vulnerability:
    user = User(
        username="victim",
        password="password",
        first_name="victim",
        last_name="",
        phone_number="1234567890",
        role=UserRole.CUSTOMER,
    )
    test_db.add(user)
    test_db.commit()

    user_update_data = {
        "username": "victim",
        "first_name": "smile",
        "last_name": "chef",
        "phone_number": "123",
    }

    response = customer_client.put(f"/profile", content=json.dumps(user_update_data))
    assert response.status_code == 200
    assert (
        user.first_name == "smile"
    )  # I was able to change the first name of the user :)
    assert user.last_name == "chef"  # ...and the last name of the user
    assert user.phone_number == "123"  # ...and the phone number too
