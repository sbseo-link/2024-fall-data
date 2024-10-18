from datetime import datetime


def born_year(age: int) -> int:
    # get current year with datetime
    current_year = datetime.now().year
    return current_year - (age - 1)


if __name__ == "__main__":
    print(born_year(20))