import requests


def get_report_data(url, data):
    headers = {
        "Content-Type": "application/json",
    }

    response_data = requests.post(url, headers=headers, json=data)

    if response_data.status_code == 200:
        return response_data.json()
    else:
        raise Exception(
            f"Failed to fetch data from {url}. Status code: {response_data.status_code}"
        )


# Define the URLs and data for the two reports
url_igh = "http://10.20.1.50:8888/report/v1/igh/"
data_igh = {
    "startDate": "2023-10-02T06:00:00.000Z",
    "endDate": "2023-10-03T05:59:59.000Z",
    "variation": "DEFAULT",
}

url_casual_harian = "http://10.20.1.50:8888/report/v1/casual-harian/"
data_casual_harian = {
    "startDate": "2023-10-02T06:00:00.000Z",
    "endDate": "2023-10-03T05:59:59.000Z",
    "variation": "DEFAULT",
    "gateId": 0,
}

# Get data for the two reports
response_igh = get_report_data(url_igh, data_igh)
response_casual_harian = get_report_data(url_casual_harian, data_casual_harian)

# Initialize total_payment_qty
total_casual_in_igh = 0

# Initialize total_payment_qty
total_casual_in_casual_harian = 0

# List of payment qty fields
total_casual_in_igh_field = ["casualIn"]

# list of total out calculated qty
total_casual_in_casual_harian_fields = ["casualIn"]

# Initialize dictionaries to store discrepancies
discrepancies_casual_in_igh = {}
discrepancies_casual_in_casual_harian = {}

# Calculate total payment quantity
for item in response_igh:
    group_by = item.get("groupBy")
    for field in total_casual_in_igh_field:
        total_casual_in_igh += item.get(field, 0)

        if group_by not in discrepancies_casual_in_igh:
            discrepancies_casual_in_igh[group_by] = 0

        discrepancies_casual_in_igh[group_by] += item.get(field, 0)

# Calculate total out calculated
for item in response_casual_harian:
    group_by = item.get("groupBy")
    for field in total_casual_in_casual_harian_fields:
        total_casual_in_casual_harian += item.get(field, 0)

        if group_by not in discrepancies_casual_in_casual_harian:
            discrepancies_casual_in_casual_harian[group_by] = 0

        discrepancies_casual_in_casual_harian[group_by] += item.get(field, 0)

# if total_casual_in_igh== total_casual_in_casual_harian:
if total_casual_in_igh == total_casual_in_casual_harian:
    print(
        f"Total Casual In IGH ({total_casual_in_igh}) matches total Casual In Casual Harian ({total_casual_in_casual_harian})"
    )
else:
    print(
        f"Total Casual In IGH ({total_casual_in_igh}) does not match total Casual In Casual Harian ({total_casual_in_casual_harian})"
    )

# Print discrepancies
for group_by, qty in discrepancies_casual_in_igh.items():
    if discrepancies_casual_in_casual_harian.get(group_by, 0) != qty:
        print(
            f"Group '{group_by}': CasualIn IGH ({qty}) does not match CasualIn Casual Harian ({discrepancies_casual_in_casual_harian.get(group_by, 0)})"
        )
