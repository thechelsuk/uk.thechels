import pytest
import countdown_solver


class TestCountdownSolver:

    def test_solve_simple(self):
        # 2 + 3 = 5
        solutions, summary = countdown_solver.solve([2, 3], 5)
        assert any('2 + 3' in s or '3 + 2' in s for s in solutions)
        assert 'Answer:' in summary
        assert summary.startswith('Answer:')

    def test_solve_no_solution(self):
        # No way to get 100 from [1, 2, 3]
        solutions, summary = countdown_solver.solve([1, 2, 3], 100)
        assert solutions == []
        assert 'Answer: 0 solutions.' == summary

    def test_solve_with_multiplication(self):
        # 2 * 3 = 6
        solutions, summary = countdown_solver.solve([2, 3], 6)
        assert any('2 x 3' in s or '3 x 2' in s for s in solutions)
        assert 'Answer:' in summary

    def test_solve_with_subtraction(self):
        # 5 - 2 = 3
        solutions, summary = countdown_solver.solve([5, 2], 3)
        assert any('5 - 2' in s for s in solutions)
        assert 'Answer:' in summary

    def test_solve_with_division(self):
        # 6 / 2 = 3
        solutions, summary = countdown_solver.solve([6, 2], 3)
        assert any('6 / 2' in s for s in solutions)
        assert 'Answer:' in summary

    def test_solve_duplicates(self):
        # [2, 2, 3], target 4 (2+2)
        solutions, summary = countdown_solver.solve([2, 2, 3], 4)
        assert any('2 + 2' in s for s in solutions)
        assert 'Answer:' in summary

    def test_solve_large_input(self):
        # Standard countdown numbers
        nums = [100, 25, 8, 3, 1, 1]
        target = 984
        solutions, summary = countdown_solver.solve(nums, target)
        assert isinstance(solutions, list)
        assert isinstance(summary, str)

    def test_invalid_target_type(self):
        with pytest.raises(AssertionError):
            countdown_solver.solve([1, 2, 3], 'not_an_int')

    def test_invalid_target_value(self):
        with pytest.raises(AssertionError):
            countdown_solver.solve([1, 2, 3], 0)

    def test_invalid_input_type(self):
        with pytest.raises(AssertionError):
            countdown_solver.solve(['a', 2, 3], 5)

    def test_invalid_input_value(self):
        with pytest.raises(AssertionError):
            countdown_solver.solve([0, 2, 3], 5)


if __name__ == "__main__":
    pytest.main()
