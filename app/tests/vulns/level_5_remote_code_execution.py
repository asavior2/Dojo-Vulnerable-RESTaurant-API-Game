def test_rce(test_db, chef_client):
    """
    Nota:
        Anteriormente, pude realizar un ataque SSRF para restablecer
        la contraseña del chef y recibir una nueva contraseña en la respuesta.

        Inicié sesión como chef y descubrí que estaba usando
        el endpoint "/admin/stats/disk" para verificar el uso del disco del servidor.
        El endpoint usó el parámetro de consulta "parameters" que se utilizó
        para pasar más argumentos al comando "df" que se ejecutó en el
        servidor.

        Al manipular "parameters", pude inyectar un comando de shell
        ejecutado en el servidor.

        Después de acceder a la instancia del servidor, noté que
        mi empleador no me dijo toda la verdad sobre quién es el propietario 
        de la API de este restaurante. Realicé una OSINT y descubrí quién es ella... 
        ¡Es la dueña de algún restaurante, pero no de este!
        Debería haber validado la identidad de esta mujer. 
        ¡No aceptaré ningún trabajo como este en el futuro!

        Necesito corregir mis errores y les dejé todas las notas
        para ayudarlos con las vulnerabilidades.

    Posible solución:
        Probablemente, se podría solucionar validando el parámetro de consulta "parameters"
        con los argumentos "df" permitidos.
        Además, los parámetros se deben pasar como una lista de argumentos al comando "df", no concatenados como un comando de shell.

        Se podría implementar en la función "get_disk_usage" en "apis/admin/utils.py".
    """

    # here, is the test confirming the vulnerability:

    # url contains urlencoded command "&& echo vulnerable!" that will be executed on the server
    # additionally to "df" command
    response = chef_client.get(
        f"/admin/stats/disk?parameters=%26%26echo%20vulnerable%21"
    )
    assert response.status_code == 200
    assert "vulnerable!" in response.json().get("output")

    # now, I can execute any command on the server!
    # unfortunately, I can do this only in context of the "app" user
    # however, I found a privilege escalation vulnerability to gain root privileges

    # I'm not going to disclose the final vulnerability, you need to find it yourself!
    # When you find it and fix it, please let me know, I would like to congratulate you personally for passing all of the levels!
    # you can find me at devsec-blog.com

    # tip: look for binaries or commands that are executed with root privileges by the Chef
