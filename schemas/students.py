def student_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item['name'],
        "age": item["age"],
        "address": item["address"]
    }


def students_entity(items) -> list:
    return [student_entity(item) for item in items]


