import faiss
import numpy as np

EMB_PATH = "data/embeddings_alls.npy"
INDEX_PATH = "data/faiss_index.index"

def main():
    embeddings = np.load(EMB_PATH).astype("float32")


    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index saved with {index.ntotal} vectors")

if __name__ == "__main__":
    main()
