import json

from bson import json_util, ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from feature import FeatureRequest
from services.behave_services import *

mongo_host = os.getenv("MONGO_CONNECTION", "mongodb://localhost:27017/")
client = MongoClient(mongo_host)

db = client["bdd"]
collection = db["features"]

app = FastAPI(
    title="BDD Runner - BENDER ( *B*ehavior driv*EN DE*velopment *R*unner )",
    description="CRUD API to manage feature/gherkin files for BDD",
    version="0.0.1"
)

# TODO set up CORS correctly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
#         "http://localhost:5173",
#         "http://localhost:8090",
        "http://localhost:12090",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("INFO: Open swagger ui under http://localhost:12091/docs")

root_path = "/features"

doc_not_found_msg = "Document not found with id: "


@app.get("/run")
def run_all_bdd_tests() -> dict:
    documents = collection.find({})
    documents_list = [json.loads(json_util.dumps(doc)) for doc in documents]
    for document in documents_list:
        location = build_file_name(document["filename"])
        write_file_with_content(document["content"], location)
        print(f"Created feature file: {location}")
    res = run_behave_tests()
    print(res)
    return extract_results(res)


@app.get(root_path)
async def get_all_features():
    documents = collection.find({})
    documents_list = [json.loads(json_util.dumps(doc)) for doc in documents]
    return documents_list


@app.get(root_path + "/{file_id}")
async def get_single_feature_file(file_id: str):
    try:
        document = collection.find_one({"_id": ObjectId(file_id)})
        if document:
            return json_util._json_convert(document)  # bson zu JSON konvertieren
        else:
            raise HTTPException(status_code=404, detail=doc_not_found_msg + file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(root_path,
          summary="Create and store new feature file in JSON")
async def upload_single_feature_json(feature: FeatureRequest):
    filename = sanitize_filename(feature.filename)
    filename += ".feature"

    mongo_document = {
        "filename": filename,
        "content" : feature.content
    }

    result = collection.insert_one(mongo_document)
    if result.inserted_id:

        write_file_with_content(feature.content, f"features/{filename}")
        return {"file_id": str(result.inserted_id)}  # TODO: return FeatureResponse


@app.patch(root_path + "/{file_id}",
           summary="Update and store existing feature file by sending JSON")
async def update_feature(file_id: str, request: FeatureRequest):
    document_filter = {"_id": ObjectId(file_id)}

    mongo_document = {
        "filename": request.filename,
        "content" : request.content
    }

    result = collection.update_one(
        document_filter,
        {"$set": mongo_document}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Feature ${file_id} not found")

    if result.modified_count == 1:
        write_file_with_content(request.content, f"features/{request.filename}")

    return {  # TODO: use FeatureResponse instead, get initialization of _id property working
        "_id"     : {
            "$oid": file_id
        },
        "filename": request.filename,
        "content" : request.content
    }


@app.put(root_path + "/{file_id}")
async def update_single_feature_file(file_id: str, file: UploadFile = File(...)):
    oid = build_object_id(file_id)
    file_bytes = await file.read()
    content = file_bytes.decode()
    result = collection.update_one({"_id": oid}, {"$set": {"filename": file.filename, "content": content}})
    if result.matched_count:
        return {"status": f"Updated document with id: ${file_id}"}
    else:
        raise HTTPException(status_code=404, detail=doc_not_found_msg + file_id)


@app.patch(root_path + "/{file_id}/run")  # TODO vll. kann das auch ein POST auf /features/$oid werden, ohne 'run'
async def run_single_feature_file(file_id: str):
    document = find_document_by(file_id)
    if document:
        location = build_file_name(document["filename"])
        write_file_with_content(document["content"], location)
        return run_test_file(location)
    else:
        raise HTTPException(status_code=404, detail=doc_not_found_msg + file_id)


@app.delete(root_path + "/{file_id}")
async def delete_single_feature_file(file_id: str):
    oid = build_object_id(file_id)
    document = find_document_by(file_id)
    if not document:
        raise HTTPException(status_code=404, detail=doc_not_found_msg + file_id)
    try:
        delete_file_from_fs(build_file_name(document["filename"]))
    except FileNotFoundError as e:
        raise e
    result = delete_doc_from_mongo(oid)
    return {f"status": f"{result.deleted_count} document deleted"}


def build_file_name(plain_file_name: str) -> str:
    return os.getcwd() + root_path + "/" + plain_file_name


def delete_doc_from_mongo(oid):
    return collection.delete_one({"_id": oid})


def find_document_by(file_id: str):
    oid = build_object_id(file_id)
    return collection.find_one({"_id": oid})


def build_object_id(file_id: str) -> ObjectId:
    try:
        return ObjectId(file_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r'[^\w\-]', '_', filename)
    sanitized = re.sub(r'__+', '_', sanitized)
    return sanitized
