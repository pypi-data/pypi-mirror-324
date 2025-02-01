import logging
from vm_pkg_tools.utils.parser_utils import (
    is_valid_action_line,
    parse_action_line,
    extract_timestamp,
)


def extract_rally_winner(line: str) -> str | None:
    """
    Determine the rally winner from the line.
    """
    return (
        "home" if line.startswith("*p") else "away" if line.startswith("ap") else None
    )


def extract_point_identifier(line: str) -> str | None:
    """
    Extract the point identifier from the line.
    """
    return line.split(";", 1)[0].strip()


def extract_actions(
    content: str, point_idx: int, next_point: str | None = None
) -> list[dict]:
    """
    Extract actions between points.
    """
    lines = content.splitlines()
    actions = []

    # Find the last action index for this rally
    last_action_of_rally_idx = point_idx - 1
    if next_point:
        try:
            next_point_idx = lines.index(next_point)
            last_action_of_rally_idx = min(last_action_of_rally_idx, next_point_idx - 1)
        except ValueError:
            logging.warning(f"Next point {next_point} not found. Using default range.")

    if last_action_of_rally_idx < 0 or last_action_of_rally_idx >= len(lines):
        logging.error(
            f"last_action_of_rally_idx out of bounds: {last_action_of_rally_idx}"
        )
        return []

    logging.info(
        f"Last action of rally index: {last_action_of_rally_idx}, Line: {lines[last_action_of_rally_idx]}"
    )

    # Backtrack to find the first action of the rally
    first_action_of_rally_idx = last_action_of_rally_idx
    while first_action_of_rally_idx > 0 and is_valid_action_line(
        lines[first_action_of_rally_idx]
    ):
        first_action_of_rally_idx -= 1

    # Start collecting actions
    for i in range(first_action_of_rally_idx + 1, last_action_of_rally_idx + 1):
        parsed_action = parse_action_line(lines[i].strip())
        if parsed_action:
            actions.append(parsed_action)

    logging.debug(f"Extracted actions: {actions}")
    return actions


def parse_point(
    line: str, content: str, point_idx: int, next_point: str | None = None
) -> dict | None:
    """
    Parse a point line and associated actions into a structured dictionary.
    """
    try:
        parts = line.split(";")
        if len(parts) < 2:
            logging.warning(f"Point line is too short: {line}")
            return None

        # Extract point-level information
        point = extract_point_identifier(line)
        rally_winner = extract_rally_winner(line)
        timestamp = extract_timestamp(parts)

        # Extract associated actions
        actions = extract_actions(content, point_idx, next_point)

        if not point or not timestamp:
            logging.warning(f"Point or timestamp missing for line: {line}")
            return None

        return {
            "point": point,
            "rally_winner": rally_winner,
            "timestamp": timestamp,
            "actions": actions,
        }
    except Exception as e:
        logging.error(f"Error parsing point line: {line} - {e}")
        return None
