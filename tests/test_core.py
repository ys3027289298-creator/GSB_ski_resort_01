import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_register(self):
        state = core.new_game()
        self.assertTrue(core.register(state, "M1"))
        self.assertFalse(core.register(state, "M1"))

    def test_02_slope_capacity(self):
        state = core.new_game()
        core.enter(state, "M1")
        core.enter(state, "M2")
        result = core.enter(state, "M3")
        self.assertFalse(result)

    def test_03_fee_exact(self):
        state = core.new_game()
        self.assertEqual(core.fee(state, "M1", 3), 2)

    def test_04_cancel_refunds_deposit(self):
        state = core.new_game()
        state["balance"] = 80
        core.cancel(state, "M1")
        self.assertEqual(state["balance"], 100)

    def test_05_no_assign_absent_coach(self):
        state = core.new_game()
        core.register(state, "M1")
        result = core.assign(state, "M1", "C2")
        self.assertFalse(result)

    def test_06_refund_fail_keeps_lessons(self):
        state = core.new_game()
        core.register(state, "M1")
        state["members"]["M1"]["lessons"] = 5
        result = core.refund(state, "M1")
        self.assertFalse(result)
        self.assertEqual(state["members"]["M1"]["lessons"], 5)

    def test_07_no_open_in_bad_snow(self):
        state = core.new_game()
        state["snow"] = "poor"
        result = core.open_slope(state)
        self.assertFalse(result)

    def test_08_load_preserves_member(self):
        state = core.new_game()
        state["member_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["member_id"], 4)


if __name__ == "__main__":
    unittest.main()
