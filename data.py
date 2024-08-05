import tabulate
import datetime

RENT_DURATION = 5  
FINE_PER_DAY = 10  

def table_():
    with open('equipment.txt', 'r') as file:
        data = [line.strip().split(',') for line in file]
    return tabulate.tabulate(data, headers='firstrow', tablefmt='grid')

def parse_price(price_str):
    if price_str.startswith('$'):
        return int(price_str[1:])
    return int(price_str)

def generate_invoice(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def rent_equipment():
    equipment_name = input("Enter equipment name: ")
    equipment_brand = input("Enter equipment brand: ")
    customer_name = input("Enter customer name: ")
    quantity = int(input("How many pieces to rent? "))

    data = []
    with open('equipment.txt', 'r') as file:
        for line in file:
            items = line.strip().split(',')
            data.append([item.strip() for item in items])

    equipment_details = None
    for item in data:
        if item[0] == equipment_name and item[1] == equipment_brand:
            equipment_details = item
            break

    if not equipment_details:
        print("Equipment not found.")
        return

    available_quantity = int(equipment_details[3])
    if quantity > available_quantity:
        print("Not enough stock available.")
        return

    price_per_5_days = parse_price(equipment_details[2])
    total_amount = quantity * price_per_5_days

    equipment_details[3] = str(available_quantity - quantity)
    with open('equipment.txt', 'w') as file:
        for item in data:
            file.write(', '.join(item) + '\n')

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return_date = datetime.datetime.now() + datetime.timedelta(days=RENT_DURATION)
    invoice = f"""
|                 *** IIC RENTAL SHOP ***                  |
|--------------------------------------------------------- |
|                        RENT INVOICE                      |
|                                                          |
| Invoice Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                        |
|                                                          |
| Customer: {customer_name}                                            |
|                                                          |
|----------------------------------------------------------|
| Description         | Quantity |   Unit Price           |
|---------------------|----------|------------------------|
| {equipment_name}   |    {quantity}     |   ${price_per_5_days:.2f}              |
|---------------------------------------------------------|
| Total Amount:                      |   ${total_amount:.2f} |
|---------------------------------------------------------|
| Return By: {return_date.strftime('%Y-%m-%d %H:%M:%S')}                          |
|                                                         |
| Thank you for choosing IIC Rental Shop!                 |
|---------------------------------------------------------|
 """
    invoice_name = f"Invoice_{customer_name}_{equipment_name}_{equipment_brand}_{timestamp}.txt"
    generate_invoice(invoice, invoice_name)
    print(f"Invoice generated as {invoice_name}. Keep the invoice file name for returning.")

def return_equipment():
    equipment_name = input("Enter equipment name: ")
    equipment_brand = input("Enter equipment brand: ")
    customer_name = input("Enter customer name: ")
    quantity = int(input("How many pieces are you returning? "))
    invoice_file_name = input("Enter the invoice file name when you rented the equipment: ")

    data = [line.strip().split(', ') for line in open('equipment.txt', 'r')]
    equipment_details = None
    for item in data:
        if item[0] == equipment_name and item[1] == equipment_brand:
            equipment_details = item
            break

    if not equipment_details:
        print("Equipment not found.")
        return

    rent_timestamp_str = invoice_file_name.split('_')[-1].replace('.txt', '')
    rent_timestamp = datetime.datetime.strptime(rent_timestamp_str, "%Y%m%d%H%M%S")
    return_due_date = rent_timestamp + datetime.timedelta(days=RENT_DURATION)
    total_fine = 0
    if datetime.datetime.now() > return_due_date:
        days_late = (datetime.datetime.now() - return_due_date).days
        total_fine = days_late * FINE_PER_DAY

    equipment_details[3] = str(int(equipment_details[3]) + quantity)
    with open('equipment.txt', 'w') as file:
        for item in data:
            file.write(', '.join(item) + '\n')

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return_date = datetime.datetime.now()
    invoice = f"""
    |--------------------------------------------------|
    |                                                  |
    |--------------------------------------------------|
    |                                                  |
    |           EVENT EQUIPMENT RENTAL SHOP            |
    |                                                  |
    |--------------------------------------------------|
    |                RETURN INVOICE                    |
    |--------------------------------------------------|
    |DATE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|
    |CUSTOMER NAME: {customer_name.upper()}            |
    |--------------------------------------------------|
    |EQUIPMENT:        {equipment_name.upper()}        |
    |BRAND:            {equipment_brand.upper()}       |
    |QUANTITY RETURNED:{quantity}                      |
    |TOTAL FINE:       ${total_fine:.2f}               |
    |--------------------------------------------------|
    |DATE OF RETURN: {return_date.strftime('%Y-%m-%d %H:%M:%S')}|
    |--------------------------------------------------|
    |THANK YOU FOR CHOOSING US!
    |We hope to serve you again in the future.
    """
    invoice_name = f"Return_Invoice_{customer_name}_{equipment_name}_{equipment_brand}_{timestamp}.txt"
    generate_invoice(invoice, invoice_name)
    print(f"Equipment returned successfully. Total fine: ${total_fine}")

def main():
    while True:
        print("\nEquipment Rental System:")
        print("1. View Equipment")
        print("2. Rent Equipment")
        print("3. Return Equipment")
        print("4. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            if 0 < choice < 5:
                if choice == 1:
                    print(table_())
                elif choice == 2:
                    rent_equipment()
                elif choice == 3:
                    return_equipment()
                elif choice == 4:
                    print("Thank You For Using Our Service!!!")
                    return
            else:
                print(f"Option {choice} does not exist.")
        except ValueError:
            print("Please Enter a valid number")

if __name__ == "__main__":
    main()