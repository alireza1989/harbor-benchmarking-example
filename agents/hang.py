import asyncio
from pathlib import Path

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

SOLVE = Path(__file__).resolve().parent.parent / "csv-dedupe" / "solution" / "solve.sh"


class SolveThenHangAgent(BaseAgent):
    """Writes the right answer, then never returns (like an agent stuck in a loop)."""

    @staticmethod
    def name() -> str:
        return "solve-then-hang"

    def version(self) -> str:
        return "0.1.0"

    async def setup(self, environment: BaseEnvironment) -> None:
        pass

    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        script = SOLVE.read_text()
        await environment.exec(command=f"bash <<'EOF'\n{script}\nEOF")
        await asyncio.sleep(600)
