def extract_data_from_file(day_number: int, is_official: bool = True) -> str:
    name = "data" if is_official else "practice"
    file = open(f"day_{day_number}/{name}.txt", "r")
    data = file.read()
    file.close()
    return data
