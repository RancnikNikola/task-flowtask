from django.shortcuts import render, redirect
from .forms import CsvModelForm
from .models import CsvFile
import csv
from kodius.models import Brand, Model


# Create your views here.
def upload_file_view(request):

    if request.method == 'POST':

        form: CsvModelForm = CsvModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            form = CsvModelForm()
            obj = CsvFile.objects.get(uploaded=False)

            # Open file
            with open(obj.file_name.path) as file_obj:
                # Create reader object by passing the file
                # object to reader method
                next(file_obj)
                reader_obj = csv.reader(file_obj)

                # Iterate over each row in the csv
                # file using reader object
                list_of_dicts = []
                for row in reader_obj:
                    first_dict = {row[0]: row[1:]}
                    list_of_dicts.append(first_dict)

                real_dict = {
                    "Aprilia": [],
                    "Ducati": [],
                    "Yamaha": [],
                    "Kawasaki": [],
                    "Suzuki": []
                }
                for second_dict in list_of_dicts:
                    for key, value in second_dict.items():
                        real_dict[key].append(value)

                for key, values in real_dict.items():
                    print(key)
                    print(values)
                    brand = Brand.objects.create(
                            name=key
                        )
                    brand.save()

                    for value in values:
                        model_name = value[0]
                        last_supported_year = value[1]
                        chain_change_price = value[2]
                        oil_and_oil_filter_change_price = value[3]
                        air_filter_change_price = value[4]
                        brake_fluid_change_price = value[5]

                        model = Model.objects.create(
                            brand=brand,
                            name=model_name,
                            last_supported_year=last_supported_year,
                            chain_change_price=chain_change_price,
                            oil_and_oil_filter_change_price=oil_and_oil_filter_change_price,
                            air_filter_change_price=air_filter_change_price,
                            brake_fluid_change_price=brake_fluid_change_price
                        )

                    model.save()

                obj.uploaded = True
                obj.save()

    else:
        form: CsvModelForm = CsvModelForm()

    context = {'form': form}
    return render(request, 'csv_file/upload_csv.html', context)
