import csv

FILE_NAME = 'sprzedane_paabdd.csv'
# Left empty if no needed
SEARCH_WORD = ''

wrong_format = 0
offers_dict = {}


def fill_dictionary(file_row):
    offer_type = ''
    date_type = ''

    if 'Liczba zakupionych przedmiotów / zestawów / kompletów' in file_row:
        offer_type = 'Liczba zakupionych przedmiotów / zestawów / kompletów'
        date_type = 'Data zakupu'
    elif 'Liczba sprzedanych przedmiotów / zestawów / kompletów' in file_row:
        offer_type = 'Liczba sprzedanych przedmiotów / zestawów / kompletów'
        date_type = 'Data sprzedaży'

    offers_dict[int(file_row['Numer oferty'])] = {
        'name': file_row['Tytuł oferty'],
        'date': file_row[date_type],
        'quantity': int(file_row[offer_type]),
        'price': float(file_row['Kwota transakcji'])
    }


def analyze_data():
    offer_counter = 0
    summary = 0

    for number, offer in offers_dict.items():
        if SEARCH_WORD is not '' and SEARCH_WORD in str(offer['name']).lower():
            summary += offer['quantity'] * offer['price']
            offer_counter += 1
        if SEARCH_WORD is '':
            summary += offer['quantity'] * offer['price']
            offer_counter += 1

    top_offers = []
    for item in sorted(offers_dict.keys(), key=lambda x: offers_dict[x]['price']):
        top_offers.append(item)

    top_offers.reverse()

    print(len(top_offers))

    if SEARCH_WORD is not '':
        for top_offer in top_offers:
            if SEARCH_WORD is not str(offers_dict.get(top_offer).get('name')).lower():
                top_offers.remove(top_offer)

    top_offers = top_offers[0:10]

    date_from = list(offers_dict.keys())[len(offers_dict) - 1]
    date_to = list(offers_dict.keys())[0]

    print("Wrong format offers: " + str(wrong_format))
    print("date from: " + str(offers_dict.get(date_from).get('date')))
    print("date to: " + str(offers_dict.get(date_to).get('date')))
    print("Number of offers: " + str(offer_counter))
    print("Summary: " + str(round(summary, 2)) + " PLN\n")

    print("Top 10 most expensive offers:")
    for top_offer in top_offers:
        print(str(offers_dict.get(top_offer).get('price')) + " PLN " + offers_dict.get(top_offer).get('name'))


with open(FILE_NAME, encoding="utf8") as csvFile:
    reader = csv.DictReader(csvFile, delimiter=';')

    for row in reader:
        try:
            fill_dictionary(row)
        except:
            wrong_format += 1

analyze_data()



