import uuid
from typing import Any, Dict
from sqlmodel import Session
from database.models import ArtifactModel, WorkflowExecutionModel
from workflows.base import BaseWorkflow


class MarketAnalyzerWorkflow(BaseWorkflow):

    @property
    def name(self) -> str:
        return "market_analyzer_workflow"

    def run(self, input_data: Dict[str, Any], session: Session) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())

        # 1. Registrar el inicio de la ejecución en la BD (Estado: PENDING -> RUNNING)
        execution_record = WorkflowExecutionModel(
            execution_id=execution_id,
            workflow_name=self.name,
            status="RUNNING",
            input_payload=str(input_data),
        )
        session.add(execution_record)
        session.commit()

        try:
            # 2. Paso del Agente de Investigación (Simulado por ahora)
            topic = input_data.get("topic", "Global Tech Trends")
            research_data = (
                f"Datos de investigación recopilados para el sector: {topic}."
            )

            # 3. Paso del Agente Estratega (Toma de decisiones y síntesis)
            strategy_output = (
                f"Análisis estratégico y plan de acción basado en: {research_data}"
            )

            # 4. Guardar el resultado final como un Artefacto en la BD
            artifact = ArtifactModel(
                artifact_id=str(uuid.uuid4()),
                execution_id=execution_id,
                title=f"Reporte Estratégico - {topic}",
                content=strategy_output,
            )
            session.add(artifact)

            # 5. Actualizar estado de ejecución a SUCCESS
            execution_record.status = "SUCCESS"
            execution_record.output_payload = str(
                {"artifact_id": artifact.artifact_id, "summary": strategy_output}
            )
            session.add(execution_record)
            session.commit()

            return {
                "status": "success",
                "execution_id": execution_id,
                "artifact_id": artifact.artifact_id,
                "result": strategy_output,
            }

        except Exception as e:
            # Manejo de errores y persistencia del fallo
            execution_record.status = "FAILED"
            execution_record.output_payload = str({"error": str(e)})
            session.add(execution_record)
            session.commit()
            raise e
