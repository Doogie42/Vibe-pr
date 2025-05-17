from models import PromptResponse
from rich.console import Console

from rich.panel import Panel
from rich.text import Text
from emoji import emojize


def get_color_issue(confidence):
    color_scheme_to_gravity = {
        0: "blue",
        1: "green",
        2: "yellow",
        3: "dark_orange",
        4: "red",
    }
    scale = max(0.0, min(confidence, 1.0))
    index = min(int(scale * 5), 4)
    return color_scheme_to_gravity[index]


def pretty_print_gpt(data: PromptResponse):
    console = Console()
    panel_content = Text(emojize(f"{data.suggested_title}\n\n"), style="bold green")
    panel_content.append(Text(emojize(f"{data.summary}\n\n"), style="blue"))
    panel_content.append(Text(emojize(f"Issues:\n\n"), style="bold"))

    for issue in data.issues:
        color = get_color_issue(issue.confidence)
        panel_content.append(
            Text(
                emojize(f"•[{issue.confidence}] {issue.description}\n\n"),
                style=color,
                justify="left",
            )
        )
    panel = Panel(panel_content, title="vibe pr", expand=False, title_align="center")

    console.print(panel, justify="center")
