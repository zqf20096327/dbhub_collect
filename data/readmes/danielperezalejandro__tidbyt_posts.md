# tidbyt_posts
## Introducción
Esta aplicación muestra posts publicados por usuarios en el proyecto de fin de ciclo que estoy realizando, recibiendo la información a traves de la api del proyecto.

## Estructura
Tiene las siguientes funciones principalmente:
- **main(config):** Función principal que procesa la entrada del usuario y renderiza la interfaz de usuario.
- **obtnerFormatoFecha(fecha):** Obtiene la fecha del post en formato adecuado.
- **render_article(posts):** Realiza un array con todos los posts de un usuario en concreto para poder mostrarse de manera estética y ordenada.
- **render_inicio(posts):** Realiza un array con todos los posts del inicio de usuario en concreto para poder mostrarse de manera estética y ordenada.

## Flujo de Trabajo 
Entrada del Usuario:
El usuario introduce su nombre de usuario o el nombre de usuario del que quiere ver los posts.

Obtención de Datos:
La aplicación obtiene la información de la api en base a lo solicitado por el usuario.
  
Renderización de la Interfaz de Usuario:
La aplicación procesa los datos y los hace visibles.

## Instalación
Para la instalación y uso de la aplicación, debes descargar este repositorio. Una vez descargado, deberás acceder desde la consola al directorio donde estén los archivos y ejecutar el comando pixlet serve nombre_del_archivo.star. Con esto realizado, la consola te devolverá la URL en la que se está ejecutando la aplicación. Si ingresas en ella, podrás usarla y verla funcionar.

## Uso
El usuario en caso de querer ver su pantalla de inicio debe introducir su nombre de usuario en el input de "Inicio", de esta manera verá todos los posts de las personas a las que sigue. En caso de querer ver los post de un usuario en concreto deberá escribir el nombre de este usuario en el input de "Usuario".

## Autor
danielperezalejandro
