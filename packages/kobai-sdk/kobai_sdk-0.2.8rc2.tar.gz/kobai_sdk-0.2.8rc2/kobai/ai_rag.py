from kobai import tenant_client

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType, IntegerType
#from delta.tables import *
from sentence_transformers import SentenceTransformer, util
#from deltalake import DeltaTable
from delta import DeltaTable
from typing import Union
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
#from databricks_langchain import DatabricksEmbeddings, ChatDatabricks
from langchain_community.document_loaders import PySparkDataFrameLoader
from langchain import hub
from langchain_core.output_parsers import StrOutputParser





def generate_sentences(tc: tenant_client.TenantClient, replica_schema=None, concept_white_list=None):

    """
    Extract Semantic Data from Graph to Delta Table

    Parameters:
    tc (TenantClient): The Kobai tenant_client instance instantiated via the SDK.
    replica_schema (str): An alternate schema (catalog.database) to create the Delta table. Useful when the base Kobai schema is not on a Unity Catalog.
    """
    
    if tc.spark_client is None:
        return None
    
    ss = tc.spark_client.spark_session

    print("Getting Tenant Config")
    tenant_json = tc.get_tenant_config()

    concepts = __get_concept_metadata(tenant_json, tc.schema, tc.model_id, concept_white_list)
    print(concepts)
    print("")

    print("Dropping and Recreating the RAG Table")
    ss.sql(__create_rag_table_sql(tc.schema, tc.model_id))

    print("Generating Extraction SQL")
    sql_statements = []
    sql_statements.extend(__generate_sentence_sql_concept_literals(concepts, tc.schema, tc.model_id))
    sql_statements.extend(__generate_sentence_sql_concept_relations(concepts, tc.schema, tc.model_id))

    print("Running the Extraction")
    for sql_statement in sql_statements:
        print(sql_statement)
        print("")
        ss.sql(sql_statement)

    if replica_schema is not None:
        print("Replicating Schema")
        ss.sql(__create_rag_table_sql(replica_schema, tc.model_id))
        ss.sql(__replicate_to_catalog_sql(tc.schema, replica_schema, tc.model_id))

def encode_to_delta_local(tc: tenant_client.TenantClient, st_model: SentenceTransformer, replica_schema=None):
    
    if tc.spark_client is None:
        return None
    
    ss = tc.spark_client.spark_session

    schema = tc.schema
    if replica_schema is not None:
        schema = replica_schema

    sentences_sql = f"SELECT content FROM {schema}.rag_{tc.model_id}"
    sentences_df = ss.sql(sentences_sql)

    num_records = sentences_df.count()
    query_batch_size = 100000

    #pool = model.start_multi_process_pool()

    for x in range(0, num_records, query_batch_size):
        print(f"Running Batch Starting at {x}")
        sentences_sql = f" SELECT id, content FROM {schema}.rag_{tc.model_id} ORDER BY id LIMIT {str(query_batch_size)} OFFSET {str(x)}"
        sentences_df = ss.sql(sentences_sql)
        content_list = [r["content"] for r in sentences_df.collect()]
        id_list = [r["id"] for r in sentences_df.collect()]
        #num_records_batch = len(content_list)
        #print("Done Getting Data")

        
        vector_list = st_model.encode(content_list, normalize_embeddings=True, show_progress_bar=True)
        #vector_list = model.encode_multi_process(content_list, pool)

        #print("Done Encoding")

        schemaV = StructType([
            StructField("id",IntegerType(),True),
            StructField("vector", ArrayType(FloatType()), False)
        ])

        updated_list = [[r[0], r[1].tolist()] for r in zip(id_list, vector_list)]
        updated_df = ss.createDataFrame(updated_list, schemaV)

        target_table = DeltaTable.forName(ss, f"{schema}.rag_{tc.model_id}")

        target_table.alias("t") \
        .merge(
            updated_df.alias("s"),
            't.id = s.id'
        ) \
        .whenMatchedUpdate(set = {"vector": "s.vector"}) \
        .execute()

    ss.sql(f"""
          CREATE FUNCTION IF NOT EXISTS {schema}.cos_sim(a ARRAY<FLOAT>, b ARRAY<FLOAT>)
            RETURNS FLOAT
            LANGUAGE PYTHON
            AS $$
                import numpy as np
                return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
            $$
          """)

def rag_delta(tc: tenant_client.TenantClient, emb_model: Union[SentenceTransformer, Embeddings], chat_model: BaseChatModel, question, k=5, replica_schema=None):

    schema = tc.schema
    if replica_schema is not None:
        schema = replica_schema

    if tc.spark_client is None:
        print("Instantiate Spark Client First")
        return None
    
    ss = tc.spark_client.spark_session

    if isinstance(emb_model, SentenceTransformer):
        vector_list = emb_model.encode(question, normalize_embeddings=True).tolist()
    elif isinstance(emb_model, Embeddings):
        vector_list = emb_model.embed_query(question)
    else:
        print("Invalid Embedding Model Type")
        return None
    
    if not isinstance(chat_model, BaseChatModel):
        print("Invalid Chat Model Type")
        return None

    #print(vector_list)
    vector_list = [str(x) for x in vector_list]
    #print(vector_list)
    vector_sql = ", ".join(vector_list)
    #print(vector_sql)

    results = ss.sql(f"""
            SELECT content, reduce(zip_with(vector, cast(array({vector_sql}) as array<float>), (x,y) -> x*y), float(0.0), (acc,x) -> acc + x) score
            FROM {schema}.rag_{tc.model_id}
            ORDER BY score DESC
            LIMIT {k}
            """)
    
    loader = PySparkDataFrameLoader(ss, results, page_content_column="content")
    documents = loader.load()
    docs_content = "\n\n".join(doc.page_content for doc in documents)

    #print(docs_content)

    prompt = hub.pull("rlm/rag-prompt")

    output_parser = StrOutputParser()

    chain = prompt | chat_model | output_parser

    response = chain.invoke(
        {
            "context": docs_content,
            "question": question
        }
    )

    return response

def dep_rag_delta(tc: tenant_client.TenantClient, st_model: SentenceTransformer, question, k=5, replica_schema=None):

    schema = tc.schema
    if replica_schema is not None:
        schema = replica_schema

    if tc.spark_client is None:
        return None
    
    ss = tc.spark_client.spark_session

    vector_list = st_model.encode(question, normalize_embeddings=True).tolist()

    #print(vector_list)
    vector_list = [str(x) for x in vector_list]
    #print(vector_list)
    vector_sql = ", ".join(vector_list)
    #print(vector_sql)

    results = ss.sql(f"""
            SELECT content, reduce(zip_with(vector, cast(array({vector_sql}) as array<float>), (x,y) -> x*y), float(0.0), (acc,x) -> acc + x) score
            FROM {schema}.rag_{tc.model_id}
            ORDER BY score DESC
            LIMIT {k}
            """)
    
    return results

def __create_rag_table_sql(schema, model_id):
    return f"CREATE OR REPLACE TABLE {schema}.rag_{model_id} (id BIGINT GENERATED BY DEFAULT AS IDENTITY, content STRING, type string, concept_id string, vector ARRAY<FLOAT>) TBLPROPERTIES (delta.enableChangeDataFeed = true)"
    
def __replicate_to_catalog_sql(base_schema, target_schema, model_id):
    move_sql = f"INSERT INTO {target_schema}.rag_{model_id} (content, concept_id, type)"
    move_sql += f" SELECT content, concept_id, type FROM {base_schema}.rag_{model_id}"
    return move_sql

def __generate_sentence_sql_concept_literals(concepts, schema, model_id):
    statements = []
    for con in concepts:
        sql = f"'This is a {con['label']}. '"
        #sql += " || 'It is identified by ' || split(cid._conceptid,'#')[1] || '. '"
        sql += " || 'It is identified by ' || cid._plain_conceptid || '. '"
            
        #sql_from = f"{con['con_table_name']} cid"
        sql_from = f"(SELECT _conceptid, _plain_conceptid FROM {con['prop_table_name']} GROUP BY _conceptid, _plain_conceptid) cid"
        for prop in con["properties"]:

            sql_from += f" LEFT JOIN {con['prop_table_name']} AS {prop['label']}"
            sql_from += f" ON cid._conceptid = {prop['label']}._conceptid"
            sql_from += f" AND {prop['label']}.type = 'l'"
            sql_from += f" AND {prop['label']}.name = '{prop['name']}'"
            
            sql += f" || 'The {prop['label']} is ' || ifnull(any_value({prop['label']}.value) IGNORE NULLS, 'unknown') || '. '"
        
        full_sql = f"INSERT INTO {schema}.rag_{model_id} (content, concept_id, type)"
        full_sql += f" SELECT {sql} content, cid._conceptid concept_id, 'c' type FROM {sql_from} GROUP BY cid._conceptid, cid._plain_conceptid"
        
        statements.append(full_sql)
            #test_df = spark.sql(full_sql)
    return statements

def __generate_sentence_sql_concept_relations(concepts, schema, model_id):
    statements = []
    for con in concepts:
        for rel in con["relations"]:
            sql_from = f"{con['prop_table_name']} rel"
            sql_from += f" INNER JOIN (SELECT _conceptid, _plain_conceptid FROM {rel['target_table_name']} GROUP BY _conceptid, _plain_conceptid) cid"
            sql_from += f" ON rel.value = cid._conceptid"
            sql_from += f" AND rel.type = 'r'"
            sql_from += f" AND rel.name = '{rel['name']}'"

            sql = f"'The {con['label']} identified by ' || rel._plain_conceptid"
            sql += f" || ' has a relationship called {rel['label']} that connects it to one or more {rel['target_con_label']} identified by '"
            #sql += " || concat_ws(', ', array_agg(split(value, '#')[1])) || '. '"
            sql += " || concat_ws(', ', array_agg(cid._plain_conceptid)) || '. '"

            
            full_sql = f"INSERT INTO {schema}.rag_{model_id} (content, concept_id, type)"
            full_sql += f" SELECT {sql} content, rel._conceptid concept_id, 'e' type FROM {sql_from} GROUP BY rel._conceptid, rel._plain_conceptid"

            statements.append(full_sql)
    return statements

def __get_concept_metadata(tenant_json, schema, model_id, whitelist):
    target_concept_labels = {}
    target_table_names = {}
    for d in tenant_json["domains"]:
        for c in d["concepts"]:
            target_concept_labels[c["uri"]] = d["name"] + " " + c["label"]
            target_table_names[c["uri"]] = {
                "prop": f"{schema}.data_{model_id}_{d['name']}_{c['label']}_np",
                "con": f"{schema}.data_{model_id}_{d['name']}_{c['label']}_c"
            }
    
    concepts = []
    #parents = {}
    for d in tenant_json["domains"]:
        for c in d["concepts"]:
            #if whitelist is not None and d["name"] + " " + c["label"] not in whitelist:
            #    continue
            con_props = []
            for col in c["properties"]:
                con_props.append({
                    #"col_name": d["name"] + "_" + c["label"] + "_" + col["label"],
                    "label": col["label"],
                    "name": f"{model_id}/{d['name']}/{c['label']}#{col['label']}"
                    })
            con_rels = []
            for rel in c["relations"]:
                if whitelist is not None and target_concept_labels[rel["relationTypeUri"]] not in whitelist:
                    continue
                con_rels.append({
                    "label": rel["label"],
                    "name": f"{model_id}/{d['name']}/{c['label']}#{rel['label']}",
                    "target_con_label": target_concept_labels[rel["relationTypeUri"]],
                    "target_table_name": target_table_names[rel["relationTypeUri"]]["prop"]
                })
            con_parents = []
            for p in c["inheritedConcepts"]:
                con_parents.append(p)
            concepts.append({
                "uri": c["uri"],
                "label": d["name"] + " " + c["label"],
                #"id_column": d["name"] + "_" + c["label"],
                "relations": con_rels,
                "properties": con_props,
                "parents": con_parents,
                #"table_name": "data_" + k.model_id + "_" + d["name"] + "_" + c["label"] + "_w",
                #"prop_table_name": f"{schema}.data_{model_id}_{d['name']}_{c['label']}_np",
                #"con_table_name": f"{schema}.data_{model_id}_{d['name']}_{c['label']}_c",
                "prop_table_name": target_table_names[c["uri"]]["prop"],
                "con_table_name": target_table_names[c["uri"]]["con"]
                })

    for ci, c in enumerate(concepts):
        if len(c["parents"]) > 0:
            for p in c["parents"]:
                for a in concepts:
                    if a["uri"] == p:
                        concepts[ci]["properties"].extend(a["properties"])
                        #concepts[ci]["properties"] = list(set(concepts[ci]["properties"]))

    out_concepts = []
    for c in concepts:
        if whitelist is not None and c["label"] not in whitelist:
            continue
        out_concepts.append(c)

    return out_concepts