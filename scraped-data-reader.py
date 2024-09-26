import csv

filePath = 'amazon_productsCA.csv' # needs to be changed depending on which file is being used

matchingRows = []
keywords = ['alarm clock on wheels', 'alarm clock wheels', 'alarm wheels', 'runaway alarm clock', 'wheel alarm clock', 'moving alarm clock', 'run-away', 'running alarm', 'jumping alarm clock', 'run alarm clock']

with open(filePath, newline='', encoding='utf-8') as csvFile:
    reader = csv.DictReader(csvFile)

    for row in reader:

        seller_name = row['Seller Name'].lower()  # Access 'Seller Name' column and convert to lowercase

        # Extract the price and handle cases where the price is missing or invalid
        price_str = row['Price']  # Accessing 'Price' and assigning to a variable
        try:
            price = float(price_str.replace(',', '').strip())  # Convert price to float, remove commas if any
        except (ValueError, TypeError):
            price = None  # If the price is not valid, set to None

        # Check if 'clocky' is not in the seller_name and any keyword is found in the seller_name
        if 'clocky' not in seller_name and any(keyword in seller_name for keyword in keywords) and price is not None and price < 35.00:
            matchingRows.append(row)
        

    # print(matchingRows)

# Write to CSV file
with open('amazon_likely_counterfeits.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Keyword', 'Seller Name', 'Product Link', 'Image URL', 'Price', 'Page']  
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write product data
    for product in matchingRows:
        writer.writerow(product)

print("Data has been saved to CSV file.")

