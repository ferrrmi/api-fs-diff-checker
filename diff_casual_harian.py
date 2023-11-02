import requests


url = "http://10.20.1.50:8888/report/v1/casual-harian/"

headers = {
    "Content-Type": "application/json",
}

data = {
    "startDate": "2023-10-02T06:00:00.000Z",
    "endDate": "2023-10-03T05:59:59.000Z",
    "variation": "DEFAULT",
    "gateId": 0,
}

response_data = requests.post(url, headers=headers, json=data)

response = response_data.json()

# Initialize total_payment_qty
total_payment_qty = 0

# Initialize total_payment_qty
total_out_calculated = 0

# List of payment qty fields
payment_qty_fields = [
    "cashQty",
    "eMoneyQty",
    "brizziQty",
    "flazzQty",
    "tapCashQty",
    "dkiQty",
    "gopayQty",
    "ovoQty",
    "danaQty",
    "linkAjaQty",
    "shopeePayQty",
    "danaExternalQty",
    "qrisQty",
    "permataVaQty",
    "bniVaQty",
    "briVaQty",
    "edcMandiriQty",
    "edcBriQty",
    "edcBniQty",
    "edcBcaQty",
]

# list of total out calculated qty
total_out_calculated_fields = ["totalOutCalculated"]

# Initialize dictionaries to store discrepancies
discrepancies_payment_qty = {}
discrepancies_out_calculated = {}

# Calculate total payment quantity
for item in response:
    group_by = item.get("groupBy")
    for field in payment_qty_fields:
        total_payment_qty += item.get(field, 0)

        if group_by not in discrepancies_payment_qty:
            discrepancies_payment_qty[group_by] = 0

        discrepancies_payment_qty[group_by] += item.get(field, 0)

# Calculate total out calculated
for item in response:
    group_by = item.get("groupBy")
    for field in total_out_calculated_fields:
        total_out_calculated += item.get(field, 0)

        if group_by not in discrepancies_out_calculated:
            discrepancies_out_calculated[group_by] = 0

        discrepancies_out_calculated[group_by] += item.get(field, 0)

# if total_payment_qty == total_out_calculated:
if total_payment_qty == total_out_calculated:
    print(
        f"Total Payment Quantity ({total_payment_qty}) matches Total Out Calculated ({total_out_calculated})"
    )
else:
    print(
        f"Total Payment Quantity ({total_payment_qty}) does not match Total Out Calculated ({total_out_calculated})"
    )

# Print discrepancies
for group_by, qty in discrepancies_payment_qty.items():
    if discrepancies_out_calculated.get(group_by, 0) != qty:
        print(
            f"Group '{group_by}': Payment Quantity ({qty}) does not match Out Calculated ({discrepancies_out_calculated.get(group_by, 0)})"
        )
