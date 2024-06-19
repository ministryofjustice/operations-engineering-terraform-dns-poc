import json
from subprocess import run, CalledProcessError

ZONE_ID = "Z31RX3GZS94JZS"
MODULE_NAME = "dsd_io_records"
ZONE_FILE = "my_records.json"

def load_records(zone_file=ZONE_FILE):
    with open(zone_file) as record_file:
        data = json.load(record_file)
    return data

def terraform_import(resource_name, resource_type):
    import_command = f'terraform import module.{MODULE_NAME}.aws_route53_record.this[\\"{resource_name}_{resource_type}\\"] {ZONE_ID}_{resource_name}_{resource_type}'
    try:
        run(import_command, shell=True, check=True)
    except CalledProcessError as e:
        print(e)


if __name__ == "__main__":
    records = load_records()
    for i in records.get("ResourceRecordSets"):
        resource_name = i.get("Name")
        resource_type = i.get("Type")
        terraform_import(resource_name, resource_type)
        print(f"Imported {resource_name}")