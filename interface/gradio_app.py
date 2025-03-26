

import gradio as gr
from pathlib import Path
import sys
import logging
import pandas as pd
from typing import Dict, List, Tuple

def setup_project_path() -> None:
    try:
        ROOT_PATH = Path(__file__).resolve().parents[1]
        if str(ROOT_PATH) not in sys.path:
            sys.path.insert(0, str(ROOT_PATH))
            logging.info(f"Added project root path: {ROOT_PATH}")
    except Exception as e:
        logging.error(f"Error setting up project path: {e}")
        raise

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

try:
    from codexmind.core.analyzer import RepoAnalyzer
    from codexmind.core.summarizer import CodeSummarizer
    from codexmind.llm.codellama import CodeLlamaLLM
except ImportError as e:
    logging.error(f"Failed to import modules: {e}")
    raise

class CodexMindApp:
    def __init__(self):
        self.llm = CodeLlamaLLM()
        self.summarizer = CodeSummarizer(self.llm)
        self.repo_results: Dict = {}
        self.metrics_df = pd.DataFrame()
        logging.info("CodexMind application initialized")

    def analyze_repo(self, repo_path_str: str) -> Tuple[str, pd.DataFrame]:
        try:
            repo_path = Path(repo_path_str)
            if not repo_path.exists() or not repo_path.is_dir():
                return "❌ Ruta inválida", pd.DataFrame()

            analyzer = RepoAnalyzer(repo_path)
            analyzer.config["max_workers"] = 1
            results = analyzer.analyze_repo()

            self.repo_results = results
            rows = []

            print(f"📂 Archivos detectados: {len(results)}")
            for filename, fa in results.items():
                print(f"  - {filename} | Funciones: {len(fa.functions)} | Clases: {len(fa.classes)}")

                try:
                    resumen = self.summarizer.generate_summary(fa, filename) if fa.functions or fa.classes else "No se pudo generar resumen."
                except Exception as e:
                    logging.error(f"Error al generar resumen para {filename}: {e}")
                    resumen = "❌ Error generando resumen"

                row = {
                    "Archivo": filename,
                    "Líneas totales": fa.total_lines,
                    "Código": fa.code_lines,
                    "Comentarios": fa.comment_lines,
                    "En blanco": fa.blank_lines,
                    "Funciones": len(fa.functions),
                    "Clases": len(fa.classes),
                    "Imports": ", ".join(fa.imports),
                    "Resumen IA": resumen
                }
                rows.append(row)

            self.metrics_df = pd.DataFrame(rows)
            return "✅ Análisis completado", self.metrics_df

        except Exception as e:
            logging.error(f"Error inesperado en analyze_repo: {e}")
            return f"❌ Error: {e}", pd.DataFrame()

    def export_csv(self) -> str:
        try:
            if self.metrics_df.empty:
                return "⚠️ No hay datos para exportar."
            export_path = Path("export_codexmind.csv")
            self.metrics_df.to_csv(export_path, index=False)
            return f"✅ Exportado como {export_path.resolve()}"
        except Exception as e:
            return f"❌ Error al exportar: {e}"

    def create_interface(self):
        with gr.Blocks(title="CodexMind Repo View") as app:
            gr.Markdown("## 📊 CodexMind - Métricas del Repositorio y Resúmenes IA")

            repo_input = gr.Textbox(label="📁 Ruta del repositorio", placeholder="C:/ruta/a/tu/repositorio")
            analizar_btn = gr.Button("🔍 Analizar Repositorio")
            export_btn = gr.Button("📤 Exportar a CSV")
            estado = gr.Markdown()
            tabla = gr.Dataframe(label="📄 Métricas y Resumen por Archivo", interactive=False)
            export_status = gr.Markdown()

            analizar_btn.click(
                fn=self.analyze_repo,
                inputs=repo_input,
                outputs=[estado, tabla]
            )

            export_btn.click(
                fn=self.export_csv,
                inputs=None,
                outputs=export_status
            )

        return app

def main():
    try:
        setup_project_path()
        app_instance = CodexMindApp()
        interface = app_instance.create_interface()
        interface.launch(inbrowser=True)
    except Exception as e:
        logging.error(f"❌ Error al iniciar CodexMindApp: {e}")

if __name__ == "__main__":
    main()
