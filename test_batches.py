from domain.model import OrderLine, Batch
from datetime import date, timedelta
import unittest


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )

class TestBatch(unittest.TestCase):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    later = tomorrow + timedelta(days=10)

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        batch, order = make_batch_and_line("PRODUCT_NAME",20, 2)
        batch.allocate(order)
        self.assertEqual(batch.available_quantity, 18)

    def test_can_allocate_if_available_greater_than_required(self):
        large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
        self.assertTrue(large_batch.can_allocate(small_line))

    def test_cannot_allocate_if_available_smaller_than_required(self):
        small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
        self.assertFalse(small_batch.can_allocate(large_line))

    def test_can_allocate_if_available_equal_to_required(self):
        batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
        self.assertTrue(batch.can_allocate(line))

    def test_cannot_allocate_if_skus_do_not_match(self):
        batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
        different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
        self.assertFalse(batch.can_allocate(different_sku_line))


    def test_allocation_is_idempotent(self):
        batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
        batch.allocate(line)
        batch.allocate(line)
        self.assertEqual(batch.available_quantity, 18)
    
    def test_can_deallocate_only_allocated_order(self):
        batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
        different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
        batch.allocate(line)
        self.assertEqual(batch.available_quantity, 18)
        batch.deallocate(different_sku_line)
        self.assertEqual(batch.available_quantity, 18)
        batch.deallocate(line)
        self.assertEqual(batch.available_quantity, 20)
    




