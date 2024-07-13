import time

import matplotlib.pyplot as plt
import numpy as np
from django.test import TestCase
from filtering.services import main


# Create your tests here.
def test_book(input_calc_const=0.5, selected_option="cosine"):
    print("It's a test function")
    for user_num in range(4, 16, 3):
        print(f"Process {user_num}")
        book_axis = np.arange(4, 20, 3)
        time_axis = np.array([])
        for book_num in book_axis:
            start = time.perf_counter()
            main.process_all_users(
                user_num, input_calc_const, book_num, selected_option
            )
            end = time.perf_counter()
            time_count = end - start
            time_axis = np.append(time_axis, time_count)

        plt.plot(book_axis, time_axis, label=f"For {user_num} users")

    plt.legend()
    plt.show()


test_book()
