from pathlib import Path
import yaml
import subprocess

from compiler.builders.ir_builder import build_ir
from compiler.sql.builders.sql_ir_builder import build_sql_ir_from_semantic
from compiler.sql.passes.pipeline import SqlCompilerPipeline
from compiler.sql.passes.normalize_fact_query import NormalizeFactQueryPass
from compiler.sql.passes.bind_measure_aggregation import BindMeasureAggregationPass
from compiler.sql.passes.bind_dimension_joins import BindDimensionJoinsPass
from compiler.sql.renderers.fact_renderer import FactQueryRenderer


SEMANTIC_MODEL_PATH = Path("semantic/model.contract.yml")
OUTPUT_SQL_DIR = Path("output/sql")


def compile_sql() -> None:
    """
    Orchestrates full SQL compilation from semantic model to SQL artifacts.
    """

    # --- Validate semantic model ---
    result = subprocess.run(
        ["python3", "validation/engine.py"],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError("Semantic model validation failed")

    # --- Load semantic model ---
    with SEMANTIC_MODEL_PATH.open() as f:
        semantic_model_dict = yaml.safe_load(f)

    # --- Build Semantic IR ---
    semantic_ir = build_ir(semantic_model_dict)

    # --- Build SQL IR ---
    sql_queries = build_sql_ir_from_semantic(semantic_ir)

    # --- SQL compiler pipeline ---
    pipeline = SqlCompilerPipeline(
        passes=[
            NormalizeFactQueryPass(),
            BindMeasureAggregationPass(),
            BindDimensionJoinsPass(semantic_ir),
        ]
    )

    # --- Render & write SQL ---
    OUTPUT_SQL_DIR.mkdir(parents=True, exist_ok=True)

    for query in sql_queries:
        compiled_query = pipeline.run(query)
        renderer = FactQueryRenderer(compiled_query)
        sql = renderer.render()

        output_path = OUTPUT_SQL_DIR / f"{compiled_query.from_table}.sql"
        output_path.write_text(sql)


if __name__ == "__main__":
    compile_sql()