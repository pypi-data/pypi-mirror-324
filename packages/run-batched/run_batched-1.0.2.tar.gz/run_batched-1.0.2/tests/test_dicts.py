import unittest

import numpy as np

from run_batched import run_batched


def instrumental_keyed(x, batch_size_callback):
    assert isinstance(x, dict)
    assert x.keys() == {"a", "b"}
    batch_size_callback({k: len(v) for k, v in x.items()})
    return {"c": x["a"] + x["b"], "d": x["a"] - x["b"]}


def return_keyed_nested(x, batch_size_callback):
    batch_size_callback(len(x))
    return {"a": x, "b": {"c": x + 1}}


def input_keyed_nested(x):
    return x["a"]["b"] - x["c"]["d"]["e"]


class TestBasic(unittest.TestCase):
    def test_keyed_basic(self):
        batch_sizes = []
        res = run_batched(
            lambda x: instrumental_keyed(x, batch_sizes.append),
            {
                "a": np.arange(10),
                "b": np.arange(10) * 10,
            },
            2,
            device="cpu",
        )
        self.assertEqual(batch_sizes, [{"a": 2, "b": 2}] * 5)

        self.assertEqual(
            list(res.keys()),
            ["c", "d"],
        )
        res = {k: v.tolist() for k, v in res.items()}
        self.assertEqual(
            res,
            {
                "c": [0, 11, 22, 33, 44, 55, 66, 77, 88, 99],
                "d": [0, -9, -18, -27, -36, -45, -54, -63, -72, -81],
            },
        )

    def test_inconsistent_sizes(self):
        with self.assertRaisesRegex(
            ValueError, "All arrays must have the same length, but got: {2, 3}"
        ):
            run_batched(
                lambda x: instrumental_keyed(x, lambda _: None),
                {
                    "a": np.arange(2),
                    "b": np.arange(3),
                },
                2,
                device="cpu",
            )

    def test_return_keyed_nested(self):
        batch_sizes = []
        res = run_batched(
            lambda x: return_keyed_nested(x, batch_sizes.append),
            np.arange(10),
            2,
            device="cpu",
        )
        self.assertEqual(batch_sizes, [2] * 5)

        self.assertEqual(
            list(res.keys()),
            ["a", "b"],
        )
        self.assertEqual(
            list(res["b"].keys()),
            ["c"],
        )
        self.assertEqual(res["a"].tolist(), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(res["b"]["c"].tolist(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_input_keyed_nested(self):
        res = run_batched(
            input_keyed_nested,
            {
                "a": {"b": np.arange(10)},
                "c": {"d": {"e": np.arange(10) * 3}},
            },
            2,
            device="cpu",
        )
        self.assertEqual(res.tolist(), [0, -2, -4, -6, -8, -10, -12, -14, -16, -18])
