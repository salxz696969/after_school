from strawberry import Info


def extract_fields(info: Info) -> list[str]:
    return [field.name for field in info.selected_fields[0].selections if field] # type: ignore