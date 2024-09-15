

def transform_to_lower_resolution(high_resolution_application_number: str) -> str:
    high_res_split = high_resolution_application_number.split('/')
    first_part = high_res_split[0]
    first_part = str.join('-', first_part.split('-')[0:2])
    return first_part + '/' + high_res_split[1]
