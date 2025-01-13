import unittest
from model.model import OrderLine, Batch, OutOfStock


class TestORM(unittest.TestCase):
    def test_orderline_mapper_can_load_lines(self, session):  #(1)
        session.execute(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
        expected = [
            OrderLine("order1", "RED-CHAIR", 12),
            OrderLine("order1", "RED-TABLE", 13),
            OrderLine("order2", "BLUE-LIPSTICK", 14),
        ]
        self.assertTrue(session.query(OrderLine).all() == expected)


    def test_orderline_mapper_can_save_lines(self, session):
        new_line = OrderLine("order1", "DECORATIVE-WIDGET", 12)
        session.add(new_line)
        session.commit()

        rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
        self.assertTrue(rows == [("order1", "DECORATIVE-WIDGET", 12)])