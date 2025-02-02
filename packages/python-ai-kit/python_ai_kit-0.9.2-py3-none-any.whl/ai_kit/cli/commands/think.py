from ai_kit.cli.registry import registry_instance
from ai_kit.core.router import Router, RouteRegistry, RouteDefinition
from ai_kit.utils import print_stream
from ai_kit.utils.fs import package_root, find_workspace_root
from ai_kit.utils.prompts import process_file_references, load_prompt
from ai_kit.config import CoreConfig
from ai_kit.core.llms.litellm_client import ReasoningClient
from ai_kit.core.llms.deepseek_client import DeepSeekClient
from ai_kit.core.llms.together_client import TogetherClient
from ai_kit.shared_console import shared_console

# Constants
PROJECT_ROOT = find_workspace_root()
PACKAGE_ROOT = package_root()

# we load think from the package root (since its a system prompt)
THINK_PROMPT_PATH = f"{PACKAGE_ROOT}/system_prompts/think.md"
# we load project_rules from the workspace root (since its a user prompt)
PROJECT_RULES_PATH = f"{PROJECT_ROOT}/{CoreConfig.ROOT_DIR}/project_rules.md"


class ThinkHandler:
    def __init__(self, model): # default model is set at the command level
        if model == "r1":
            self.client: DeepSeekClient = DeepSeekClient(model="r1")
        elif model == "r1-together":
            self.client: TogetherClient = TogetherClient(model="r1-together")
        else:
            self.client: ReasoningClient = ReasoningClient(model=model)

        # Initialize router with routes
        self.route_registry = RouteRegistry()
        self._setup_routes()
        self.router = Router(route_registry=self.route_registry, model="gpt-4o")

    def _setup_routes(self):
        """Setup available routes with their conditions."""
        self.route_registry.register(
            RouteDefinition(
                name="thinking_agent",
                description="Advanced reasoning, coding, research, or tasks requiring deep analysis.",
            )
        )

        self.route_registry.register(
            RouteDefinition(
                name="execution_agent",
                description="Basic conversation or simple Q&A that doesn't require external context.",
            )
        )

    async def handle_think(self, prompt: str):
        """Main entry point for the think command processing."""
        # Get routing decision
        decision = self.router.route(prompt)

        # Handle the request based on the route
        if decision.route == "thinking_agent":
            await self._handle_complex_request(prompt)
        else:
            self._handle_simple_request()

    def _build_system_prompt(self) -> str:
        """Construct the system prompt with dynamic content."""
        try:
            base_prompt = load_prompt(THINK_PROMPT_PATH)
        except FileNotFoundError:
            shared_console.print(
                f"[red]Error:[/] Could not find think.md prompt file at {THINK_PROMPT_PATH}"
            )
            shared_console.print(
                "[yellow]Hint:[/] Make sure you have initialized ai-kit with `ai-kit init`"
            )
            raise SystemExit(1)

        try:
            project_rules = load_prompt(PROJECT_RULES_PATH)
        except FileNotFoundError:
            shared_console.print(
                f"[red]Error:[/] Could not find project_rules.md at {PROJECT_RULES_PATH}"
            )
            shared_console.print(
                "[yellow]Hint:[/] Make sure you have initialized ai-kit with `ai-kit init`"
            )
            raise SystemExit(1)

        return base_prompt.format(
            commands=registry_instance.markdown_prompt,
            project_rules=project_rules,
        )

    async def _handle_complex_request(self, prompt: str) -> None:
        """Handle requests requiring deep thinking."""
        processed_prompt = process_file_references(prompt)
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": processed_prompt},
        ]
        with shared_console.status("[bold green]Thinking..."):
            
            # Only pass through thoughts_only if using a thought enabled model
            kwargs = {}
            if self.client.model in ["r1", "r1-together"]:
                kwargs["thoughts_only"] = True
            
            shared_console.print(f"Calling [bold blue]{self.client.model}[/bold blue]...")
            response = await self.client.reasoning_completion(
                messages=messages,
                stream=True,
                **kwargs,
            )
            shared_console.print("\n[bold]Thinking Process:[/bold]")
            await print_stream(response)
        shared_console.print("</thinking>")

    def _handle_simple_request(self):
        """Handle simple requests that don't require deep thinking."""
        shared_console.print(f"<thinking>I should answer the user's request</thinking>")


async def think_command(prompt: str, model: str):
    """CLI entry point for the think command."""
    handler = ThinkHandler(model)
    await handler.handle_think(prompt)