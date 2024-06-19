import json
from subprocess import run, CalledProcessError
from string import Template
from os import path

ZONE_ID = "Z31RX3GZS94JZS"
MODULE_NAME = "dsd_io_records"
ZONE_FILE = "new_records.json"

def load_records(zone_file=ZONE_FILE):
    with open(zone_file) as record_file:
        data = json.load(record_file)
    return data

def terraform_import(record):
    record_name = record.get("Name")
    record_type = record.get("Type")
    import_command = f'terraform import module.{MODULE_NAME}.aws_route53_record.this[\\"{record_name}_{record_type}\\"] {ZONE_ID}_{record_name}_{record_type}'
    try:
        run(import_command, shell=True, check=True)
        print(f"Imported {record_name}")
    except CalledProcessError:
        print(f"generating Terraform configuration for {record_name}")
        generate_config(record)


def generate_config(record):
    config_template = Template(
    """
    {
      name = "$resource_name"
      type = "$resource_type"
      ttl  = $resource_ttl
      records = $resource_records
    },"""
    )
    alias_config_template = Template(
    """
    {
      name = "$resource_name"
      type = "$resource_type"
      alias = {
        zone_id                = "$zone_id"
        name                   = "$dns_name"
        evaluate_target_health = $evaluate_target_health
      }
    },"""
    )
    file_path = path.join("generated_configurations.json")
    with open(file_path, "a") as f:
        if "AliasTarget" in record:
            alias_target_config = record.get("AliasTarget")
            f.write(alias_config_template.substitute(resource_name=record.get("Name"), resource_type=record.get("Type"), zone_id=alias_target_config["HostedZoneId"], dns_name=alias_target_config["DNSName"], evaluate_target_health=str(alias_target_config["EvaluateTargetHealth"]).lower()))
        else:
            records = [ r["Value"].strip('\"') for r in record.get("ResourceRecords") ]
            f.write(config_template.substitute(resource_name=record.get("Name"), resource_type=record.get("Type"), resource_ttl=record.get("TTL"), resource_records=str(records).replace("'", '"')))


if __name__ == "__main__":
    records = load_records()
    for record in records.get("ResourceRecordSets"):
        terraform_import(record)
          