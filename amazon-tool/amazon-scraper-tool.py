import requests
from bs4 import BeautifulSoup
import csv
import random
import time

# List of User-Agent strings (browsers and devices)
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv=88.0) Gecko/20100101 Firefox/88.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',  # Updated to request English content
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'ubid-main=133-2111192-2659311; i18n-prefs=USD; lc-main=en_US; session-id=133-1686409-1952010; session-id-apay=133-1686409-1952010; _ccid=17060423407372d9r0groe; AMCV_CCBC879D5572070E7F000101%40AdobeOrg=179643557%7CMCIDTS%7C19857%7CMCMID%7C91542235582653276273622131777156236874%7CMCAAMLH-1716248248%7C9%7CMCAAMB-1716248248%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1715650648s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; _gcl_au=1.1.1662030709.1715643449; _ga=GA1.1.337916832.1715643449; _ga_MD27L7RGVC=GS1.1.1715643449.1.0.1715643449.0.0.0; _uetvid=c3556880118111efbf59718656d65e03; aws-target-data=%7B%22support%22%3A%221%22%7D; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19882%7CMCMID%7C85061598956177135124271034371069190953%7CMCAAMLH-1718340487%7C9%7CMCAAMB-1718340487%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1717742887s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; regStatus=pre-register; aws-target-visitor-id=1717735687725-13780.45_0; session-id-time=2082787201l; session-token=RypQRl2e327VrVRqqfAaTchcGddbS5mt8vKpKLYaNQxLzsuUQNuIofJDjCdNTthC6O7+iM41AdJWtqGMBUXX4dJObhuU8ukOgY/ztGY0OhCYevBrn0qyBw/+5iwXKcZDv/dY41h3hmCPwWftXP9O7+46Wz9dRbzV3DFR6paNkSaXpwJB1v0foFsGQERaThq6W5i1lKQylZHoASBomQUDTDajKHa7DKV6yYFm4OKm+2EXEtlXYSE+dxeTjanN+w/nc3AjL64Q+WhANSC5TNkdHaqG0LBELoTqVe84RBj9umDnQbTn/EmprMeppyPDZTHDsnBVAJObRgNuKKbY8At2hXCAYEbIbp7g',
'TE': 'Trailers'
}

# Keywords list
keywords = ['clocky', 'Alarm clock on wheels', 'Alarm clock wheels', 'Alarm wheels', 'Runaway alarm clock', 'Wheel alarm clock', 'Moving alarm clock', 'Run-Away', 'Running Alarm', 'Jumping alarm clock', 'Run Alarm Clock']

# Initialize data list
products_list = []

# Iterate over each keyword
for keyword in keywords:
    # Iterate over 10 result pages
    for page in range(1, 8):
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        url = f"https://www.amazon.ca/s?k={keyword.replace(' ', '+')}&page={page}"
        print(f"Scraping {url} with User-Agent: {headers['User-Agent']}")

        response = requests.get(url, headers=headers)

        # Pause for a short time to avoid detection
        time.sleep(random.uniform(1, 3))

        if response.status_code != 200:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
            continue
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_containers = soup.find_all('div', class_='s-result-item')

            for item in product_containers:
                seller_name = item.find('span', class_='a-size-base-plus')
                product_link_tag = item.find('a', class_='a-link-normal')
                image_tag = item.find('img', class_='s-image')  # Locate the image tag with class 's-image'
                
                # Try to find the price elements (whole and fraction parts)
                price_whole = item.find('span', class_='a-price-whole')
                price_fraction = item.find('span', class_='a-price-fraction')

                # Combine whole and fractional parts of the price if they exist
                # Combine whole and fractional parts of the price if they exist
                price = None
                if price_whole:
                    price_whole_cleaned = price_whole.text.strip().replace('.', '').replace('..', '')
                    price_fraction_cleaned = price_fraction.text.strip() if price_fraction else '00'
                    price = f"{price_whole_cleaned}.{price_fraction_cleaned}"


                if seller_name and product_link_tag and image_tag:
                    product_link = "https://www.amazon.ca" + product_link_tag['href']
                    image_url = image_tag['src']  # Extract the source URL of the image
                    products_list.append({
                        'Keyword': keyword,
                        'Seller Name': seller_name.text.strip(),
                        'Product Link': product_link,
                        'Image URL': image_url,  # Store the image URL
                        'Price': price,
                        'Page': page
                    })
                else:
                    print("Incomplete product details found. Skipping this item.")
        
        # Introduce a random delay between 1 and 5 seconds
        time.sleep(random.uniform(1, 5))

# Write to CSV file
with open('amazon_productsCA.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Keyword', 'Seller Name', 'Product Link', 'Image URL', 'Price', 'Page']  
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write product data
    for product in products_list:
        writer.writerow(product)

print("Data has been saved to CSV file.")