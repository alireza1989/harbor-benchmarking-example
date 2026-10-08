import random
from pathlib import Path
from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

SOLVE = Path(__file__).resolve().parent.parent / "csv-dedupe" / "solution" / "solve.sh"


class CoinFlipAgent(BaseAgent):
    """Solves the task with probability 0.6, otherwise does nothing."""

    P_SOLVE = 0.6

    @staticmethod
    def name() -> str:
        return "coin-flip"

    def version(self) -> str:
        return "0.1.0"

    async def setup(self, environment: BaseEnvironment) -> None:
        pass

    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        if random.random() < self.P_SOLVE:
            script = SOLVE.read_text()
            await environment.exec(command=f"bash <<'EOF'\n{script}\nEOF")
