
import numpy as np

def get_reward(state, new_state):
    """
    Возвращает вознаграждение на основе изменений в состоянии игры.
    """
    if is_line_cleared(state, new_state):
        return 1  
    elif is_game_over(state, new_state):
        return -1  
    else:
        return 0  

def is_line_cleared(state, new_state):
    """
    Проверяет, была ли очищена линия.
    """

    old_lines = np.sum(np.all(state > 0, axis=1))
    new_lines = np.sum(np.all(new_state > 0, axis=1))
    if new_lines < old_lines:
        return True
    return False

def is_game_over(state, new_state, tolerance=3):
    """
    Проверяет окончание игры.
    :param state: Текущее состояние игры.
    :param new_state: Новое состояние игры.
    :param tolerance: Максимальное количество заполненных ячеек в верхнем ряду для продолжения игры.
    """

    top_row = new_state[0]
    non_zero_top_row = np.count_nonzero(top_row)
    if non_zero_top_row >= tolerance:
        print(f"Игра завершена: верхний ряд заполнен ({non_zero_top_row} ячеек).")
        return True


    if np.array_equal(state, new_state):
        print("Игра завершена: состояние не изменилось.")
        return True

    return False
