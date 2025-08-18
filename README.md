# femboyFoxBot - Bot de Telegram para Novelas Visuales Traducidas

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-20.0-brightgreen.svg)

Un bot de Telegram que muestra información sobre novelas visuales traducidas al español por @VulpVenandi25.

## Características principales

- 📚 Listado paginado de novelas visuales traducidas
- 🔍 Detalles completos de cada novela (título, descripción, autor, plataformas, etc.)
- 🔗 Enlaces directos a las páginas oficiales y opciones de descarga
- 🖼️ Muestra la imagen de portada de cada novela cuando está disponible
- 🔄 Navegación intuitiva entre páginas y detalles

## Comandos disponibles

| Comando   | Descripción                            |
| --------- | -------------------------------------- |
| `/start`  | Mensaje de bienvenida e información    |
| `/help`   | Muestra los comandos disponibles       |
| `/novels` | Muestra la lista de novelas traducidas |

## Requisitos

- Python 3.8+
- Cuenta de Telegram con un bot creado (obtén tu token de @BotFather)
- Cuenta en itch.io (opcional, para obtener el token de API)

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

4. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

   ```
   TELEGRAM_TOKEN=tu_token_de_telegram
   ITCH_TOKEN=tu_token_de_itch_io (opcional)
   ```

5. Ejecuta el bot:
   ```bash
   python main.py
   ```

## Estructura del proyecto

```
FemboyFoxBot/
├── main.py               # Código principal del bot
├── .env                  # Archivo de configuración (crearlo)
├── README.md             # Este archivo
└── requirements.txt      # Dependencias del proyecto
```

## Dependencias

- `python-telegram-bot` - Para la interacción con la API de Telegram
- `python-dotenv` - Para manejar variables de entorno
- `requests` - Para hacer peticiones HTTP a la API de itch.io

## Configuración avanzada

Puedes modificar los siguientes parámetros en el código:

- `ITEMS_PER_PAGE`: Número de novelas a mostrar por página (por defecto: 10)
- URL de la API: Actualmente configurada para `https://backend-vv25.vercel.app/api/novels`

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerir mejoras.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

Creado con ❤️ por [@VulpVenandi25](https://t.me/VulpVenandi25) | [Linktree](https://linktr.ee/vulpxvenandi25)
