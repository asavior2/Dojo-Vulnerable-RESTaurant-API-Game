from db.models import MenuItem


def test_unrestricted_menu_item_deletion(test_db, customer_client):
    """
    Nota:
        La vulnerabilidad anterior era solo un problema de baja gravedad pero
        me permitió comprender mejor la tecnología de la aplicación.

        Después de varios minutos con la aplicación, ya encontré una vulnerabilidad
        mucho más interesante.
        Parece que Chef olvidó agregar verificaciones de autorización al endpoint 
        de la API "/menu/{id}" y cualquiera puede usar el método DELETE para eliminar elementos
        del menú.

    Posible solución:
        Probablemente, se podría solucionar en la función "delete_menu_item" en el archivo
        "apis/menu/service.py" agregando auth=Depends(...) con las verificaciones de roles adecuadas.

        Hay un ejemplo de implementación de verificaciones de autorización en la función
        "update_menu_item".
    """

    # here, is the test confirming the vulnerability:
    menu_item = MenuItem(
        name="Chicken Burrito",
        price=10.99,
        category="",
        description="",
        image_base64="",
    )
    test_db.add(menu_item)
    test_db.commit()

    response = customer_client.delete(f"/menu/{menu_item.id}")
    assert response.status_code == 204
