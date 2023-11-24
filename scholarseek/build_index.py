import json
import pyterrier as pt

if not pt.started():
    pt.init()

# TODO: Include other categories from https://arxiv.org/category_taxonomy
arxiv_category_taxonomy_map = {
    "cs.AI": "Artificial Intelligence",
    "cs.AR": "Hardware Architecture",
    "cs.CC": "Computational Complexity",
    "cs.CE": "Computational Engineering, Finance, and Science",
    "cs.CG": "Computational Geometry",
    "cs.CL": "Computation and Language",
    "cs.CR": "Cryptography and Security",
    "cs.CV": "Computer Vision and Pattern Recognition",
    "cs.CY": "Computers and Society",
    "cs.DB": "Databases",
    "cs.DC": "Distributed, Parallel, and Cluster Computing",
    "cs.DL": "Digital Libraries",
    "cs.DM": "Discrete Mathematics",
    "cs.DS": "Data Structures and Algorithms",
    "cs.ET": "Emerging Technologies",
    "cs.FL": "Formal Languages and Automata Theory",
    "cs.GL": "General Literature",
    "cs.GR": "Graphics",
    "cs.GT": "Computer Science and Game Theory",
    "cs.HC": "Human-Computer Interaction",
    "cs.IR": "Information Retrieval",
    "cs.IT": "Information Theory",
    "cs.LG": "Machine Learning",
    "cs.LO": "Logic in Computer Science",
    "cs.MA": "Multiagent Systems",
    "cs.MM": "Multimedia",
    "cs.MS": "Mathematical Software",
    "cs.NA": "Numerical Analysis",
    "cs.NE": "Neural and Evolutionary Computing",
    "cs.NI": "Networking and Internet Architecture",
    "cs.OH": "Other Computer Science",
    "cs.OS": "Operating Systems",
    "cs.PF": "Performance",
    "cs.PL": "Programming Languages",
    "cs.RO": "Robotics",
    "cs.SC": "Symbolic Computation",
    "cs.SD": "Sound",
    "cs.SE": "Software Engineering",
    "cs.SI": "Social and Information Networks",
    "cs.SY": "Systems and Control",
}

def arxiv_pdf_iter(arxiv_metadata_path):
    with open(arxiv_metadata_path, "r") as arxiv_metadata:
        for json_obj in arxiv_metadata:
            research_paper_metadata = json.loads(json_obj)
        
            research_paper_index_text = (
                f'{research_paper_metadata["title"] + " "}' * 3 +
                " " +
                research_paper_metadata["authors"] +
                " " +
                "".join(
                    [f'{arxiv_category_taxonomy_map.get(category, "") + " "}' * 3
                     for category in research_paper_metadata["categories"].split(" ")]
                ) +
                " " +
                research_paper_metadata["abstract"]
            )

            yield {
                "docno": research_paper_metadata["id"],
                "title": research_paper_metadata.get("title", ""),
                "authors": research_paper_metadata.get("authors", ""),
                "text": research_paper_index_text
            }



def build_index_from_pdf_iter(index_path, arxiv_metadata_path):
    iter_indexer = pt.IterDictIndexer(index_path, meta={
        'docno': 20, 
        'title': 256, 
        'authors': 256,
        'text': 1024  # Adjust the size as needed
    })
    pdf_iter = arxiv_pdf_iter(arxiv_metadata_path)
    indexref = iter_indexer.index(pdf_iter)
    index = pt.IndexFactory.of(indexref)
    return index, indexref


def main():
    arxiv_metadata_path = "./arxiv-metadata-oai-snapshot.json"
    index_path = "./index"

    index, indexref = build_index_from_pdf_iter(index_path, arxiv_metadata_path)

    # print the summary after index building process is complete
    print(index.getCollectionStatistics().toString())


if __name__ == "__main__":
    main()
