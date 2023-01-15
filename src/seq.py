from random import Random
from typing import MutableSequence, Dict
from storage import dump_data


def shuffle_with_seed(items: MutableSequence, seed):
    length = len(items)
    seed_type = type(seed).__name__
    print(
        f"shuffle with seed. len: {length}, seed: {seed}, seed_type:{seed_type}")
    Random(seed).shuffle(items)
    dump_data("shuffle_with_seed", {"items": items, "seed": seed})


def assign_group(items: MutableSequence[Dict], prefer_size: int):
    length = len(items)
    print(
        f"assign group. len: {length}, prefer_size: {prefer_size}")

    group_count, extra = divmod(length, prefer_size)

    it = iter(items)

    for group_idx in range(group_count):
        group_id = chr(65 + group_idx)
        group_size = prefer_size + 1 if group_idx < extra else prefer_size
        for item_idx in range(1, group_size + 1):
            item = next(it)
            item |= {"_group_id": group_id, "_group_idx": item_idx}

    dump_data("assign_group", {"items": items, "prefer_size": prefer_size})
