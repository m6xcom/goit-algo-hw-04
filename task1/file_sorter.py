import argparse
import shutil
import sys
from pathlib import Path

NO_EXTENSION_DIR = "no_extension"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та сортує їх за розширенням."
    )
    parser.add_argument("source", type=Path, help="шлях до вихідної директорії")
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="шлях до директорії призначення (за замовчуванням: dist)",
    )
    return parser.parse_args()


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def copy_file(file_path: Path, destination: Path) -> None:
    extension = file_path.suffix[1:].lower() or NO_EXTENSION_DIR
    target_dir = destination / extension
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = unique_path(target_dir / file_path.name)
        shutil.copy2(file_path, target)
        print(f"Скопійовано: {file_path} -> {target}")
    except PermissionError:
        print(f"Немає доступу, файл пропущено: {file_path}", file=sys.stderr)
    except OSError as error:
        print(f"Не вдалося скопіювати {file_path}: {error}", file=sys.stderr)


def process_directory(source: Path, destination: Path) -> None:
    try:
        items = list(source.iterdir())
    except PermissionError:
        print(f"Немає доступу, директорію пропущено: {source}", file=sys.stderr)
        return
    except OSError as error:
        print(f"Не вдалося прочитати директорію {source}: {error}", file=sys.stderr)
        return

    for item in items:
        if item.resolve() == destination.resolve():
            continue
        if item.is_dir():
            process_directory(item, destination)
        elif item.is_file():
            copy_file(item, destination)


def main() -> None:
    args = parse_args()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists():
        sys.exit(f"Вихідна директорія не існує: {source}")
    if not source.is_dir():
        sys.exit(f"Вихідний шлях не є директорією: {source}")

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        sys.exit(f"Не вдалося створити директорію призначення {destination}: {error}")

    process_directory(source, destination)
    print(f"\nГотово. Файли розсортовано в: {destination.resolve()}")


if __name__ == "__main__":
    main()
