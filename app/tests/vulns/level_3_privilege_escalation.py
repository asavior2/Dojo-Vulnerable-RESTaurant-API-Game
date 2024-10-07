import json

from db.models import User, UserRole


def test_privilege_escalation(test_db, customer_client):
    """
    Nota:
        ¡Ahora comienza la parte divertida!

        ¡Pude escalar privilegios de cliente a empleado!
        Lo logré a través del punto final de API "/users/update_role"
        simplemente cambiando un rol.

        Con este rol, ahora puedo acceder a los puntos finales restringidos para empleados...

        ¿Qué puedo hacer con estos permisos a continuación? :thinking_face:

        Por cierto, mi empleador no respondió a mis hallazgos iniciales.
        Esta API es muy vulnerable...

    Posible solución:
        Se podría solucionar asegurándose de que solo los empleados
        o Chef puedan otorgar el rol de Empleado.

        Probablemente, la solución se podría implementar en el archivo "apis/users/service.py"
        en la función "update_user_role", de manera similar a la primera vulnerabilidad.
    """

    # here, is the test confirming the vulnerability:
    user = User(
        username="regular_customer",
        password="password",
        first_name="customer",
        last_name="",
        phone_number="1234567890",
        role=UserRole.CUSTOMER,
    )
    test_db.add(user)
    test_db.commit()

    user_update_data = {
        "username": "regular_customer",
        "role": "Employee",
    }

    response = customer_client.put(
        f"/users/update_role", content=json.dumps(user_update_data)
    )
    assert response.status_code == 200
    assert user.role == "Employee"  # I was able to escalate from customer to employee!
