"""Helper functions for cleaning api resp data into more digestible objects"""

# def check_api_returns_valid_value(field):
#     """Converts string values to floats"""
#     if field != Nan and != None : 
#     resp = (list_dict)
#     for sub in list_dict:
#         for key in sub:
#             if key != 'period':
#                 sub[key] = '{:,.0f}'.format(float(sub[key])/1000000)


#     return resp


def convert_keys_to_str(api_dataframe):
    """Converts api response dataframe into dictionary and addresses timestamps as keys"""
    resp = api_dataframe.to_dict(orient="dict")

    for key in resp.copy():
        resp[str(key)] = resp.pop(key)

    return resp

def convert_values_to_floats(list_dict):
    """Converts string values to floats"""
    resp = (list_dict)

    for sub in list_dict:
        for key in sub:
            if key != 'period':
                try:
                    sub[key] = '{:,.0f}'.format(float(sub[key])/1000000)
                except:
                    sub[key] =  'N/A'
    return resp


def convert_rates_to_percentages(list_dict):
    """Converts string values to floats"""
    resp = (list_dict)

    for sub in list_dict:
        for key in sub:
            if key != 'period':
                try:
                    sub[key] = '{:,.0f}'.format(float(sub[key])/1000000)
                except:
                    sub[key] = 'Not a value that is convertible to percentage'

    return resp

def convert_rate_to_percentages(float_number):
    """Converts numbers to percentages"""

    percentage = '{:.0%}'.format((float_number)/1000000)

    return percentage

def convert_numbers_to_thousands(float_number):
    """Converts floats to smaller numbers and adds , decorator"""

    percentage = '{:,.0f}'.format((float_number)/1000000)

    return percentage

def convert_nums(float_number):
    """Converts floats to smaller numbers"""

    percentage = '{:.0f}'.format((float_number)/1000000)

    return percentage