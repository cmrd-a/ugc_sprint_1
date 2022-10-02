import csv
import random
import uuid


def generate_test_data():
    with open("./views_data.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=("film_id", "user_id", "film_position_ms"))
        writer.writeheader()
        current = 0
        user_ids = random.sample(range(1, 999999), 1000)
        for _ in range(100):
            film_id = uuid.uuid4()
            for user_id in user_ids:
                for film_position_ms in range(random.randint(100, 150)):
                    writer.writerow({"film_id": film_id, "user_id": user_id, "film_position_ms": film_position_ms})
                    current += 1
                    if current >= 10000000:
                        return


if __name__ == "__main__":
    generate_test_data()
