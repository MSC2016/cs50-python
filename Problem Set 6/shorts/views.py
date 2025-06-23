import numpy as np
import csv

from PIL import Image

# import PILImage, this helps with intellisense and code hints
from PIL.Image import Image as PILImage 

def main():
    print(calculate_brightness('image1.jpg'))
    print(calculate_brightness('output.jpg'))

    # open 2 files in the same with block
    with open('data.csv', 'r') as data_in, open('result.csv', 'w') as data_out:
        reader = csv.DictReader(data_in)
        # writer for result.csv, using the same fields as the reader PLUS the field we want to add
        writer = csv.DictWriter(data_out, fieldnames=reader.fieldnames + ['Estimated Taxes'])
        # write the same headers from the input file in the results file
        writer.writeheader()

        # BETTER WAY TO ADD FIELDS TO CSV FILES
        for row in reader:
            # calculate the tax value, gett the value of salary and multiply by .15
            tax_value = float(row['Salary']) * 0.15
            # because its a dictionary, we just need to add a new field
            row['Estimated Taxes'] = tax_value
            writer.writerow(row)


        # EDIT EACH FIELD AND DATA SEPARATLY
        # TOO MUTCH CODE WHEN WE JUST WANT TO ADD ONE FIELD
        # for row in reader:
        #     tax_deductions = 0.15
        #     tax_value = float(row['Salary']) * tax_deductions
            
        #     writer.writerow(
        #         {
        #             'Name': row['Name'],
        #             'Department': row['Department'],
        #             'Age': row['Age'],
        #             'Salary': row['Salary'],
        #             'Estimated Taxes': tax_value,
        #         }
        #     )


def calculate_brightness(filename):
    with Image.open(filename) as image:
        image: PILImage
        brightness = np.mean(np.array(image.convert('L')))
    return brightness

if __name__ == '__main__':
    main()
