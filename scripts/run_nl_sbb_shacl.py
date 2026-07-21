#!/usr/bin/env python3
"""Run official NL-SBB SHACL validation (skos-ap-nl) on an RDF/Turtle file."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from pyshacl import validate
from rdflib import RDF
from rdflib.namespace import SH

DEFAULT_SHAPES = Path(__file__).resolve().parent.parent / "profiles" / "skos-ap-nl.ttl"
SHAPES_URL = "https://raw.githubusercontent.com/geonovum/NL-SBB/main/profiles/skos-ap-nl.ttl"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RDF against NL-SBB skos-ap-nl SHACL.")
    parser.add_argument("data", type=Path, help="Path to data graph (Turtle/RDF)")
    parser.add_argument(
        "--shapes",
        type=Path,
        default=DEFAULT_SHAPES,
        help=f"Path to skos-ap-nl.ttl (default: {DEFAULT_SHAPES})",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("reports"),
        help="Directory for report artefacts (default: reports)",
    )
    parser.add_argument(
        "--prefix",
        default="shacl",
        help="Filename prefix for artefacts (default: shacl)",
    )
    parser.add_argument(
        "--data-format",
        default="turtle",
        help="RDF format of data graph (default: turtle)",
    )
    args = parser.parse_args()

    if not args.data.is_file():
        raise SystemExit(f"Data file not found: {args.data}")
    if not args.shapes.is_file():
        raise SystemExit(
            f"Shapes file not found: {args.shapes}\n"
            f"Download from: {SHAPES_URL}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_txt = args.out_dir / f"_{args.prefix}-raw.txt"
    out_ttl = args.out_dir / f"_{args.prefix}-report.ttl"
    out_sum = args.out_dir / f"_{args.prefix}-summary.txt"

    conforms, results_graph, results_text = validate(
        data_graph=str(args.data),
        shacl_graph=str(args.shapes),
        data_graph_format=args.data_format,
        shacl_graph_format="turtle",
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        meta_shacl=False,
        advanced=True,
        js=False,
        debug=False,
    )

    out_txt.write_text(results_text or "", encoding="utf-8")
    results_graph.serialize(destination=str(out_ttl), format="turtle")

    severity_counts: Counter[str] = Counter()
    constraint_counts: Counter[str] = Counter()
    message_counts: Counter[str] = Counter()
    focus_by_constraint: dict[str, set[str]] = defaultdict(set)
    examples_by_constraint: dict[str, list[str]] = defaultdict(list)

    for vr in results_graph.subjects(RDF.type, SH.ValidationResult):
        sev = results_graph.value(vr, SH.resultSeverity)
        sev_name = sev.split("#")[-1] if sev else "UNKNOWN"
        severity_counts[sev_name] += 1

        src = results_graph.value(vr, SH.sourceConstraint) or results_graph.value(
            vr, SH.sourceShape
        )
        src_name = str(src).split("#")[-1] if src else "UNKNOWN"
        constraint_counts[src_name] += 1

        msg = results_graph.value(vr, SH.resultMessage)
        if msg:
            message_counts[str(msg)] += 1

        focus = results_graph.value(vr, SH.focusNode)
        if focus:
            focus_by_constraint[src_name].add(str(focus))
            if len(examples_by_constraint[src_name]) < 8:
                examples_by_constraint[src_name].append(str(focus))

    lines: list[str] = [
        f"CONFORMS\t{conforms}",
        f"RESULTS_TEXT_CHARS\t{len(results_text or '')}",
        f"RESULTS_TRIPLES\t{len(results_graph)}",
        "SEVERITY_COUNTS",
    ]
    for k, v in severity_counts.most_common():
        lines.append(f"SEV\t{k}\t{v}")
    lines.append("CONSTRAINT_COUNTS")
    for k, v in constraint_counts.most_common():
        lines.append(
            f"CON\t{k}\t{v}\tfocus_unique={len(focus_by_constraint[k])}"
        )
    lines.append("MESSAGES")
    for k, v in message_counts.most_common(40):
        lines.append(f"MSG\t{v}\t{k}")
    lines.append("EXAMPLES")
    for k, foci in examples_by_constraint.items():
        for f in foci:
            lines.append(f"EX\t{k}\t{f}")
    lines.append("DONE")

    summary = "\n".join(lines) + "\n"
    out_sum.write_text(summary, encoding="utf-8")
    print(summary, end="")
    print(f"WROTE\t{out_sum}")
    print(f"WROTE\t{out_txt}")
    print(f"WROTE\t{out_ttl}")
    return 0 if conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
