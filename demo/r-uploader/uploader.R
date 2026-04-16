library(reticulate)
use_python(Sys.which("python3"))
flywheel <- import("flywheel")

api_key <- Sys.getenv("FW_API_KEY")
if (api_key == "") {
  stop("ERROR: environment variable FW_API_KEY not found")
}
client <- flywheel$Client(api_key)

# Configuration via environment variables with defaults
adcid <- Sys.getenv("ADCID", "0")
datatype <- Sys.getenv("DATATYPE", "form")
pipeline_type <- Sys.getenv("PIPELINE", "sandbox")
study_id <- Sys.getenv("STUDYID", "adrc")

center_info <- import("nacc_common.center_info")
group_id <- center_info$get_center_id(client, adcid)
message(sprintf("Group ID for ADCID %s is %s", adcid, group_id))

pipeline <- import("nacc_common.pipeline")
upload_project <- tryCatch(
  pipeline$get_project(
    client = client,
    group_id = group_id,
    datatype = datatype,
    pipeline_type = pipeline_type,
    study_id = study_id
  ),
  error = function(e) {
    stop("ERROR:", e)
  }
)

message(sprintf(
  "Using project %s/%s",
  upload_project$group,
  upload_project$label
))

filename <- "form-data-dummyv1.csv"
file_path <- sprintf("/wd/%s", filename)

if (!file.exists(file_path)) {
  stop(sprintf("ERROR: no file found: %s", filename))
}

if (file.size(file_path) == 0) {
  stop(sprintf("file %s is empty", filename))
}

response <- upload_project$upload_file(file_path)
message(sprintf("uploaded file %s: %s bytes", filename, response[[1]]$size))
