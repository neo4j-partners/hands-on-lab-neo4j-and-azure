# Chunk and Entity ID Best Practices

How the `neo4j-graphrag-python` library generates and uses IDs during knowledge graph construction.

All file references below are relative to the library root at `~/projects/workshops/neo4j-graphrag-python/`.

## Chunk ID Generation

Each `TextChunk` receives a random UUID4 at creation time.

**Reference:** [`src/neo4j_graphrag/experimental/components/types.py:89-106`](src/neo4j_graphrag/experimental/components/types.py)

```python
class TextChunk(BaseModel):
    text: str
    index: int
    metadata: Optional[dict[str, Any]] = None
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))  # line 102

    @property
    def chunk_id(self) -> str:
        return self.uid
```

- `uid` is the unique identifier (UUID4 string)
- `index` tracks sequential position within the document (0, 1, 2, ...) but is **not** the ID
- `chunk_id` is a read-only property that returns `uid`

`DocumentInfo` follows the same UUID pattern at line 76:

```python
class DocumentInfo(DataModel):
    path: str
    metadata: Optional[Dict[str, str]] = None
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))  # line 76
```

## Entity ID Generation

During entity extraction, the LLM returns entity nodes with simple IDs (e.g., `"Apple"`, `"iPhone"`). The `EntityRelationExtractor.update_ids()` method then prefixes each entity ID with the source chunk's UUID to guarantee uniqueness.

**Reference:** [`src/neo4j_graphrag/experimental/components/entity_relation_extractor.py:142-158`](src/neo4j_graphrag/experimental/components/entity_relation_extractor.py)

```python
def update_ids(self, graph: Neo4jGraph, chunk: TextChunk) -> Neo4jGraph:
    """Make node IDs unique across chunks, document and pipeline runs
    by prefixing them with a unique prefix."""
    prefix = chunk.chunk_id                          # line 150
    for node in graph.nodes:
        node.id = f"{prefix}:{node.id}"              # line 152 — e.g., "a1b2c3d4-...:Apple"
    for rel in graph.relationships:
        rel.start_node_id = f"{prefix}:{rel.start_node_id}"  # line 156
        rel.end_node_id = f"{prefix}:{rel.end_node_id}"      # line 157
    return graph
```

This is called from `post_process_chunk()` at line 298, which runs after each chunk's LLM extraction completes.

## Lexical Graph: How Chunk IDs Become Neo4j Nodes

The `LexicalGraphBuilder` uses `chunk.chunk_id` as the node identifier for every graph element it creates.

**Reference:** [`src/neo4j_graphrag/experimental/components/lexical_graph.py`](src/neo4j_graphrag/experimental/components/lexical_graph.py)

| Method | Line | What it does with chunk_id |
|--------|------|---------------------------|
| `create_chunk_node()` | 126-150 | Sets `Neo4jNode(id=chunk.chunk_id, ...)` — the UUID becomes the node's primary identifier |
| `create_chunk_to_document_rel()` | 152-162 | Uses `chunk.chunk_id` as `start_node_id` in the `FROM_DOCUMENT` relationship |
| `create_next_chunk_relationship()` | 164-174 | Links `chunk.chunk_id` → `next_chunk.chunk_id` via `NEXT_CHUNK` |
| `create_node_to_chunk_rel()` | 176-184 | Links extracted entity → chunk via `FROM_CHUNK` |
| `process_chunk_extracted_entities()` | 186-203 | Creates `FROM_CHUNK` relationships for every non-lexical node in the chunk graph |

## KG Writer: How IDs Flow into Neo4j

The `Neo4jWriter` uses a temporary `__tmp_internal_id` property to match nodes during relationship creation.

**Reference:** [`src/neo4j_graphrag/experimental/components/kg_writer.py`](src/neo4j_graphrag/experimental/components/kg_writer.py) and [`src/neo4j_graphrag/neo4j_queries.py`](src/neo4j_graphrag/neo4j_queries.py)

### Step 1: Node creation (neo4j_queries.py:71-94)

```cypher
-- upsert_node_query()
UNWIND $rows AS row
CREATE (n:__KGBuilder__ {__tmp_internal_id: row.id})  -- chunk UUID or entity prefixed ID
SET n += row.properties
...
```

### Step 2: Relationship creation (neo4j_queries.py:97-121)

```cypher
-- upsert_relationship_query()
UNWIND $rows as row
MATCH (start:__KGBuilder__ {__tmp_internal_id: row.start_node_id}),
      (end:__KGBuilder__ {__tmp_internal_id: row.end_node_id})
CALL apoc.merge.relationship(start, row.type, {}, row.properties, end, row.properties) YIELD rel
...
```

### Step 3: Cleanup (neo4j_queries.py:124-137)

```cypher
-- db_cleaning_query()
MATCH (n:__KGBuilder__)
WHERE n.__tmp_internal_id IS NOT NULL
SET n.__tmp_internal_id = NULL
```

Entity vs lexical nodes are distinguished at write time (kg_writer.py:134-145): lexical nodes (Chunk, Document) keep their label as-is, while entity nodes also get an `__Entity__` label appended.

## Entity Resolution: Merging Duplicate Entities

After extraction, each mention of "Apple" from different chunks exists as separate nodes (e.g., `"uuid1:Apple"`, `"uuid2:Apple"`). Entity resolution merges them.

**Reference:** [`src/neo4j_graphrag/experimental/components/resolver.py`](src/neo4j_graphrag/experimental/components/resolver.py)

### SinglePropertyExactMatchResolver (line 74-167)

Matches entities with the **same label and exact same `name` property** using APOC `mergeNodes`:

```cypher
-- resolver.py:134-157
MATCH (entity:__Entity__)
WITH entity, entity.name as prop
WHERE prop IS NOT NULL
UNWIND labels(entity) as lab
WITH lab, prop, entity WHERE NOT lab IN ['__Entity__', '__KGBuilder__']
WITH prop, lab, collect(entity) AS entities
CALL apoc.refactor.mergeNodes(entities, { properties:'discard', mergeRels:true })
YIELD node
RETURN count(node) as c
```

### FuzzyMatchResolver (line 435-471)

Uses RapidFuzz's `WRatio` for fuzzy string matching with configurable threshold (default 0.8).

### SpaCySemanticMatchResolver (line 315-432)

Uses spaCy embeddings + cosine similarity for semantic matching.

## Graph Structure

```
(:Document) <-[:FROM_DOCUMENT]- (:Chunk) -[:NEXT_CHUNK]-> (:Chunk)
                                   ^
                                   |
                              [:FROM_CHUNK]
                                   |
                          (:Company)-[:OFFERS_PRODUCT]->(:Product)
```

## Customization Options

### Override chunk UIDs at creation

```python
chunk = TextChunk(text="...", index=0, uid="my-custom-id")
```

### Deterministic document-scoped IDs

For idempotent pipeline runs, combine document ID with chunk index:

```python
chunk = TextChunk(
    text=text,
    index=i,
    uid=f"{document_info.document_id}:chunk:{i}"
)
```

### Custom text splitter

```python
class DeterministicSplitter(TextSplitter):
    async def run(self, text: str) -> TextChunks:
        chunks = []
        for i, chunk_text in enumerate(split_texts):
            chunks.append(TextChunk(
                text=chunk_text,
                index=i,
                uid=f"doc-{doc_id}-chunk-{i}"
            ))
        return TextChunks(chunks=chunks)
```

### LexicalGraphConfig property names

**Reference:** `LexicalGraphConfig` is defined in [`src/neo4j_graphrag/experimental/components/types.py`](src/neo4j_graphrag/experimental/components/types.py)

```python
from neo4j_graphrag.experimental.components.types import LexicalGraphConfig

config = LexicalGraphConfig(
    chunk_node_label="Chunk",          # default
    chunk_id_property="id",            # Neo4j property name for chunk ID
    chunk_index_property="index",      # Neo4j property name for chunk index
    chunk_text_property="text",        # Neo4j property name for chunk text
)
```

## Key Considerations

| Concern | Default Behavior | Notes |
|---------|-----------------|-------|
| **Uniqueness** | UUID4 — globally unique | Safe for parallel processing |
| **Reproducibility** | Not reproducible | Re-running creates new IDs |
| **Idempotency** | Not idempotent | Must clear graph before re-running, or use custom deterministic IDs |
| **Entity collisions** | Prevented by chunk_id prefix | Same entity from different chunks gets separate nodes |
| **Entity merging** | Handled by entity resolution | Runs after extraction to merge duplicates |

## Complete Pipeline Flow with Line References

```
1. Text Splitting
   TextChunk created with uid=uuid4()
   → types.py:102

2. Lexical Graph Building
   Chunk node: Neo4jNode(id=chunk.chunk_id)
   FROM_DOCUMENT, NEXT_CHUNK relationships created
   → lexical_graph.py:126-174

3. Entity Extraction (per chunk, max_concurrency=5)
   LLM returns entities → post_process_chunk() prefixes IDs
   → entity_relation_extractor.py:288-303, 142-158

4. FROM_CHUNK Provenance
   Each extracted entity linked back to its source chunk
   → lexical_graph.py:186-203

5. Neo4j Writing
   Nodes created with __tmp_internal_id, relationships matched, temp IDs cleaned up
   → kg_writer.py:196-229, neo4j_queries.py:71-137

6. Entity Resolution (optional)
   Merges duplicate entities by name match (exact, fuzzy, or semantic)
   → resolver.py:74-167 (exact), 435-471 (fuzzy), 315-432 (spaCy)
```

## Source Files

| File | Line(s) | Role |
|------|---------|------|
| `types.py` | 65-82 | `DocumentInfo` — UUID generation for documents |
| `types.py` | 89-106 | `TextChunk` — UUID generation for chunks |
| `entity_relation_extractor.py` | 142-158 | `update_ids()` — prefixes entity IDs with chunk UUID |
| `entity_relation_extractor.py` | 288-303 | `post_process_chunk()` — orchestrates ID update + lexical graph linking |
| `entity_relation_extractor.py` | 337-390 | `run()` — main extraction loop with concurrency control |
| `lexical_graph.py` | 126-150 | `create_chunk_node()` — chunk UUID → Neo4j node ID |
| `lexical_graph.py` | 152-162 | `create_chunk_to_document_rel()` — FROM_DOCUMENT relationship |
| `lexical_graph.py` | 164-174 | `create_next_chunk_relationship()` — NEXT_CHUNK relationship |
| `lexical_graph.py` | 186-203 | `process_chunk_extracted_entities()` — FROM_CHUNK relationships |
| `kg_writer.py` | 134-145 | `_nodes_to_rows()` — adds `__Entity__` label to non-lexical nodes |
| `kg_writer.py` | 196-229 | `run()` — batch upsert nodes, relationships, cleanup |
| `neo4j_queries.py` | 71-94 | `upsert_node_query()` — CREATE with `__tmp_internal_id` |
| `neo4j_queries.py` | 97-121 | `upsert_relationship_query()` — MATCH by `__tmp_internal_id` |
| `neo4j_queries.py` | 124-137 | `db_cleaning_query()` — removes temp IDs |
| `resolver.py` | 74-167 | `SinglePropertyExactMatchResolver` — exact name match merging |
| `resolver.py` | 435-471 | `FuzzyMatchResolver` — RapidFuzz-based merging |
| `resolver.py` | 315-432 | `SpaCySemanticMatchResolver` — embedding-based merging |
