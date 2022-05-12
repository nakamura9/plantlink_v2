import csv
from io import StringIO
# Create your views here.
from inventory.models import Machine, Section, SubAssembly, SubUnit, Component, Spares

def parse_file(file):
    content = StringIO(file.read().decode("utf-8", "ignore"))
    reader = csv.reader(content)
    
    for i, row in enumerate(reader):
        if i < 1:
            continue
        try:
            num = int(row[0])
        except:
            print(f"error, missing data in row {i}")
            continue

        if len(str(num)) % 2 != 0:
            id_string =  "0" + str(num)
        else:
            id_string = str(num)
        name = row[1]
            
        if len(id_string) == 4:     
            machine = Machine.objects.get(pk=id_string[:2])
            Section.objects.create(
                unique_id=id_string,
                section_name=name,
                machine=machine
            )
            
        elif len(id_string) == 6:
            #Subt Unit
            machine = Machine.objects.get(pk=id_string[:2])
            section = Section.objects.get(pk=id_string[:4])
            SubUnit.objects.create(
                unique_id=id_string,
                unit_name=name,
                machine=machine,
                section=section
            )

        elif len(id_string) == 8:
            #Sub assembly
            machine = Machine.objects.get(pk=id_string[:2])
            section = Section.objects.get(pk=id_string[:4])
            subunit = SubUnit.objects.get(pk=id_string[:6])
            SubAssembly.objects.create(
                unique_id=id_string,
                unit_name=name,
                machine = machine,
                section = section,
                subunit = subunit
            )

        elif len(id_string) == 10:
            #Component
            machine = Machine.objects.get(pk=id_string[:2])
            section = Section.objects.get(pk=id_string[:4])
            subunit = SubUnit.objects.get(pk=id_string[:6])
            subassy = SubAssembly.objects.get(pk=id_string[:8])
            Component.objects.create(
                unique_id=id_string,
                component_name=name,
                machine=machine,
                section=section,
                subunit=subunit,
                subassembly=subassy
            )