def main():
    filename = "form-data.csv"
    file_path = f"../data/{filename}"
    file_type = 'text/csv'

    group_id = get_center_id(fw=fw, adcid=0)
    log.info("Group ID for ADCID 0 is %s", group_id)

    upload_project = get_project(fw=fw, group_id=group_id)
    log.info("Using project %s/%s", upload_project.group, upload_project.label)

    if upload_project:
        upload_project.upload_file(file_path)

if __name__ == "__main__":
    main()
