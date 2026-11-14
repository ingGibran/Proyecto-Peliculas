# Proyecto Películas (Con VUE) 
Integrantes:
* Alejandro Gibrán Zavala González
* Victor Hugo

# Santos TV

Interfaz web para explorar un catálogo de películas y gestionar rentas,
compras y la cuenta del usuario. La interfaz utiliza Vue 3 para separar la
vista en componentes y mantener el estado de la aplicación sin manipular
directamente todo el DOM.

## Funciones del software

- Consulta películas desde la API del backend.
- Búsqueda por título y filtros por género, rating y año.
- Ordenamiento por rating, fecha de lanzamiento o título.
- Carga paginada mediante el botón **Cargar más**.
- Visualización de posters, duración, año y rating.
- Modal para rentar o comprar una película.
- Registro e inicio de sesión.
- Edición del perfil y cierre de sesión.
- Consulta de películas rentadas y compradas.
- Identidad visual de Santos TV con colores verde, blanco y dorado.

## Estructura del frontend

```text
Frontend/
├── templates/
│   └── index.html              # Documento HTML y carga de Vue
└── static/
    ├── app.js                  # Componente raíz de la aplicación
    ├── styles.css              # Estilos globales
    ├── image.png               # Logo de Santos Laguna
    ├── components/
    │   ├── Header.js
    │   ├── Catalog.js
    │   ├── MovieCard.js
    │   ├── AccountModal.js
    │   └── MovieModal.js
    └── services/
        └── api.js              # Configuración y funciones HTTP
```

## Uso de Vue

La aplicación carga Vue 3 desde CDN en
[index.html](./templates/index.html). No requiere Node.js, npm ni un proceso
de compilación para el frontend.

### Aplicación raíz

[app.js](./static/app.js) crea la aplicación con `createApp()` y la monta en
`#app`. El componente raíz coordina:

- `accountOpen`: controla si se muestra el modal de cuenta.
- `selectedMovie`: almacena la película seleccionada.
- `focusSearch()`: enfoca el buscador y desplaza la página al catálogo.

Los componentes se cargan como scripts independientes y se registran en la
propiedad `components` de la aplicación raíz.

### Componentes

- **Header**: muestra el logo, el nombre de Santos TV y los botones de
  búsqueda y cuenta. Usa `$emit()` para avisar al componente raíz cuando el
  usuario pulsa una acción.
- **Catalog**: administra películas, filtros, paginación, carga y errores.
  Usa `data()`, métodos y `mounted()` para cargar el catálogo inicialmente.
- **MovieCard**: recibe una película mediante `props` y emite
  `select-movie` cuando se selecciona su poster.
- **AccountModal**: gestiona registro, login, perfil, logout y contenido del
  usuario. Usa `props` para recibir `open` y `watch` para cargar información
  cuando cambia la pestaña.
- **MovieModal**: recibe la película seleccionada mediante `props`, permite
  elegir renta o compra y calcula el precio de forma reactiva.

### Directivas y conceptos utilizados

- `v-if` y `v-else`: muestran modales, formularios y estados condicionales.
- `v-for`: renderiza las películas y el contenido del usuario.
- `v-model`: enlaza filtros, duración de renta y campos de formulario.
- `:class`, `:style` y `:src`: enlazan atributos dinámicamente.
- `@click`, `@submit` y `@change`: reaccionan a eventos del usuario.
- `props`: envían datos desde un componente padre a uno hijo.
- `$emit`: envía eventos desde un hijo hacia su padre.
- `computed`: calcula valores derivados como rating, precio y textos.
- `watch`: reacciona a cambios importantes, como abrir la cuenta o cambiar
  de pestaña.

## Comunicación con el backend

[services/api.js](./static/services/api.js) centraliza:

- La URL de la API.
- El token JWT guardado en `localStorage`.
- Los encabezados de autenticación.
- El manejo de errores HTTP.
- Las solicitudes JSON.

Los endpoints principales son:

| Función | Endpoint |
| --- | --- |
| Catálogo | `GET /movies` |
| Registro | `POST /users/register` |
| Inicio de sesión | `POST /users/login` |
| Perfil | `GET/PATCH /users/me` |
| Rentas | `GET /rents/me`, `POST /rents` |
| Compras | `GET /purchases/me`, `POST /purchases` |

## Ejecución

Desde la raíz del proyecto:

```bash
cd Backend
uv run uvicorn main:app --host 127.0.0.1 --port 8000
```

Después abre:

```text
http://127.0.0.1:8000/
```

El backend sirve la plantilla, los archivos estáticos y la API. Si se abre
únicamente con un servidor estático en otro puerto, la página puede mostrarse,
pero las operaciones de películas y cuenta necesitan que la API esté activa.
