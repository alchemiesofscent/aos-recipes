#!/usr/bin/env python3
"""Frequent ingredient co-occurrence analysis (Apriori).

Reads `data/recipes.json` and `data/ingredient_lexicon.json`. Builds one
transaction per recipe (the set of canonical `lookup_key`s its ingredients
resolve to), then runs the Apriori algorithm up to `--max-k`, keeping every
k-itemset that appears in at least `--min-count` recipes.

Writes one JSON file per k under `data/analysis/cooccurrence/`, a sibling
`index.json` with run metadata, and a human-readable summary at
`docs/cooccurrence.md`.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPES_JSON = ROOT / "data" / "recipes.json"
LEXICON_JSON = ROOT / "data" / "ingredient_lexicon.json"
OUT_DIR = ROOT / "data" / "analysis" / "cooccurrence"
INDEX_JSON = OUT_DIR / "index.json"
REPORT_MD = ROOT / "docs" / "cooccurrence.md"

DEFAULT_MIN_COUNT = 3
DEFAULT_MAX_K = 10
DEFAULT_TOP_PER_K = 200
RECIPE_ID_CAP = 20


def load_lexicon() -> tuple[dict[str, str], dict[str, str]]:
    payload = json.loads(LEXICON_JSON.read_text(encoding="utf-8"))
    id_to_key: dict[str, str] = {}
    display_for_key: dict[str, str] = {}
    for entry in payload["entries"]:
        lookup = entry["lookup_key"]
        display_for_key[lookup] = entry.get("display_entry") or lookup
        for occ in entry.get("occurrences", []):
            id_to_key[occ["ingredient_id"]] = lookup
    return id_to_key, display_for_key


def build_transactions(
    id_to_key: dict[str, str],
) -> tuple[list[tuple[str, set[str]]], list[tuple[str, str]], int, int, int]:
    payload = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
    recipes = payload["recipes"]
    transactions: list[tuple[str, set[str]]] = []
    fallback_hits: list[tuple[str, str]] = []
    uncertain = 0
    total = 0
    for recipe in recipes:
        ings = recipe.get("ingredients") or []
        if not ings:
            continue
        keys: set[str] = set()
        for ing in ings:
            total += 1
            if ing.get("certainty") == "uncertain":
                uncertain += 1
            iid = ing.get("ingredient_id") or ""
            key = id_to_key.get(iid)
            if key is None:
                key = ing.get("normalized_label") or iid
                fallback_hits.append((recipe["recipe_id"], iid))
            keys.add(key)
        transactions.append((recipe["recipe_id"], keys))
    return transactions, fallback_hits, uncertain, total, len(recipes)


def generate_candidates(
    L_prev: list[tuple[str, ...]],
    L_prev_set: set[frozenset[str]],
) -> list[tuple[str, ...]]:
    """Apriori join + prune. L_prev must be sorted ascending; tuples sorted."""
    cands: list[tuple[str, ...]] = []
    n = len(L_prev)
    for i in range(n):
        a = L_prev[i]
        prefix = a[:-1]
        for j in range(i + 1, n):
            b = L_prev[j]
            if b[:-1] != prefix:
                break
            new = a + (b[-1],)
            if all(
                frozenset(sub) in L_prev_set
                for sub in combinations(new, len(new) - 1)
            ):
                cands.append(new)
    return cands


def apriori(
    transactions: list[tuple[str, set[str]]],
    min_count: int,
    max_k: int,
) -> dict[int, list[tuple[tuple[str, ...], int, list[str]]]]:
    """Returns {k: [(members_tuple_sorted, count, sorted_recipe_ids), ...]}."""
    results: dict[int, list[tuple[tuple[str, ...], int, list[str]]]] = {}

    counts_1: Counter[str] = Counter()
    recipes_1: dict[str, list[str]] = defaultdict(list)
    for rid, keys in transactions:
        for key in keys:
            counts_1[key] += 1
            recipes_1[key].append(rid)
    L1_items = [k for k, c in counts_1.items() if c >= min_count]
    if not L1_items:
        return results
    L1_items.sort()
    results[1] = [
        ((k,), counts_1[k], sorted(recipes_1[k])) for k in L1_items
    ]

    L_prev: list[tuple[str, ...]] = [(k,) for k in L1_items]
    L_prev_set: set[frozenset[str]] = {frozenset(t) for t in L_prev}

    for k in range(2, max_k + 1):
        candidates = generate_candidates(L_prev, L_prev_set)
        if not candidates:
            break
        c_counts: Counter[tuple[str, ...]] = Counter()
        c_recipes: dict[tuple[str, ...], list[str]] = defaultdict(list)
        for rid, keys in transactions:
            if len(keys) < k:
                continue
            for cand in candidates:
                if all(m in keys for m in cand):
                    c_counts[cand] += 1
                    c_recipes[cand].append(rid)
        Lk_items = [c for c, cnt in c_counts.items() if cnt >= min_count]
        if not Lk_items:
            break
        Lk_items.sort()
        results[k] = [(c, c_counts[c], sorted(c_recipes[c])) for c in Lk_items]
        L_prev = Lk_items
        L_prev_set = {frozenset(t) for t in Lk_items}

    return results


def render_itemset(
    members: tuple[str, ...],
    count: int,
    recipe_ids: list[str],
    recipe_count: int,
    display_for_key: dict[str, str],
) -> dict:
    capped = recipe_ids[:RECIPE_ID_CAP]
    return {
        "members": list(members),
        "display": [display_for_key.get(m, m) for m in members],
        "count": count,
        "support": round(count / recipe_count, 4),
        "recipe_ids": capped,
        "recipe_id_overflow": len(recipe_ids) > RECIPE_ID_CAP,
    }


def sort_itemset_records(records: list[dict]) -> list[dict]:
    return sorted(records, key=lambda r: (-r["count"], r["members"]))


def build_outputs(
    results: dict[int, list[tuple[tuple[str, ...], int, list[str]]]],
    recipe_count: int,
    display_for_key: dict[str, str],
) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {}
    for k, items in results.items():
        records = [
            render_itemset(m, c, rids, recipe_count, display_for_key)
            for (m, c, rids) in items
        ]
        out[k] = sort_itemset_records(records)
    return out


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def write_per_k_files(
    per_k: dict[int, list[dict]], min_count: int, top_per_k: int
) -> None:
    for k, records in per_k.items():
        emitted = records if top_per_k == 0 else records[:top_per_k]
        write_json(
            OUT_DIR / f"k{k:02d}.json",
            {
                "k": k,
                "min_count": min_count,
                "frequent_count": len(records),
                "emitted_count": len(emitted),
                "itemsets": emitted,
            },
        )


def remove_stale_per_k_files(per_k: dict[int, list[dict]], max_k: int) -> None:
    """Delete kNN.json files left from a previous higher-k run that no longer have records."""
    if not OUT_DIR.exists():
        return
    keep = {f"k{k:02d}.json" for k in per_k}
    for path in OUT_DIR.glob("k*.json"):
        if path.name not in keep:
            path.unlink()


def render_markdown_report(
    per_k: dict[int, list[dict]],
    *,
    recipe_count: int,
    transaction_count: int,
    lookup_key_count: int,
    min_count: int,
    max_k_attempted: int,
    fallback_hits: list[tuple[str, str]],
    uncertain: int,
    total: int,
) -> str:
    lines: list[str] = []
    lines.append("# Ingredient Co-occurrence Analysis")
    lines.append("")
    lines.append(
        "Auto-generated by `scripts/cooccurrence.py`. Do not edit by hand; "
        "re-run the script to refresh."
    )
    lines.append("")

    lines.append("## Method")
    lines.append("")
    lines.append(
        "Apriori frequent-itemset mining. Each recipe contributes one transaction: "
        "the set of canonical ingredient `lookup_key`s (from "
        "`data/ingredient_lexicon.json`) that appear in it. A k-itemset is "
        "reported if it appears in at least `min_count` recipes; the loop runs "
        "until either `max_k` is reached or no more frequent itemsets are found."
    )
    lines.append("")

    lines.append("## Parameters")
    lines.append("")
    lines.append(f"- `min_count` = **{min_count}**")
    lines.append(f"- `max_k_attempted` = **{max_k_attempted}**")
    max_k_with = max(per_k) if per_k else 0
    lines.append(f"- `max_k_with_results` = **{max_k_with}**")
    lines.append(f"- recipes in corpus: **{recipe_count}**")
    lines.append(
        f"- recipes contributing to analysis (≥1 ingredient): **{transaction_count}**"
    )
    lines.append(f"- distinct lookup_keys in lexicon: **{lookup_key_count}**")
    frac = (uncertain / total) if total else 0.0
    lines.append(
        f"- ingredient occurrences flagged uncertain: **{uncertain}/{total}** "
        f"({frac:.1%})"
    )
    lines.append(f"- lexicon fallback hits: **{len(fallback_hits)}**")
    lines.append("")

    lines.append("## Per-k counts")
    lines.append("")
    lines.append("| k | frequent itemsets |")
    lines.append("|---|---|")
    for k in sorted(per_k):
        lines.append(f"| {k} | {len(per_k[k])} |")
    lines.append("")

    def render_table(records: list[dict], limit: int) -> list[str]:
        rows: list[str] = []
        rows.append("| rank | count | support | ingredients |")
        rows.append("|---|---|---|---|")
        for rank, r in enumerate(records[:limit], start=1):
            display = " + ".join(r["display"])
            rows.append(
                f"| {rank} | {r['count']} | {r['support']:.4f} | {display} |"
            )
        if not records:
            rows.append("| _(none)_ | | | |")
        return rows

    if 1 in per_k:
        lines.append("## Top 30 single ingredients (k=1)")
        lines.append("")
        lines.extend(render_table(per_k[1], 30))
        lines.append("")

    if 2 in per_k:
        lines.append("## Top 20 pairs (k=2)")
        lines.append("")
        lines.extend(render_table(per_k[2], 20))
        lines.append("")

    if 3 in per_k:
        lines.append("## Top 20 triples (k=3)")
        lines.append("")
        lines.extend(render_table(per_k[3], 20))
        lines.append("")

    for k in sorted(per_k):
        if k < 4:
            continue
        lines.append(f"## Top 10 {k}-tuples (k={k})")
        lines.append("")
        lines.extend(render_table(per_k[k], 10))
        lines.append("")

    lines.append("## Caveats")
    lines.append("")
    lines.append(
        "- Recipes with zero structured ingredients are excluded from "
        "transactions (they cannot contribute to any itemset)."
    )
    lines.append(
        "- Ingredients marked `certainty: uncertain` are kept; the uncertain "
        "share above lets a reader discount accordingly."
    )
    if fallback_hits:
        lines.append(
            "- Some recipe ingredients had no entry in the lexicon and fell "
            "back to `normalized_label`. See the index for the count; the join "
            "should be tightened in the lexicon if this is non-zero."
        )
    lines.append(
        "- Support is `count / recipe_count` (denominator includes the few "
        "ingredient-less recipes), so support values are slightly conservative."
    )
    lines.append("")

    return "\n".join(lines)


def write_report(text: str) -> None:
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(text, encoding="utf-8")


def compute(
    min_count: int, max_k: int
) -> tuple[dict[int, list[dict]], dict, str]:
    id_to_key, display_for_key = load_lexicon()
    transactions, fallback_hits, uncertain, total, recipe_count = build_transactions(
        id_to_key
    )
    results = apriori(transactions, min_count, max_k)
    per_k = build_outputs(results, recipe_count, display_for_key)

    index_payload: dict = {
        "recipe_count": recipe_count,
        "transaction_count": len(transactions),
        "lookup_key_count": len(display_for_key),
        "min_count": min_count,
        "max_k_attempted": max_k,
        "max_k_with_results": max(per_k) if per_k else 0,
        "per_k_counts": {str(k): len(v) for k, v in per_k.items()},
        "fallback_count": len(fallback_hits),
        "uncertain_occurrences": uncertain,
        "ingredient_occurrences": total,
    }
    report = render_markdown_report(
        per_k,
        recipe_count=recipe_count,
        transaction_count=len(transactions),
        lookup_key_count=len(display_for_key),
        min_count=min_count,
        max_k_attempted=max_k,
        fallback_hits=fallback_hits,
        uncertain=uncertain,
        total=total,
    )
    return per_k, index_payload, report


def cmd_run(min_count: int, max_k: int, top_per_k: int) -> int:
    per_k, index_payload, report = compute(min_count, max_k)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_per_k_files(per_k, min_count, top_per_k)
    remove_stale_per_k_files(per_k, max_k)
    index_payload["top_per_k"] = top_per_k
    index_payload["generated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    write_json(INDEX_JSON, index_payload)
    write_report(report)
    total = sum(len(v) for v in per_k.values())
    emitted = sum(
        (len(v) if top_per_k == 0 else min(len(v), top_per_k))
        for v in per_k.values()
    )
    print(
        f"wrote {len(per_k)} per-k files (k=1..{max(per_k) if per_k else 0}); "
        f"{total} frequent itemsets found, {emitted} emitted "
        f"(top_per_k={top_per_k or 'unlimited'})"
    )
    return 0


def cmd_check(min_count: int, max_k: int, top_per_k: int) -> int:
    per_k, index_payload, report = compute(min_count, max_k)
    errors: list[str] = []

    if not INDEX_JSON.exists():
        errors.append(f"missing {INDEX_JSON.relative_to(ROOT)}")
    else:
        committed = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
        for field in (
            "recipe_count",
            "transaction_count",
            "lookup_key_count",
            "min_count",
            "max_k_attempted",
            "max_k_with_results",
            "per_k_counts",
            "fallback_count",
            "uncertain_occurrences",
            "ingredient_occurrences",
        ):
            if committed.get(field) != index_payload.get(field):
                errors.append(
                    f"index.json {field}: committed={committed.get(field)!r} "
                    f"recomputed={index_payload.get(field)!r}"
                )
        if committed.get("top_per_k") != top_per_k:
            errors.append(
                f"index.json top_per_k: committed={committed.get('top_per_k')!r} "
                f"recomputed={top_per_k!r}"
            )

    for k, records in per_k.items():
        path = OUT_DIR / f"k{k:02d}.json"
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        committed = json.loads(path.read_text(encoding="utf-8"))
        expected = records if top_per_k == 0 else records[:top_per_k]
        if committed.get("itemsets") != expected:
            errors.append(f"k{k:02d}.json itemsets differ from recomputed")
        if committed.get("frequent_count") != len(records):
            errors.append(f"k{k:02d}.json frequent_count differs from recomputed")

    if REPORT_MD.exists():
        if REPORT_MD.read_text(encoding="utf-8") != report:
            errors.append("docs/cooccurrence.md differs from recomputed")
    else:
        errors.append(f"missing {REPORT_MD.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("OK: committed cooccurrence outputs match recomputed analysis")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--min-count",
        type=int,
        default=DEFAULT_MIN_COUNT,
        help=f"minimum recipe count for an itemset to be 'frequent' "
        f"(default: {DEFAULT_MIN_COUNT})",
    )
    parser.add_argument(
        "--max-k",
        type=int,
        default=DEFAULT_MAX_K,
        help=f"maximum itemset size to attempt (default: {DEFAULT_MAX_K})",
    )
    parser.add_argument(
        "--top-per-k",
        type=int,
        default=DEFAULT_TOP_PER_K,
        help=f"emit at most this many itemsets per k in the JSON files "
        f"(0 = unlimited; default: {DEFAULT_TOP_PER_K}). The Markdown "
        f"report and 'frequent_count' field always reflect the full sweep.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="recompute and compare against committed outputs; exit non-zero on mismatch",
    )
    args = parser.parse_args(argv)
    if args.min_count < 1:
        print("--min-count must be >= 1", file=sys.stderr)
        return 2
    if args.max_k < 1:
        print("--max-k must be >= 1", file=sys.stderr)
        return 2
    if args.top_per_k < 0:
        print("--top-per-k must be >= 0", file=sys.stderr)
        return 2
    if args.check:
        return cmd_check(args.min_count, args.max_k, args.top_per_k)
    return cmd_run(args.min_count, args.max_k, args.top_per_k)


if __name__ == "__main__":
    sys.exit(main())
