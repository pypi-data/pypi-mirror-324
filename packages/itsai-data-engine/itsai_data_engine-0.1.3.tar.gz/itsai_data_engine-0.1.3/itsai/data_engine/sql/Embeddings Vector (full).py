# Databricks notebook source
dbutils.widgets.text("isIncremental", "false")
isIncremental = dbutils.widgets.get("isIncremental")

dbutils.widgets.text("tableName", "")
tableName = dbutils.widgets.get("tableName")



# COMMAND ----------

# Reference https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/matching_engine/sdk_matching_engine_create_stack_overflow_embeddings_vertex.ipynb


# COMMAND ----------

from vertexai.language_models import TextEmbeddingModel
from google.cloud import bigquery, storage, aiplatform
from typing import Generator, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
import time, functools, math, json, gc, os, glob
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
import tempfile
from pathlib import Path
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import MatchNeighbor
import re 

# COMMAND ----------

os.environ['GOOGLE_CLOUD_PROJECT'] = 'itsks-ent-search-dev-proj' # WB -
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Volumes/qa_datascience_enterprisesearch/volumes/enterprisesearch/Search/artifacts/GES/clientLibraryConfig-itsks-ent-search-oidc-dev-prvdid.json'
PROJECT_ID = 'itsks-ent-search-dev-proj'
EMBEDDING_MODEl = "textembedding-gecko@003"
BUCKET_URI = f"itsks-ent-search-dev-bkt/people2307003"
REGION = "us-east4"
EMBEDDINGS_UPDATE_URI = f"people2307003/"

# COMMAND ----------

aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_URI)

# COMMAND ----------

def encode_texts_to_embeddings(sentences: List[str]) -> List[Optional[List[float]]]:
    """Process and upload embedding data for a row in a 
    database table"""
    model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEl)
    sentencesnew = sentences.tolist()
    try:
        embeddings = model.get_embeddings(sentencesnew)
        xyz = [embedding.values for embedding in embeddings]
        #print(sentencesnew[0])
        #print(sentencesnew)
        
        return xyz
    except Exception as error:
        errorStr = str(error)
        print(errorStr)
        return [None for _ in range(len(sentencesnew))]

# COMMAND ----------

def generate_batches(
        sentences: List[str],
        batch_size: int
        ) -> Generator[List[str], None, None]:
    """Generate batches of size n from an array of sentences"""
    for i in range(0, len(sentences), batch_size):
        yield sentences[i : i + batch_size]

# COMMAND ----------

def encode_text_to_embedding_batched(
        sentences: List[str],
        api_calls_per_second: int = 10,
        batch_size: int = 5
) -> Tuple[List[bool], np.ndarray]:
    """Naive rate-limited function to batch encode text to embeddings"""
    embeddings_list: List[List[float]] = []
    batches = generate_batches(sentences, batch_size)
    seconds_per_job = 1 / api_calls_per_second
    print(seconds_per_job)
    with ThreadPoolExecutor() as executor:
        futures = []
        for batch in tqdm(
            batches,
            total=math.ceil(len(sentences) / batch_size), position=0
        ):
            futures.append(
                executor.submit(functools.partial(encode_texts_to_embeddings), batch)
            )
            time.sleep(1)

        for future in futures:
            #print(futures)
            embeddings_list.extend(future.result())

    is_successful = [
        embedding is not None for _sentence, embedding in zip(sentences, embeddings_list)
    ]
    embeddings_list_successful = np.squeeze(
        np.stack([embedding for embedding in embeddings_list if embedding is not None])
    )
    #print(embeddings_list_successful[0])
    #exit()
    return is_successful, embeddings_list_successful

# COMMAND ----------

from datetime import datetime
from datetime import timedelta

numOfHours = 20
last_hrs = (datetime.now() - timedelta(hours = numOfHours)).strftime("%Y-%m-%d %H:%M:%S")
query_template = """
SELECT * FROM `{table_name}`
ORDER BY {order_by_col} DESC
LIMIT {limit} OFFSET {offset}
WHERE bg_insertion_date > '""" + str(last_hrs) + "';"

# COMMAND ----------

print(query_template)

# COMMAND ----------

def query_bigquery_chunks(
        table_name: str,
        id_col: str,
        retrieval_cols: List[str],
        last_hrs: str,
        max_rows: int,
        rows_per_chunk: int,
        start_chunk: int = 0
) -> Generator[pd.DataFrame, Any, None]:
    if (isIncremental == "true"):
        #numOfHours = 20
       
        query_template = """
            SELECT * FROM `{table_name}`
            WHERE bg_insertion_date > '{last_hrs}' 
            ORDER BY {order_by_col} DESC
            LIMIT {limit} OFFSET {offset};"""
        print(query_template)
    else:
        query_template = """
            SELECT * FROM `{table_name}`;
            """
    client = bigquery.Client()
    for offset in range(start_chunk, max_rows, rows_per_chunk):
        if (isIncremental == "true"):
            query = query_template.format(table_name=table_name,
                                        last_hrs=last_hrs,
                                      order_by_col=id_col,
                                      limit=rows_per_chunk,
                                      offset=offset)
        else:
            query = query_template.format(table_name=table_name,
                                        order_by_col=id_col,
                                        limit=rows_per_chunk,
                                        offset=offset)
        query_job = client.query(query)
        rows = query_job.result()
        df = rows.to_dataframe()
        # Give unique names to the ID and content to retrieve
        df['_id_col'] = df[id_col]
        df['_retrieval_content'] = pd.Series(df[retrieval_cols].fillna('').values.tolist()).map(lambda x: ','.join(map(str,x)))
        yield df

# COMMAND ----------

def table_to_jsonl(table_name, id_col='id', retrieval_cols = ['content']):
    """Write all table results to a temp directory of JSON files.
    Returns path to embedding results and number of dimensions
    """
    print(table_name)    
    client = bigquery.Client()
    last_hrs = '2000-12-04 20:34:35'
    if (isIncremental == "true"):
        delpath = '/Volumes/qa_datascience_enterprisesearch/volumes/enterprisesearch/Search/VectorIncr/'
        for i in dbutils.fs.ls(delpath):
            dbutils.fs.rm(i[0],True)
        embeddings_file_path = '/Volumes/qa_datascience_enterprisesearch/volumes/enterprisesearch/Search/VectorIncr/'
        numOfHours = 60
        last_hrs = str((datetime.now() - timedelta(hours = numOfHours)).strftime("%Y-%m-%d %H:%M:%S"))
        r = client.query(f"SELECT COUNT(*) FROM {table_name} WHERE bg_insertion_date > '{last_hrs}' LIMIT 1")
    else:
        delpath = '/Volumes/qa_datascience_enterprisesearch/volumes/enterprisesearch/Search/Vector/onecmsnews/'
        for i in dbutils.fs.ls(delpath):
            dbutils.fs.rm(i[0],True)
        embeddings_file_path = '/Volumes/qa_datascience_enterprisesearch/volumes/enterprisesearch/Search/Vector/onecmsnews/'
    
        r = client.query(f"SELECT COUNT(*) FROM {table_name} LIMIT 1 ")
    
    try:
        BQ_NUM_ROWS = next(r.result())[0]
    except:
        BQ_NUM_ROWS = 0
    BQ_CHUNK_SIZE = 100
    BQ_NUM_CHUNKS = math.ceil(BQ_NUM_ROWS / BQ_CHUNK_SIZE)
    START_CHUNK = 0
    API_CALLS_PER_SECOND = 300 / 60 # 300 reqs per min
    if(BQ_NUM_ROWS > 5):
        ITEMS_PER_REQUEST = 5 # Max
    else:
        ITEMS_PER_REQUEST = BQ_NUM_ROWS

    if BQ_NUM_ROWS > 0:
        # Loop through each generated dataframe, convert
        for i, df in tqdm(
            enumerate(
                query_bigquery_chunks(
                    table_name, id_col, retrieval_cols, last_hrs, max_rows=BQ_NUM_ROWS, rows_per_chunk=BQ_CHUNK_SIZE, start_chunk=START_CHUNK
                )
            ),
            total=BQ_NUM_CHUNKS - START_CHUNK,
            position=-1,
            desc="Chunk of rows from BigQuery",
        ):
            # Create a unique output file for each chunk
            chunk_path = f"{embeddings_file_path}_{i+START_CHUNK}.json"
            with open(chunk_path, "a") as f:
                id_chunk = df['_id_col']

                # Convert batch to embeddings

                is_successful, question_chunk_embeddings = encode_text_to_embedding_batched(
                    sentences=df['_retrieval_content'],
                    api_calls_per_second=API_CALLS_PER_SECOND,
                    batch_size=ITEMS_PER_REQUEST,
                )

                # Append to file
                embeddings_formatted = [
                    json.dumps(
                        {
                            "id": str(id),
                            "embedding": [str(value) for value in embedding],
                        }
                    )
                    + "\n"
                    for id, embedding in zip(id_chunk[is_successful], question_chunk_embeddings)
                ]
                f.writelines(embeddings_formatted)
                del df
                gc.collect()
        return embeddings_file_path, len(question_chunk_embeddings[0])
    else:
        return " ", 0

# COMMAND ----------

def make_vector_index(display_name: str, 
                      num_dims: int, 
                      remote_folder: str, 
                      unique_index_name: str, 
                      description:str='') -> str:
    remote_folder2 = f"gs://{remote_folder}" if not remote_folder.startswith('gs://') else remote_folder
    
    tree_ah_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=display_name,
        contents_delta_uri=remote_folder2,
        dimensions=num_dims,
        approximate_neighbors_count=150,
        distance_measure_type="DOT_PRODUCT_DISTANCE",
        leaf_node_embedding_count=500,
        leaf_nodes_to_search_percent=80,
        description=description,
    )
    """tree_ah_index = aiplatform.MatchingEngineIndex(
    index_name='7106205222967443456')"""
    
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name=display_name,
        description=description,
        public_endpoint_enabled=False,
        network="projects/737143562546/global/networks/wbg-gcp-itsoc-dev-vpc"
    )
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name='247047068621733888')
    
    index_endpoint.deploy_index(
        index=tree_ah_index, deployed_index_id=unique_index_name
    )
    endpoint_name = index_endpoint.resource_name
    #endpoint_name = tree_ah_index.resource_name
    
    return endpoint_name

# COMMAND ----------

def upload_local_directory_to_gcs(local_path, bucket):
    print(local_path)
    if not isinstance(local_path, str):
        local_path = str(local_path)
    assert os.path.isdir(local_path)
    
    for local_file in glob.glob(local_path + '/**'):
        if not os.path.isfile(local_file):
           upload_local_directory_to_gcs(local_file, bucket, "/" + os.path.basename(local_file))
        else:
           remote_path = os.path.join(local_file[1 + len(local_path):])
           remote_path = EMBEDDINGS_UPDATE_URI + remote_path
           blob = bucket.blob(remote_path)
           blob.upload_from_filename(local_file)
           

# COMMAND ----------

def upload_to_gcs(fpath):
    client = storage.Client()
    bucket = client.bucket('itsks-ent-search-dev-bkt')
    test=upload_local_directory_to_gcs(fpath, bucket)
    return f"{BUCKET_URI}"

# COMMAND ----------

def convert_table_to_index(table_name: str, 
                           id_col: str,
                           retrieval_cols: List[str], 
                           display_name: str, 
                           unique_index_name: str, 
                           description: Optional[str]=None) -> str:
    """
    Read a BQ table into an embedding and create an online index in Google Vector Search
    
    table_name:     str             Fully scoped BQ table name (project.dataset.table)
    id_col:         str             Column in the table to use as a unique ID
    retrieval_cols: List[str]       List of columns to create embeddings from
    display_name:   str             Friendly name for the index
    index_name:     str             Unique name for the index
    description     Optional[str]   Description for the index. Defaults to display name if None
    """
    fpath, num_dims = table_to_jsonl(table_name, id_col, retrieval_cols)
    if(num_dims > 0):
      remote_folder = upload_to_gcs(fpath)
      description = display_name if description is None else description
      return make_vector_index(display_name, num_dims, remote_folder, unique_index_name, description)
    else:
      return "Nothing to index"
    

# COMMAND ----------

#pip install db_dtypes

# COMMAND ----------

import argparse
import db_dtypes  

# COMMAND ----------

#pip install db-dtypes

# COMMAND ----------

#dbutils.library.restartPython()

# COMMAND ----------

tables = {
        'projects': {
            'name': 'itsks-ent-search-dev-proj.search_internal_data.projectssummary',
            'id_col': 'id',
            'retrieval_cols': ["projectid",
                               "projectname",
                               "projectstatus",
                               "countryshortname",
                               "teamlead",
                               "doctypecode",
                               "projectabstracttext",
                               "fulltext",
                               "id"],
            'display_name': 'Projects Vector DB',
            'endpoint_name': 'projects'
        },
        'people': {
            'name': 'itsks-ent-search-dev-proj.search_internal_data.skillfinder1',
            'id_col': 'id',
            'retrieval_cols': ["id",
              "jsonData"
              ],
            'display_name': 'People Vector DB',
            'endpoint_name': 'people2307003'
        },
        'news': {
            'name': 'itsks-ent-search-dev-proj.search_internal_data.onecmsnews_s',
            'id_col': 'id',
            'retrieval_cols': [
              "id",
              "author",
              ],
            'display_name': 'News Vector DB',
            'endpoint_name': 'news'
        },
    }

# COMMAND ----------

print(table)

# COMMAND ----------



def create_index_for_table(tables):
    table = tables['news']
    index = convert_table_to_index(table['name'], table['id_col'], table['retrieval_cols'], table['display_name'], table['endpoint_name'])
    print(f"New index deployed for table:: `{index}`")

create_index_for_table(tables)
    