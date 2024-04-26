library(reticulate)
use_python(Sys.which("python3"))
flywheel <- import("flywheel")

api_key <- Sys.getenv("FW_API_KEY")
if(api_key == "") {
    stop("ERROR: environment variable FW_API_KEY not found")
}
client <- flywheel$Client(api_key)

adcid <- '0'
center_info <- import("center_info")
group_id <- center_info$get_center_id(client, adcid)
message(sprintf("Group ID for ADCID %s is %s", adcid, group_id))

pipeline <- import("pipeline")
upload_project <- tryCatch(
    pipeline$get_project(client=client, group_id=group_id, datatype='form', pipeline_type='sandbox', study_id='adrc'),
    error = function(e){
        stop('ERROR:', e)
    })

message(sprintf("Using project %s/%s", upload_project$group, upload_project$label))

filename <- "form-data-dummyv1.csv"
file_path = sprintf("/wd/%s", filename)

if(!file.exists(file_path)){
    stop(sprintf("ERROR: no file found: %s", filename))
}

if(file.size(file_path) == 0){
    stop(sprintf("file %s is empty", filename))
}

response = upload_project$upload_file(file_path)
message(sprintf("uploaded file %s: %s bytes", filename, response[[1]]$size))