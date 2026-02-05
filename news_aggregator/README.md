# News Multi-Scraper (news_aggregator)

Este proyecto es un agregador de noticias desarrollado con Scrapy que extrae, limpia y unifica datos de tres fuentes españolas: **ABC**, **El País** y **La Voz de Galicia**.

## 🛠️ Detalles Técnicos
El proyecto utiliza diferentes estrategias de extracción según los requisitos del ejercicio:

- **ABC (`abc.py`)**: Implementado exclusivamente con selectores **CSS**.
- **El País (`elpais.py`)**: Implementado exclusivamente con selectores **XPath**.
- **La Voz de Galicia (`lvdg.py`)**: Utiliza una combinación de selectores y una lógica especial de filtrado para descartar artículos sin contenido (spam).

## 📊 Estructura de Datos
Cada noticia extraída se normaliza mediante un `Pipeline` y contiene los siguientes campos:
- `position`: Orden de aparición en la portada.
- `title`: Título de la noticia (limpio de espacios y caracteres especiales).
- `date`: Fecha normalizada al formato `YYYY-MM-DD HH:MM`.
- `author`: Nombre del autor o autores.
- `source`: Nombre del periódico de origen.
- `url`: Enlace directo a la noticia (usado para depuración y control de calidad).

## ✨ Procesamiento y Limpieza

1. **Normaliza Fechas:** Traduce meses del español al inglés y maneja formatos ISO y UTC automáticamente usando `dateutil`.
2. **Limpieza de Texto:** Elimina saltos de línea, espacios extra y caracteres como `\xa0`.
3. **Validación:** En `lvdg.py`, se descartan automáticamente las entradas que no tienen título, autor ni fecha para asegurar la calidad del archivo final.

## 🚀 Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install scrapy python-dateutil

2. **Ejecutar todos los spiders:**
   ```bash
   python run_all.py

## 📁 Archivos del Proyecto

### `spiders/`
Contiene los scripts de extracción específicos para cada diario:

- **`abc.py`**: Extracción mediante **CSS**.
- **`elpais.py`**: Extracción mediante **XPath**.
- **`lvdg.py`**: Extracción mixta con lógica de filtrado de noticias vacías.

### `items.py`
Define el objeto **`NewsAggregatorItem`** con los campos:
- `position`
- `title`
- `date`
- `author`
- `source`
- `url`

### `pipelines.py`
Gestiona:
- La normalización de fechas (traducción de meses y formato ISO).
- La limpieza final de los datos.

### `run_all.py`
Script de conveniencia que utiliza **`CrawlerProcess`** para lanzar los tres spiders simultáneamente y generar el archivo unificado.

### `all_news.json`
Resultado final que contiene todos los datos agregados en formato **JSON**.


