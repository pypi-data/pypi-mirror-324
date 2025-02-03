-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create agents table
CREATE TABLE IF NOT EXISTS public.agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    metadata JSONB,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create memories table
CREATE TABLE IF NOT EXISTS public.memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536),  -- OpenAI text-embedding-3-small dimension
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create memory edges table
CREATE TABLE IF NOT EXISTS public.memory_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_memory UUID REFERENCES public.memories(id) ON DELETE CASCADE,
    target_memory UUID REFERENCES public.memories(id) ON DELETE CASCADE,
    relationship TEXT NOT NULL,
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_memories_embedding ON public.memories 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for memory edges lookup
CREATE INDEX IF NOT EXISTS idx_memory_edges_source ON public.memory_edges(source_memory);
CREATE INDEX IF NOT EXISTS idx_memory_edges_target ON public.memory_edges(target_memory);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON public.agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memories_updated_at
    BEFORE UPDATE ON public.memories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create function for vector similarity search
CREATE OR REPLACE FUNCTION search_memories(
    query_vector vector(1536),
    similarity_threshold float8 DEFAULT 0.7,
    max_results integer DEFAULT 10,
    agent_id uuid DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    agent_id UUID,
    content TEXT,
    metadata JSONB,
    similarity float8
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.agent_id,
        m.content,
        m.metadata,
        1 - (m.embedding <=> query_vector) as similarity
    FROM public.memories m
    WHERE 
        m.embedding IS NOT NULL
        AND (agent_id IS NULL OR m.agent_id = agent_id)
        AND 1 - (m.embedding <=> query_vector) > similarity_threshold
    ORDER BY m.embedding <=> query_vector
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql STABLE;

-- Create function to get connected memories
CREATE OR REPLACE FUNCTION get_connected_memories(
    memory_id uuid,
    relationship_type text DEFAULT NULL,
    max_depth integer DEFAULT 1
)
RETURNS TABLE (
    source_id UUID,
    target_id UUID,
    relationship TEXT,
    weight FLOAT,
    depth INTEGER
) AS $$
WITH RECURSIVE memory_graph AS (
    -- Base case
    SELECT 
        source_memory,
        target_memory,
        relationship,
        weight,
        1 as depth
    FROM public.memory_edges
    WHERE 
        (source_memory = memory_id OR target_memory = memory_id)
        AND (relationship_type IS NULL OR relationship = relationship_type)
    
    UNION
    
    -- Recursive case
    SELECT 
        e.source_memory,
        e.target_memory,
        e.relationship,
        e.weight,
        g.depth + 1
    FROM public.memory_edges e
    INNER JOIN memory_graph g ON 
        (e.source_memory = g.target_memory OR e.target_memory = g.source_memory)
    WHERE 
        g.depth < max_depth
        AND (relationship_type IS NULL OR e.relationship = relationship_type)
)
SELECT DISTINCT
    source_memory as source_id,
    target_memory as target_id,
    relationship,
    weight,
    depth
FROM memory_graph;
$$ LANGUAGE SQL STABLE; 