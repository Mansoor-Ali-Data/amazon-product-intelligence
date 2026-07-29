"""
Entry point for the Ground Truth Builder.

Allows the user to build candidate products for one benchmark query
or for the entire benchmark dataset.
"""

from __future__ import annotations

from src.evaluation.ground_truth.builder import GroundTruthBuilder
from src.evaluation.ground_truth.formatter import GroundTruthFormatter
from src.evaluation.ground_truth.queries import GROUND_TRUTH_QUERIES
from src.evaluation.ground_truth.writer import (
    GroundTruthWriter,
)




def _print_menu() -> None:
    """
    Display the benchmark query menu.
    """

    print()
    print("=" * 100)
    print("Ground Truth Builder")
    print("=" * 100)
    print()

    print("Available Benchmark Queries")
    print("-" * 100)

    for index, example in enumerate(
        GROUND_TRUTH_QUERIES,
        start=1,
    ):
        print(
            f"{index:>2}. {example.id}"
        )
        print(
            f"    Category : {example.category.value}"
        )
        print(
            f"    Query    : {example.query}"
        )
        print(
            f"    Purpose  : {example.description}"
        )
        print()

    print("-" * 100)
    print(" A. Build ALL benchmark queries")
    print(" Q. Quit")
    print("=" * 100)
    print()


def _build_one(
    builder: GroundTruthBuilder,
    formatter: GroundTruthFormatter,
    writer: GroundTruthWriter,
    index: int,
) -> None:

    example = GROUND_TRUTH_QUERIES[index]

    candidates = builder.build(example)

    report = formatter.format(
        example,
        candidates,
    )

    template = formatter.format_benchmark_template(
        example,
        candidates,
    )

    writer.write_report(
        example.id,
        report,
    )

    writer.write_template(
        example.id,
        template,
    )

    print(
        f"✓ Generated {example.id}"
    )


def _build_all(
    builder: GroundTruthBuilder,
    formatter: GroundTruthFormatter,
    writer: GroundTruthWriter,
) -> None:
    """
    Build candidate products for every benchmark query.
    """

    total = len(GROUND_TRUTH_QUERIES)

    for index, example in enumerate(
        GROUND_TRUTH_QUERIES,
        start=1,
    ):

        print()
        print(
            f"[{index}/{total}] "
            f"Building '{example.id}'..."
        )

        candidates = builder.build(
            example,
        )

        report = formatter.format(
            example,
            candidates,
        )

        writer.write_report(
            example.id,
            report,
        )


        print(
            f"✓ Generated {example.id}"
        )


def main() -> None:
    """
    Run the interactive Ground Truth Builder.
    """
    writer = GroundTruthWriter()

    builder = GroundTruthBuilder()

    formatter = GroundTruthFormatter()

    while True:

        _print_menu()

        choice = input(
            "Select query (number/A/Q): "
        ).strip().lower()

        if choice == "q":
            print("\nGoodbye!")
            break

        if choice == "a":
            _build_all(
                builder,
                formatter,
                writer,
            )
            continue

        if not choice.isdigit():

            print(
                "\nInvalid selection."
            )

            continue

        index = int(choice) - 1

        if index < 0 or index >= len(
            GROUND_TRUTH_QUERIES,
        ):

            print(
                "\nInvalid query number."
            )

            continue

        _build_one(
            builder,
            formatter,
            index,
        )


if __name__ == "__main__":
    main()