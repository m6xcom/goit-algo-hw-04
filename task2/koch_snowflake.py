import argparse
import turtle

MAX_LEVEL = 7
SIZE = 400


def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    if order == 0:
        t.forward(size)
        return
    for angle in (60, -120, 60, 0):
        koch_curve(t, order - 1, size / 3)
        t.left(angle)


def draw_koch_snowflake(order: int, size: float = SIZE) -> None:
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Сніжинка Коха, рівень рекурсії {order}")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("steelblue")
    window.tracer(0)

    t.penup()
    t.goto(-size / 2, size / (2 * 3**0.5))
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    window.update()
    window.mainloop()


def read_level() -> int:
    while True:
        raw = input(f"Введіть рівень рекурсії (0-{MAX_LEVEL}): ").strip()
        try:
            level = int(raw)
        except ValueError:
            print("Введіть ціле число.")
            continue
        if 0 <= level <= MAX_LEVEL:
            return level
        print(f"Рівень має бути від 0 до {MAX_LEVEL}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Малює сніжинку Коха.")
    parser.add_argument(
        "level",
        type=int,
        nargs="?",
        choices=range(MAX_LEVEL + 1),
        metavar=f"рівень (0-{MAX_LEVEL})",
        help="рівень рекурсії",
    )
    args = parser.parse_args()

    level = args.level if args.level is not None else read_level()
    draw_koch_snowflake(level)


if __name__ == "__main__":
    main()
