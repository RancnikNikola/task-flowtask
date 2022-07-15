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
            import csv
            with open('csv/service_pricing_list.csv', newline='') as f:
                next(f)
                reader = csv.DictReader(f, fieldnames=['Brand'])
                real_dict = {}
                for item in reader:
                    real_dict.setdefault(item['Brand'], []).append(item[None])
                print(real_dict)

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
