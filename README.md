# femboyFoxBot - Bot de Telegram para Novelas Visuales Traducidas

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22.3-brightgreen.svg)
![pywebview](https://img.shields.io/badge/pywebview-5.4.2-orange.svg)

Bot de Telegram que lista y muestra información sobre novelas visuales traducidas al español por [@VulpVenandi25](https://t.me/VulpVenandi25), con panel de control gráfico incluido.

## Características

### Bot de Telegram

- 📚 Listado paginado de novelas visuales traducidas
- 🔍 Detalles completos desde la API de itch.io (título, autor, descripción, precio, portada)
- 🔗 Enlaces directos a páginas oficiales y descarga por Terabox
- 🖼️ Muestra la imagen de portada cuando está disponible
- 🔄 Navegación intuitiva con botones inline (páginas, volver atrás)

### Panel de Control (GUI)

- 🖥️ Ventana nativa con **pywebview** (WebView2 en Windows, WebKit en Linux/macOS)
- 🟢 Estado en tiempo real del bot (conectado / detenido)
- ⏱️ Uptime y última interacción
- 📋 Registro de eventos recientes con scroll automático
- 🔌 Actualización automática cada 1.5 segundos vía JS → Python bridge

## Comandos del Bot

| Comando   | Descripción                            |
| --------- | -------------------------------------- |
| `/start`  | Mensaje de bienvenida e información    |
| `/help`   | Muestra los comandos disponibles       |
| `/novels` | Muestra la lista de novelas traducidas |

## Requisitos

- Python 3.8+
- Cuenta de Telegram con un bot creado ([@BotFather](https://t.me/BotFather))
- Cuenta en itch.io (opcional, para obtener token de API)
- Windows: WebView2 Runtime (viene incluido en Windows 11 / actualizaciones de Windows 10)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/VulpxVenandi25/FemboyFoxBot.git
   cd FemboyFoxBot
   ```

2. Crea y activa un entorno virtual (recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz del proyecto:

   ```
   TELEGRAM_TOKEN="tu_token_de_telegram"
   ITCH_TOKEN="tu_token_de_itch_io"
   ```

   > `ITCH_TOKEN` es opcional si solo quieres el listado; sin él fallará la carga de detalles desde itch.io.

5. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

   Se abrirá la ventana del panel de control y el bot comenzará a funcionar en segundo plano.

## Estructura del Proyecto

```
FemboyFoxBot/
├── main.py                 # Punto de entrada: inicia bot + GUI en hilos
├── src/                    # Código fuente Python
│   ├── __init__.py
│   ├── config.py           # Variables de entorno y constantes
│   ├── novels.py           # Carga de novels.json y API de itch.io
│   ├── keyboards.py        # Constructores de teclados inline
│   ├── handlers.py         # Handlers de comandos y callbacks
│   ├── bot.py              # Clase BotApp (setup, run, stop, cola de eventos)
│   └── ui.py               # Ventana pywebview (carga gui/ y expone API)
├── gui/                    # Interfaz gráfica (frontend)
│   ├── index.html          # Estructura HTML
│   ├── styles.css          # Estilos dark theme
│   └── scripts.js          # Lógica JS: polling y actualización DOM
├── json/
│   └── novels.json         # Base de datos de novelas (gameid, nombre, link)
├── .env                    # Tokens de Telegram e itch.io
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

## Arquitectura

### Flujo de datos

```
Usuario Telegram
      │
      ▼
handlers.py  ──►  novels.py  ──►  itch.io API
      │                │
      ▼                ▼
keyboards.py     json/novels.json
      │
      ▼
  BotApp (bot.py) ──► UI (ui.py) ──► gui/index.html
      │                                    │
      ▼                                    ▼
  Cola de eventos                  pywebview bridge (JS ↔ Python)
```

### Hilos

- **Hilo principal**: pywebview (ventana GUI)
- **Hilo secundario** (daemon): `application.run_polling()` del bot de Telegram

Al cerrar la ventana, el hilo del bot se detiene automáticamente.

### API del BotApp (expuesta a la GUI)

| Método        | Retorno                                                |
| ------------- | ------------------------------------------------------ |
| `get_info()`  | `{ running, uptime, last_interaction, events: [...] }` |
| `add_event()` | Agrega un evento a la cola (máx. 100)                  |

## Personalización

Puedes modificar estos valores en `src/config.py`:

| Constante        | Valor por defecto | Descripción                              |
| ---------------- | ----------------- | ---------------------------------------- |
| `ITEMS_PER_PAGE` | `10`              | Novelas mostradas por página en Telegram |

Para agregar o quitar novelas, edita `json/novels.json`:

```json
{
  "gameid": "123456",
  "name": "Nombre de la Novela",
  "link": "https://autor.itch.io/novela"
}
```

## Dependencias

| Paquete               | Versión | Uso                                 |
| --------------------- | ------- | ----------------------------------- |
| `python-telegram-bot` | ≥22.0   | Interacción con la API de Telegram  |
| `python-dotenv`       | ≥1.0    | Carga de variables de entorno       |
| `requests`            | ≥2.30   | Peticiones HTTP a la API de itch.io |
| `pywebview`           | ≥5.0    | Ventana nativa con HTML/JS/CSS      |

## Licencia

MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

Creado con ❤️ por [@VulpVenandi25](https://t.me/VulpVenandi25) | [Linktree](https://linktr.ee/vulpxvenandi25)
