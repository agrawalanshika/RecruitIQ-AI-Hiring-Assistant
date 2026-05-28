from sentence_transformers import (

    SentenceTransformer
)

from sklearn.metrics.pairwise import cosine_similarity



model = SentenceTransformer(

    'all-MiniLM-L6-v2'
)



def calculate_semantic_similarity(

    resume_text,

    jd_text
):

    # Generate embeddings
    resume_embedding = model.encode(

        [resume_text]
    )

    jd_embedding = model.encode(

        [jd_text]
    )

    # Compute cosine similarity
    similarity = cosine_similarity(

        resume_embedding,

        jd_embedding
    )[0][0]

    return round(

        float(similarity),

        2
    )
