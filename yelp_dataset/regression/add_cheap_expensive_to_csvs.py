import csv

write_file = open('restaurants_all_with_price.csv', 'wb')

writer = csv.writer(write_file)

with open('cheap_restaurants.csv') as rf:
	
	reader = csv.reader(rf)

	temp = reader.next()
	temp.append('expensive')

	writer.writerow(temp)

	for i in range(1666):

		toAdd = reader.next()

		toAdd.append(0)

		writer.writerow(toAdd)

with open('expensive_restaurants.csv') as rf:
	reader = csv.reader(rf)

	reader.next()

	for row in reader:

		toAdd = row
		toAdd.append(1)

		writer.writerow(toAdd)

write_file.close()