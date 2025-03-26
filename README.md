# CortexMind

CodexMind es una plataforma modular e inteligente que analiza código fuente, genera documentación técnica, responde preguntas y evalúa la calidad del código utilizando modelos de lenguaje (LLM) open-source como DeepSeek Coder o CodeLlama.

## Características principales

- Análisis automático de repositorios en Python.
- Resúmenes inteligentes y explicaciones con IA local.
- Métricas de calidad de código: complejidad, líneas, documentación, etc.
- Visualización de dependencias en forma de grafo.
- Generación de documentación técnica por archivo, clase y función.
- Interfaz conversacional para hacer preguntas sobre el código.

## Arquitectura modular
codexmind/ 
├── config/ # Configuraciones globales 
├── llm/ # Motor de lenguaje (DeepSeek, CodeLlama, etc.) 
├── core/ # Análisis de código con AST y métricas 
├── interface/ # Interfaz en Gradio (antes Streamlit) 
├── utils/ # Funciones auxiliares 
├── tests/ # Pruebas unitarias 
├── ci/ # CI/CD (GitHub Actions) 
├── assets/ # Archivos estáticos 
└── README.md

## Tecnologías

- Python 3.10 o superior
- ast, concurrent.futures, asyncio
- Gradio
- llama-cpp-python (para usar LLMs locales)
- NetworkX y pyvis (para grafos de dependencias)

## Estado

Proyecto en desarrollo activo (MVP funcional). Preparado para expandirse con soporte multi-lenguaje y despliegue web.

## Licencia

Este proyecto está licenciado bajo la MIT License.