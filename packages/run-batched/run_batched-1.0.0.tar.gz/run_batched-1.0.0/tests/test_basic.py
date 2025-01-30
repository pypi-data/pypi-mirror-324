import unittest

import numpy as np
import torch

from run_batched import run_batched


def instrumented_double(x, batch_size_callback):
    assert isinstance(x, torch.Tensor)
    batch_size_callback(len(x))
    return 2 * x


def subtract_mean(x, batch_size_callback):
    assert isinstance(x, torch.Tensor)
    batch_size_callback(len(x))
    return x - torch.mean(x)


class TestBasic(unittest.TestCase):
    def test_addition(self):
        batch_sizes = []
        self.assertEqual(
            run_batched(
                lambda x: instrumented_double(x, batch_sizes.append),
                np.array([1, 2, 3]),
                2,
                device="cpu",
            ).tolist(),
            [2, 4, 6],
        )
        self.assertEqual(batch_sizes, [2, 1])

    def test_extremely_large_batch(self):
        batch_sizes = []
        self.assertEqual(
            run_batched(
                lambda x: instrumented_double(x, batch_sizes.append),
                np.array([1, 2, 3, 4, 5, 6]),
                100,
                device="cpu",
            ).tolist(),
            [2, 4, 6, 8, 10, 12],
        )
        self.assertEqual(batch_sizes, [6])

    def test_invalid_batch_size_not_int(self):
        with self.assertRaisesRegex(ValueError, "Batch size must be an integer."):
            run_batched(lambda x: x, np.array([1, 2, 3]), 2.5, device="cpu")

    def test_invalid_batch_size_negative(self):
        with self.assertRaisesRegex(ValueError, "Batch size must be positive."):
            run_batched(lambda x: x, np.array([1, 2, 3]), -1, device="cpu")

    def test_only_batch_first_axis(self):
        x = np.arange(2400).reshape(40, 3, -1)
        batch_sizes = []
        self.assertEqual(
            run_batched(
                lambda x: instrumented_double(x, batch_sizes.append),
                x,
                2,
                device="cpu",
            ).tolist(),
            (2 * x).tolist(),
        )
        self.assertEqual(batch_sizes, [2] * 20)

    def test_batches_consecutive(self):
        x = np.arange(10, dtype=np.float32)
        batch_sizes = []
        self.assertEqual(
            run_batched(
                lambda x: subtract_mean(x, batch_sizes.append),
                x,
                3,
                device="cpu",
            ).tolist(),
            [-1, 0, 1, -1, 0, 1, -1, 0, 1, 0],
        )
        self.assertEqual(batch_sizes, [3, 3, 3, 1])
