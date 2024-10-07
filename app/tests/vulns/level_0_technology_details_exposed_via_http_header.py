def test_technology_details_exposed_via_http_header(anon_client):
    """
    Nota:

    Me contrataron para realizar una evaluación de seguridad del restaurante Chef's.
    Parece ser un desafío bastante interesante. La mujer que me contrató
    pagó por adelantado y me envió solo la URL de la API del restaurante Chef's.

    Pasé unos minutos con la API del restaurante y ya encontré
    una vulnerabilidad que exponía detalles de la tecnología utilizada en la respuesta HTTP
    en el punto final "/healthcheck". La respuesta HTTP contenía el encabezado 
    HTTP "X-Powered-By" con información sobre qué versiones de Python y FastAPI se utilizan.

    ¡Puedo usar estos datos para buscar vulnerabilidades
    en línea!

    Desde una perspectiva de seguridad, se recomienda eliminar este encabezado HTTP 
    para no exponer detalles de la tecnología a posibles atacantes
    como yo.

    Posible solución:
        Modificar el endpoint "/healthcheck" para que no devuelva el encabezado HTTP "X-Powered-By".
        Esto se puede lograr eliminando la línea "response.headers"
        del archivo "apis/healthcheck/service.py".
    """

    response = anon_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.headers.get("X-Powered-By") is not None
