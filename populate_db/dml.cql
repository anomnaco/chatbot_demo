CREATE TABLE vector_search_ai.qadoc_openai (
    document_id text, // RecordId
    index_id int,
    document text, // Question/Answer
    question text, // Question in separate filed
    metadata_s map<int, text>,
    vector vector<float, 1536>, //Vector data of either query OR Response
    PRIMARY KEY (document_id, index_id)
);

CREATE CUSTOM INDEX qadoc_idx ON vector_search_ai.qadoc_openai (vector) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';
