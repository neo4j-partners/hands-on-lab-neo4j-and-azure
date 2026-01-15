# Requirements Document: neo4j-graphrag-python to Java/Spring Translation

## Executive Summary

This document captures the requirements for translating the neo4j-graphrag-python library functionality used in the "Neo4j and Azure Hands-On Lab" workshop to Java and Spring. The workshop demonstrates Graph Retrieval-Augmented Generation (GraphRAG) patterns for building knowledge graphs from SEC 10-K financial filings and implementing intelligent retrieval and agentic AI systems.

---

## Part 1: Workshop Overview and Scope

### Workshop Purpose
The workshop teaches participants how to:
1. Build knowledge graphs from unstructured documents (SEC 10-K company filings)
2. Generate and store vector embeddings for semantic search
3. Implement various retrieval patterns (vector, graph-enhanced, text-to-cypher, hybrid)
4. Create intelligent agents that leverage graph-based retrieval tools

### Lab Structure
- **Lab 0-3**: Environment setup (Azure, Neo4j Aura, Microsoft Foundry)
- **Lab 4**: Knowledge Graph Building (data loading, embeddings, entity extraction)
- **Lab 5**: GraphRAG Retrievers (vector, vector+cypher, text2cypher)
- **Lab 6**: GraphRAG Agents (schema-aware agent, multi-tool agents)
- **Lab 7**: Hybrid Search (fulltext and hybrid vector+fulltext)

---

## Part 2: neo4j-graphrag-python Components Used

### 2.1 Core Data Types

#### RetrieverResultItem
A data structure representing a single retrieval result.

**Properties:**
- `content`: The main content of the retrieved item (typically the text from a chunk or formatted result)
- `metadata`: An optional dictionary containing additional information like similarity score, node labels, and element ID

**Usage in Workshop:**
- Every retriever returns results wrapped in this structure
- Custom result formatters transform Neo4j records into this format
- Used in hybrid search with custom formatters to structure company, risks, and products data

#### RetrieverResult
A container for multiple retrieval results.

**Properties:**
- `items`: A list of RetrieverResultItem objects
- `metadata`: Optional context-level metadata such as the generated Cypher query (for Text2CypherRetriever)

**Usage in Workshop:**
- The output type of all retriever `search()` methods
- Passed to GraphRAG for answer generation

#### RawSearchResult
Internal type representing unprocessed Neo4j query results.

**Properties:**
- `records`: A list of Neo4j Record objects
- `metadata`: Optional dictionary for retriever-level information

**Usage in Workshop:**
- Internal intermediary before formatting to RetrieverResult
- Text2CypherRetriever stores the generated Cypher query in metadata

---

### 2.2 Embedder Interface

#### Abstract Interface: Embedder

**Purpose:** Defines the contract for embedding text into vector representations.

**Required Method:**
- `embed_query(text)`: Takes a string and returns a list of floating-point numbers representing the vector embedding

**Constructor Parameters:**
- `rate_limit_handler`: Optional handler for managing rate limits when calling embedding APIs

**Workshop Implementation:** OpenAIEmbeddings
- Configured with model name, base URL (Microsoft Foundry endpoint), and API key
- Uses Azure CLI credentials for authentication
- Default model: "text-embedding-ada-002" (1536 dimensions)

**Usage in Workshop:**
- Generating embeddings for text chunks during data pipeline
- Converting user queries to vectors during retrieval
- Required by VectorRetriever, VectorCypherRetriever, HybridRetriever, and HybridCypherRetriever

---

### 2.3 LLM Interface

#### Abstract Interface: LLMInterface

**Purpose:** Defines the contract for interacting with large language models.

**Required Methods:**
- `invoke(input, message_history, system_instruction)`: Synchronous text generation
- `ainvoke(input, message_history, system_instruction)`: Asynchronous text generation

**Optional Methods:**
- `invoke_with_tools(input, tools, message_history, system_instruction)`: For tool/function calling
- `ainvoke_with_tools(...)`: Async version of tool calling

**Constructor Parameters:**
- `model_name`: The name of the language model
- `model_params`: Additional parameters for the model
- `rate_limit_handler`: Optional handler for rate limiting

**Response Type:** LLMResponse
- `content`: The generated text response

**Workshop Implementation:** OpenAILLM
- Configured with model name (default: "gpt-4o-mini"), base URL, and API key
- Uses Azure CLI credentials for Microsoft Foundry authentication

**Usage in Workshop:**
- Text2CypherRetriever for generating Cypher queries from natural language
- GraphRAG for generating final answers based on retrieved context
- SimpleKGPipeline for entity and relationship extraction

---

### 2.4 Retriever Base Class

#### Abstract Class: Retriever

**Purpose:** The foundation for all retrieval implementations.

**Constructor Parameters:**
- `driver`: Neo4j driver instance
- `neo4j_database`: Optional database name (defaults to server's default)

**Abstract Method:**
- `get_search_results(...)`: Must be implemented by subclasses to perform the actual retrieval

**Concrete Methods:**
- `search(...)`: Public interface that calls get_search_results and formats results
- `get_result_formatter()`: Returns the function used to transform Neo4j records
- `default_record_formatter(record)`: Default transformation logic
- `convert_to_tool(name, description, parameter_descriptions)`: Converts retriever to a Tool for agent use

**Internal Behavior:**
- Verifies Neo4j version supports vector indexes
- Fetches index information (node label, embedding property, dimensions) from Neo4j

---

### 2.5 Vector Retriever

#### Class: VectorRetriever

**Purpose:** Performs semantic similarity search using vector embeddings.

**Constructor Parameters:**
- `driver`: Neo4j driver instance
- `index_name`: Name of the vector index in Neo4j
- `embedder`: Optional Embedder instance (required for text queries)
- `return_properties`: Optional list of node properties to include in results
- `result_formatter`: Optional custom function to format Neo4j records
- `neo4j_database`: Optional database name

**Search Method Parameters:**
- `query_vector`: Pre-computed vector embedding (optional)
- `query_text`: Text to embed and search for (optional, requires embedder)
- `top_k`: Number of results to return (default: 5)
- `effective_search_ratio`: Multiplier for candidate pool size (default: 1)
- `filters`: Optional metadata filters for pre-filtering

**Behavior:**
- Either query_vector or query_text must be provided (not both)
- If query_text is provided, uses embedder to generate vector
- Executes Neo4j vector index query using `db.index.vector.queryNodes()`
- Returns nodes with similarity scores

**Usage in Workshop:**
- Basic semantic search over chunk embeddings
- Foundation for GraphRAG answer generation

---

### 2.6 Vector Cypher Retriever

#### Class: VectorCypherRetriever

**Purpose:** Combines vector similarity search with custom Cypher traversal for graph context enrichment.

**Constructor Parameters:**
- `driver`: Neo4j driver instance
- `index_name`: Name of the vector index
- `retrieval_query`: Custom Cypher query appended after vector search
- `embedder`: Optional Embedder instance
- `result_formatter`: Optional custom result formatter
- `neo4j_database`: Optional database name

**Search Method Parameters:**
- Same as VectorRetriever, plus:
- `query_params`: Optional parameters for the custom Cypher query

**Retrieval Query Context:**
The retrieval query receives:
- `node`: The matched node from vector search
- `score`: The similarity score

**Usage in Workshop:**
Three different retrieval query patterns demonstrated:

1. **Company + Risk Context:**
   - Traverses from chunk to document to company
   - Collects associated risk factors
   - Returns company name, risks array, and context text

2. **Asset Manager Context:**
   - Traverses from chunk to company to asset managers
   - Uses COLLECT subquery to limit managers per company
   - Returns company, managers list, and context

3. **Shared Risks Between Companies:**
   - Finds companies that share common risk factors
   - Groups by company pairs
   - Returns source company, related companies, and shared risks

**Critical Implementation Detail:**
The library automatically prepends the vector search query before the retrieval query, yielding `node` and `score` variables that the retrieval query can use.

---

### 2.7 Text2Cypher Retriever

#### Class: Text2CypherRetriever

**Purpose:** Converts natural language queries to Cypher queries using an LLM, then executes them.

**Constructor Parameters:**
- `driver`: Neo4j driver instance
- `llm`: LLMInterface instance for Cypher generation
- `neo4j_schema`: Optional schema string (auto-fetched if not provided)
- `examples`: Optional list of example queries for few-shot prompting
- `result_formatter`: Optional custom result formatter
- `custom_prompt`: Optional custom prompt template
- `neo4j_database`: Optional database name

**Search Method Parameters:**
- `query_text`: The natural language query
- `prompt_params`: Optional additional template parameters

**Prompt Template Variables:**
- `{schema}`: The Neo4j database schema
- `{examples}`: Example queries (if provided)
- `{query_text}`: The user's natural language query

**Response Metadata:**
- `cypher`: The generated Cypher query that was executed

**Error Handling:**
- Extracts Cypher from triple backticks if present
- Automatically quotes multi-word identifiers
- Raises Text2CypherRetrievalError on syntax errors

**Usage in Workshop:**
Custom prompt template includes:
- Instructions for using only schema-defined elements
- Case-insensitive name matching guidance
- Modern Cypher requirements (elementId instead of id, count{} instead of size(), etc.)
- LIMIT clause enforcement

---

### 2.8 Hybrid Retriever

#### Class: HybridRetriever

**Purpose:** Combines vector similarity search with fulltext keyword search.

**Constructor Parameters:**
- `driver`: Neo4j driver instance
- `vector_index_name`: Name of the vector index
- `fulltext_index_name`: Name of the fulltext index
- `embedder`: Optional Embedder instance
- `return_properties`: Optional list of node properties to return
- `result_formatter`: Optional custom result formatter
- `neo4j_database`: Optional database name

**Search Method Parameters:**
- `query_text`: The search query (required for fulltext)
- `query_vector`: Optional pre-computed vector
- `top_k`: Number of results (default: 5)
- `effective_search_ratio`: Candidate pool multiplier (default: 1)
- `ranker`: Ranking strategy ("naive" or "linear")
- `alpha`: Weight for vector score when using linear ranker (0.0 to 1.0)

**Alpha Parameter Behavior:**
- `alpha=1.0`: Pure vector (semantic) search
- `alpha=0.5`: Equal weight to both
- `alpha=0.0`: Pure fulltext (keyword) search

**Combined Score Formula (linear ranker):**
`combined_score = alpha * vector_score + (1 - alpha) * fulltext_score`

**Usage in Workshop:**
- Demonstrates different alpha values for balancing semantic vs keyword search
- Shows when hybrid outperforms single methods

---

### 2.9 Hybrid Cypher Retriever

#### Class: HybridCypherRetriever

**Purpose:** Extends hybrid search with custom Cypher graph traversal.

**Constructor Parameters:**
- Same as HybridRetriever, plus:
- `retrieval_query`: Custom Cypher query for graph enrichment

**Search Method Parameters:**
- Same as HybridRetriever, plus:
- `query_params`: Optional parameters for the retrieval query

**Usage in Workshop:**
- Traverses from matched chunks to documents, companies, risks, and products
- Uses custom result formatter to structure output as dictionary with text, company, document, risks, and products

---

### 2.10 GraphRAG Orchestrator

#### Class: GraphRAG

**Purpose:** Orchestrates the full Retrieval-Augmented Generation pipeline.

**Constructor Parameters:**
- `retriever`: Any Retriever instance
- `llm`: LLMInterface instance for answer generation
- `prompt_template`: Template for formatting context and question (default: RagTemplate)

**Search Method Parameters:**
- `query_text`: The user question
- `message_history`: Optional conversation history
- `examples`: Optional examples for the LLM
- `retriever_config`: Parameters passed to retriever (e.g., top_k)
- `return_context`: Whether to include retriever results in response
- `response_fallback`: Fallback message if no context found

**Response Type:** RagResultModel
- `answer`: The LLM-generated answer
- `retriever_result`: Optional RetrieverResult (if return_context=True)

**Pipeline Steps:**
1. Build query (summarize conversation history if present)
2. Call retriever.search() with query and config
3. If empty results and fallback provided, return fallback
4. Format prompt with context and question
5. Call LLM with prompt and optional system instructions
6. Return answer (and optionally context)

**Usage in Workshop:**
- Combined with VectorRetriever for basic RAG
- Combined with VectorCypherRetriever for graph-enhanced RAG
- Combined with Text2CypherRetriever for schema-aware RAG

---

### 2.11 Schema Retrieval

#### Function: get_schema(driver)

**Purpose:** Retrieves the database schema in a formatted string representation.

**Parameters:**
- `driver`: Neo4j driver instance
- `is_enhanced`: Include detailed statistics (default: False)
- `database`: Optional database name
- `timeout`: Optional query timeout
- `sanitize`: Remove large lists from results (default: False)
- `sample`: Number of nodes to sample (default: 1000)

**Output Format:**
```
Node properties:
Person {id: INTEGER, name: STRING}
Relationship properties:
KNOWS {fromDate: DATE}
The relationships:
(:Person)-[:KNOWS]->(:Person)
```

**Dependencies:**
Requires APOC procedures installed in Neo4j:
- `apoc.meta.data()` for property information
- `apoc.schema.nodes()` for index information
- `apoc.meta.graph()` for enhanced statistics

**Usage in Workshop:**
- Passed to Text2CypherRetriever for Cypher generation
- Used in agent tools for schema inspection

---

### 2.12 Index Management

#### Function: create_vector_index

**Purpose:** Creates a vector index on node embeddings.

**Parameters:**
- `driver`: Neo4j driver instance
- `name`: Unique index name
- `label`: Node label to index
- `embedding_property`: Property containing vectors
- `dimensions`: Vector dimensionality (e.g., 1536 for ada-002)
- `similarity_fn`: "euclidean" or "cosine"
- `fail_if_exists`: Raise error if exists (default: False)
- `neo4j_database`: Optional database name

**Generated Cypher:**
```
CREATE VECTOR INDEX $name IF NOT EXISTS
FOR (n:Label) ON n.embedding
OPTIONS { indexConfig: {
  `vector.dimensions`: $dimensions,
  `vector.similarity_function`: $similarity_fn
}}
```

**Usage in Workshop:**
- Creates "chunkEmbeddings" index on Chunk nodes
- 1536 dimensions with cosine similarity

#### Function: create_fulltext_index

**Purpose:** Creates a fulltext index for keyword search.

**Parameters:**
- `driver`: Neo4j driver instance
- `name`: Unique index name
- `label`: Node label to index
- `node_properties`: List of text properties to index
- `fail_if_exists`: Raise error if exists (default: False)
- `neo4j_database`: Optional database name

**Usage in Workshop:**
- Creates "search_entities" fulltext index for hybrid search

---

### 2.13 Text Splitting (Experimental)

#### Class: FixedSizeSplitter

**Purpose:** Splits text into fixed-size chunks with overlap.

**Constructor Parameters:**
- `chunk_size`: Maximum characters per chunk (default varies)
- `chunk_overlap`: Characters overlapping between chunks

**Method:**
- `run(text)`: Async method returning TextChunks object

**Output Type:** TextChunks
- `chunks`: List of TextChunk objects, each with:
  - `text`: The chunk content
  - `index`: Position in sequence
  - `metadata`: Optional additional information

**Usage in Workshop:**
- Splits SEC filing text into 400-character chunks with 50-character overlap
- Prepares text for embedding and storage

---

### 2.14 Knowledge Graph Pipeline (Experimental)

#### Class: SimpleKGPipeline

**Purpose:** Automated knowledge graph construction from text documents.

**Constructor Parameters:**
- `llm`: LLMInterface for entity/relation extraction
- `driver`: Neo4j driver instance
- `embedder`: Embedder for chunk embeddings
- `schema`: Schema configuration with:
  - `node_types`: List of entity type definitions
  - `relationship_types`: List of relationship type definitions
  - `patterns`: Allowed relationship patterns as tuples
- `from_pdf`: Whether to process PDF files (default: True)
- `text_splitter`: Optional custom text splitter
- `on_error`: Error handling ("RAISE" or "IGNORE")
- `perform_entity_resolution`: Merge duplicate entities (default: True)

**Schema Definition Format:**
Each entity type has:
- `label`: The node label (e.g., "Company")
- `description`: Human-readable description

Each relationship type has:
- `label`: The relationship type (e.g., "OFFERS_PRODUCT")
- `description`: Human-readable description

Patterns are tuples of (source_label, relationship_type, target_label)

**Execution Method:**
- `run_async(text=None, file_path=None, document_metadata=None)`: Processes input and builds graph

**Pipeline Steps:**
1. Load document (if PDF)
2. Split text into chunks
3. Generate embeddings for chunks
4. Extract entities and relationships using LLM
5. Write to Neo4j graph
6. Perform entity resolution if enabled

**Graph Structure Created:**
- `Document` nodes with path and metadata
- `Chunk` nodes with text and embeddings
- `FROM_DOCUMENT` relationships linking chunks to documents
- `NEXT_CHUNK` relationships forming chunk sequence
- Entity nodes (Company, Product, Service, etc.)
- `FROM_CHUNK` relationships linking entities to source chunks
- Domain relationships (OFFERS_PRODUCT, FACES_RISK, etc.)

**Usage in Workshop:**
- Extracts Company, Product, and Service entities
- Creates OFFERS_PRODUCT and OFFERS_SERVICE relationships
- Builds knowledge graph from SEC filing content

---

## Part 3: Minimally Viable Prototype Scope

### Steel Thread Definition

The steel thread prototype should demonstrate a complete end-to-end flow through the system, proving the architecture works before expanding to full functionality.

### Recommended Steel Thread: VectorRetriever + GraphRAG

**Rationale:**
- VectorRetriever is the simplest retriever implementation
- GraphRAG demonstrates the full RAG pattern
- This combination provides immediate value and proves the core architecture
- Other retrievers are variations that can be added incrementally

### Phase 1: Core Types and Interfaces

#### 1.1 Data Types to Implement

**RetrieverResultItem**
- Java record or class with content (Object) and metadata (Map<String, Object>)
- Jackson annotations for JSON serialization if needed

**RetrieverResult**
- List of RetrieverResultItem
- Optional metadata map

**RawSearchResult**
- List of Neo4j Record objects
- Optional metadata map

#### 1.2 Interfaces to Define

**Embedder Interface**
```
- Method: embedQuery(String text) -> List<Double>
- Consider: async variant for Spring WebFlux compatibility
```

**LLMInterface**
```
- Method: invoke(String input, List<Message> history, String systemInstruction) -> LLMResponse
- Consider: async variant, streaming support
```

**Retriever Abstract Class**
```
- Constructor: Neo4j Driver, optional database name
- Abstract: getSearchResults(...) -> RawSearchResult
- Concrete: search(...) -> RetrieverResult
- Concrete: getResultFormatter() -> Function<Record, RetrieverResultItem>
```

### Phase 2: VectorRetriever Implementation

#### 2.1 Constructor Requirements
- Accept Neo4j Java driver
- Accept vector index name
- Accept optional Embedder
- Accept optional list of return properties
- Accept optional result formatter function
- Fetch index metadata on construction (label, property, dimensions)

#### 2.2 Search Method Requirements
- Accept either query vector or query text
- Accept top_k parameter
- Accept effective_search_ratio parameter
- Accept optional filters
- If query text provided, use embedder to generate vector
- Execute vector index query against Neo4j
- Format and return results

#### 2.3 Neo4j Query Pattern
```
CALL db.index.vector.queryNodes($index_name, $top_k, $vector)
YIELD node, score
RETURN node.text AS text, node AS node, score,
       labels(node) AS nodeLabels, elementId(node) AS id
```

### Phase 3: GraphRAG Implementation

#### 3.1 Constructor Requirements
- Accept any Retriever implementation
- Accept LLMInterface
- Accept optional prompt template

#### 3.2 Search Method Requirements
- Accept query text
- Accept optional message history
- Accept optional retriever configuration (passed to retriever)
- Accept return_context flag
- Steps:
  1. Call retriever.search() with query
  2. Concatenate result contents as context
  3. Format prompt with context and query
  4. Call LLM with formatted prompt
  5. Return answer (and optionally context)

### Phase 4: Embedder Implementation (OpenAI-Compatible)

#### 4.1 Requirements
- Work with Azure OpenAI endpoints
- Work with Microsoft Foundry endpoints
- Support configurable model name
- Support configurable base URL
- Support API key or Azure credential authentication

#### 4.2 Spring Integration Considerations
- Use WebClient for HTTP calls
- Support both sync and async operations
- Handle rate limiting gracefully
- Configure through application properties

### Phase 5: LLM Implementation (OpenAI-Compatible)

#### 5.1 Requirements
- Same endpoint compatibility as embedder
- Support system instructions
- Support message history
- Return structured response with content

#### 5.2 Spring Integration Considerations
- Same HTTP client considerations as embedder
- Consider streaming response support for future

---

## Part 4: Extended Scope (Post-Prototype)

### Phase 6: VectorCypherRetriever
- Extends VectorRetriever
- Adds retrieval_query parameter
- Appends custom Cypher after vector search
- Supports query_params for custom query

### Phase 7: Text2CypherRetriever
- Requires schema retrieval function
- Requires prompt template system
- LLM generates Cypher from natural language
- Executes generated query
- Returns results with generated Cypher in metadata

### Phase 8: HybridRetriever
- Requires fulltext index support
- Combines vector and fulltext search
- Implements alpha-weighted score combination
- Supports both "naive" and "linear" rankers

### Phase 9: HybridCypherRetriever
- Extends HybridRetriever pattern
- Adds retrieval_query for graph traversal
- Supports custom result formatters

### Phase 10: Schema Utilities
- get_schema function implementation
- Requires APOC procedures or alternative approach
- Format output as text representation

### Phase 11: Index Management
- create_vector_index function
- create_fulltext_index function
- drop_index_if_exists function

### Phase 12: SimpleKGPipeline (Experimental)
- Most complex component
- Requires text splitting
- Requires LLM-based entity extraction
- Requires graph writing with merge logic
- Consider if this belongs in Spring prototype

---

## Part 5: Architecture Considerations for Java/Spring

### 5.1 Neo4j Integration
- Use Neo4j Java Driver (matches Python driver semantics)
- Consider Spring Data Neo4j for repository patterns
- Ensure async driver support for reactive patterns

### 5.2 Dependency Injection
- All components should be Spring beans
- Configuration through @ConfigurationProperties
- Profile-based configuration for different environments

### 5.3 Error Handling
- Define custom exception hierarchy
- Map to appropriate HTTP status codes if REST API
- Consistent error response format

### 5.4 Configuration Properties

**Neo4j Configuration:**
- neo4j.uri
- neo4j.username
- neo4j.password
- neo4j.database (optional)

**Embedding Configuration:**
- embedding.model
- embedding.base-url
- embedding.api-key (or use Azure credential chain)

**LLM Configuration:**
- llm.model
- llm.base-url
- llm.api-key (or use Azure credential chain)

### 5.5 Testing Strategy
- Unit tests for formatters and utilities
- Integration tests with embedded/test Neo4j
- Mock LLM and embedder for deterministic tests
- End-to-end tests with real services

### 5.6 Logging
- Structured logging for queries and responses
- Debug-level logging for Cypher queries
- Configurable verbosity

---

## Part 6: Workshop Translation Requirements

### 6.1 Lab 4 Translation (Knowledge Graph Building)

**Data Loading:**
- Load sample text content
- Create Document and Chunk nodes
- Store text and metadata

**Embeddings:**
- Split text using fixed-size splitter
- Generate embeddings for each chunk
- Store embeddings as node properties
- Create vector index

**Entity Extraction (Optional for MVP):**
- Can be done manually for prototype
- Full pipeline can be Phase 12

### 6.2 Lab 5 Translation (Retrievers)

**Vector Retriever Demo:**
- Initialize retriever with index name and embedder
- Execute search with sample queries
- Display results with scores

**Vector Cypher Retriever Demo:**
- Define retrieval queries for different patterns
- Show graph context enrichment

**Text2Cypher Demo:**
- Retrieve schema
- Configure custom prompt
- Show generated Cypher and results

### 6.3 Lab 6 Translation (Agents)

**Agent Framework:**
- Microsoft Agent Framework may have Java equivalent
- Alternative: Spring AI agents
- Alternative: Custom tool-calling implementation

**Tool Definitions:**
- Schema retrieval tool
- Document retrieval tool
- Database query tool

### 6.4 Lab 7 Translation (Hybrid Search)

**Fulltext Setup:**
- Create fulltext index
- Configure hybrid retriever

**Demos:**
- Alpha parameter comparison
- Search method comparison

---

## Part 7: Success Criteria

### Steel Thread (Phase 1-5) Complete When:
1. VectorRetriever successfully searches Neo4j vector index
2. Embedder generates embeddings from Azure endpoint
3. LLM generates answers from Azure endpoint
4. GraphRAG combines retrieval and generation
5. End-to-end query returns meaningful answer
6. Configuration externalized to application properties
7. Basic error handling in place
8. Unit and integration tests passing

### Full Translation Complete When:
1. All retriever types implemented
2. Schema utilities working
3. Index management functions available
4. Workshop labs reproducible in Java/Spring
5. Documentation updated for Java version
6. Performance comparable to Python version

---

## Appendix A: Data Model Reference

### Node Types
- **Document**: Source files (path, metadata)
- **Chunk**: Text segments (text, index, embedding)
- **Company**: Extracted companies (name)
- **Product**: Extracted products (name)
- **Service**: Extracted services (name)
- **RiskFactor**: Extracted risks (name)
- **AssetManager**: Extracted fund managers (managerName)

### Relationship Types
- **FROM_DOCUMENT**: Chunk to Document
- **NEXT_CHUNK**: Chunk to Chunk (sequence)
- **FROM_CHUNK**: Entity to Chunk (provenance)
- **FILED**: Document to Company
- **OFFERS_PRODUCT**: Company to Product
- **OFFERS_SERVICE**: Company to Service
- **FACES_RISK**: Company to RiskFactor
- **MENTIONS**: Company to Product
- **OWNS**: Company to AssetManager

### Indexes
- **chunkEmbeddings**: Vector index on Chunk.embedding (1536 dims, cosine)
- **search_entities**: Fulltext index for hybrid search

---

## Appendix B: Key API Contracts Summary

### Embedder
```
Input: String text
Output: List<Double> (1536 elements for ada-002)
```

### LLM
```
Input: String prompt, List<Message> history, String systemInstruction
Output: LLMResponse { String content }
```

### VectorRetriever.search
```
Input: String queryText OR List<Double> queryVector, int topK
Output: RetrieverResult { List<RetrieverResultItem> items }
```

### GraphRAG.search
```
Input: String queryText, Map<String, Object> retrieverConfig, boolean returnContext
Output: RagResult { String answer, Optional<RetrieverResult> context }
```

---

## Appendix C: Modern Cypher Requirements

The workshop enforces modern Cypher syntax for Neo4j 5+:

1. Use `elementId(node)` instead of deprecated `id(node)`
2. Use `count{pattern}` instead of `size((pattern))`
3. Use `EXISTS{MATCH pattern}` instead of `exists((pattern))`
4. Filter NULL values before ORDER BY: `WHERE prop IS NOT NULL ORDER BY prop`
5. Use explicit WITH clauses for grouping before aggregations
6. Limit collected results: `collect(item)[0..20]`

These requirements should be documented for any Text2Cypher prompt templates.

---

## Appendix D: Dependencies for Java/Spring Implementation

### Core Dependencies
- neo4j-java-driver (5.x)
- spring-boot-starter
- spring-boot-starter-webflux (for async HTTP)
- jackson-databind (JSON processing)
- lombok (optional, for boilerplate reduction)

### Azure Dependencies
- azure-identity (credential management)
- azure-ai-openai (if using official SDK)

### Testing Dependencies
- spring-boot-starter-test
- neo4j-harness (embedded test database)
- mockito (mocking)
- testcontainers-neo4j (container-based testing)
