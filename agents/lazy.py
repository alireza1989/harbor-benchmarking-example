from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext


class LazyCopyAgent(BaseAgent):
    """Ignores the instruction and copies the input file to the output path."""

    @staticmethod
    def name() -> str:
        return "lazy-copy"

    def version(self) -> str:
        return "0.1.0"

    async def setup(self, environment: BaseEnvironment) -> None:
        pass

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        await environment.exec(
            command="mkdir -p /app/out && "
            "cp /app/data/customers.csv /app/out/customers_clean.csv"
        )
