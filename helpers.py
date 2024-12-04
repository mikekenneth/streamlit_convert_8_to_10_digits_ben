def convert_8_to_10_digits(phone_number: str, prefix_to_add="01") -> list:
    if phone_number[:4] == "+229":
        return [
            f"{phone_number[:4]}{prefix_to_add}{phone_number[4:]}",
            f"{prefix_to_add}{phone_number[4:]}",
        ]
    elif len(phone_number) == 8:
        return [f"{prefix_to_add}{phone_number}"]
    else:
        return False


def process_individual_vcard(vcard: list, drop_duplicates_in_vcard: bool, prefix_to_add: str):
    updated = False
    for i in vcard:
        if i.strip().startswith("TEL;"):
            i = i.strip()
            phone_number = i.split(":")[-1].replace(" ", "")
            # check if its a valid Benin 8 Digits Number:
            if (len(phone_number) == 8 and phone_number.isnumeric()) or (
                len(phone_number) == 12 and phone_number[:4] == "+229"
            ):
                new_phone_numbers = convert_8_to_10_digits(phone_number, prefix_to_add)
                if new_phone_numbers:
                    for new_phone_number in new_phone_numbers:
                        to_add = f"{':'.join(i.split(':')[:-1])}:{new_phone_number}"
                        vcard.append(to_add)
                    updated = True
    if drop_duplicates_in_vcard:
        seen = set()
        vcard = [x for x in vcard if not (x in seen or seen.add(x))]
    return vcard, updated
