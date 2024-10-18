
![Damn Vulnerable RESTaurant Logo](app/static/img/Ciber.png)

# 🏆 Dojo Api Sec 🏆: ¡Dominando la seguridad de API! 🚀

¡Únete a nuestro Dojo Api Sec para mejorar tus habilidades en seguridad de desarrollo de API! Aprenderás sobre vulnerabilidades y pondrás en práctica la mitigación de las mismas en un juego interactivo que incluye 5 de las principales amenazas de API según el OWASP Top 10. Comenzamos con una introducción a los riesgos y luego te sumergirás en la práctica para fortalecer tus conocimientos y proteger tus proyectos. ¡Únete ahora y mejora tus habilidades en seguridad de API! 👨‍💻🔒💻🎮 #ApiSecurity #OWASP #AprendeHaciendo

An intentionally vulnerable API service designed for learning and training purposes dedicated to developers, ethical hackers and security engineers. The idea of the project is to provide an environment that can be easily extended with new vulnerable endpoints and mechanisms that could be used in trainings for detecting and exploiting identified vulnerabilities.


It's a training playground: 

* **For Developers** - engage in a dedicated game where you will identify and fix vulnerabilities interactively. 
* **For Ethical Hackers** - exploit vulnerabilities manually or use automated tools. Treat it as a CTF challenge, you can start from low privileged API user and escalate to root user. There is one path to achieve this. API docs are provided to facilitate your hacking adventure.
* **For Security Engineers** - utilise various security automation tools such as SAST, DAST, IaC, etc., to test vulnerability detection mechanisms.

## 👨‍💻 Developers Approach

Para los desarrolladores, se creo un juego dedicado donde pueden identificar y corregir vulnerabilidades en aplicaciones basadas en FastAPI de forma interactiva.

1. Install [Docker](https://www.docker.com/get-started/) and [Docker Compose V2](https://docs.docker.com/compose/install/).

2. Inicia el juego ejecutando los siguientes comandos:
```sh
git clone https://github.com/asavior2/Dojo-Vulnerable-RESTaurant-API-Game.git
cd Dojo-Vulnerable-RESTaurant-API-Game
./start_game.sh
```
3. Deberías observar la siguiente pantalla o parecida xD:
![The Game Entry Screen](app/static/img/game-screenshot.png)

4. Puede implementar las correcciones sin necesidad de reiniciar la instancia de Docker. Dado que no se requieren cambios en los modelos, no debería ser necesario reiniciar las migraciones.

En este punto, la aplicación se ejecuta localmente. Puedes consultar el **paso 3** en la siguiente sección para obtener más detalles sobre cómo acceder a la API y la documentación.

## 👾 Ethical Hackers Approach

Puedes abrir un RESTAurante fácilmente con sólo unos pocos pasos, no necesitas tener un gran presupuesto, local alquilado, cocineros o camareras...

Solo necesitas encontrar un Chef y seguir los pasos:

1. Install [Docker](https://www.docker.com/get-started/) and [Docker Compose V2](https://docs.docker.com/compose/install/).

2. Implemente RESTAurant localmente con Docker ejecutando los siguientes comandos:

    ```sh
    git clone https://github.com/asavior2/Dojo-Vulnerable-RESTaurant-API-Game.git
    cd Dojo-Vulnerable-RESTaurant-API-Game
    ./start_app.sh
    ```

3. El servicio API se expondrá en [http://localhost:8001](http://localhost:8001) de forma predeterminada. La documentación de la API se puede encontrar en los siguientes puntos finales:
 * Swagger - [http://localhost:8001/docs](http://localhost:8001/docs)
 * Redoc - [http://localhost:8001/redoc](http://localhost:8001/redoc)

4. Para cerrar el restaurante al final del día de hackeo, simplemente ejecute:
```
./stop_app.sh
```
Los datos persistirán entre paradas y arranques.

¡Ya estás listo para servir los platos ahora, **haz enojar al Chef explotando vulnerabilidades** o **hazlo feliz arreglándolos**!


## ⚠️ Warning and Disclaimer!

¡El Dojo Damn Vulnerable RESTaurant vulnerable es muy vulnerable! No sirvas platos de este RESTAURANTE en la vía pública... ejem... ¡en redes! 

No lo subas a la carpeta html pública de tu proveedor de alojamiento ni a ningún servidor que dé acceso a Internet, ya que se verán comprometidos.

Se recomienda implementar RESTAURANTE localmente con Docker. El uso de la aplicación RESTAURANTE vulnerable, que es intencionalmente insegura por diseño, es bajo tu propio riesgo. No asumimos ninguna responsabilidad por posibles daños, perjuicios o infracciones de seguridad que puedan surgir del uso de RESTAURANTE. Esta aplicación se creó específicamente con fines educativos y de formación en entornos controlados, como aprender sobre vulnerabilidades y practicar técnicas de piratería ética. Es responsabilidad de RESTAURANTE utilizar RESTAURANTE de forma responsable y exclusiva en entornos a los que tengas derecho a acceder y modificar. Al utilizar RESTAURANTE, reconoces que cualquier uso o consecuencia no intencionada es tu responsabilidad exclusiva, y declinamos toda responsabilidad por dichas acciones.

## 🧾 License

Damn Vulnerable RESTaurant se ha desarrollado con orgullo bajo los términos de la Licencia Pública General GNU versión 3.0 (GNU GPL v3.0). Esta licencia fortalece a la comunidad de código abierto al promover los principios de libertad, colaboración y transparencia del software. Con la GNU GPL v3.0, RESTAurant fomenta el aprendizaje, el intercambio y las contribuciones de hackers éticos, ingenieros de seguridad y desarrolladores para mejorar colectivamente sus habilidades y su comprensión de las vulnerabilidades de seguridad. Revise el archivo de LICENCIA para obtener una descripción detallada de los derechos y responsabilidades asociados con el uso y la contribución a este proyecto.
