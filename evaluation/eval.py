import pyterrier as pt
import os
import threading


def createPath(name):
    base_path = os.getcwd() + "./evaluation/indices/"
    dataset = "/clinicaltrials_2019"
    return base_path + name + dataset


class InformationRetriever:
    def __init__(self, index_dir, stemmer, stopwords, tokeniser):
        self.index_ref = None
        self.stemmer = stemmer
        self.stopwords = stopwords
        self.tokeniser = tokeniser
        self.index_dir = index_dir

        self.dataset = None

    def buildIndex(self):
        self.dataset = pt.get_dataset('irds:clinicaltrials/2019/trec-pm-2019')
        if (os.path.exists(self.index_dir + "/data.properties") is False):
            indexer = pt.IterDictIndexer(self.index_dir, stemmer=self.stemmer, stopwords=self.stopwords, tokeniser=self.tokeniser)
            self.index_ref = indexer.index(self.dataset.get_corpus_iter(), fields=['title', 'condition', 'summary', 'detailed_description', 'eligibility'])
        else:
            self.index_ref = pt.IndexRef.of(self.index_dir + "/data.properties")

    def search(self, model, query):
        if (self.index_ref is None):
            return False
        else:
            batchRetrieve = pt.BatchRetrieve(self.index_ref, wmodel=model)
            return batchRetrieve.search(query)


class Evaluator:
    def __init__(self, ir_systems):
        self.ir_systems = ir_systems
        self.dataset = None
        self.checkSameDatasetAndAssign()

    def checkSameDatasetAndAssign(self):
        dataset = self.ir_systems[0].dataset
        for i in range(len(self.ir_systems)):
            if (dataset != self.ir_systems[i].dataset):
                return False
        self.dataset = dataset

    def compareSystems(self, wmodel):
        pipelines = []
        for model in wmodel:
            for ir_system in self.ir_systems:
                ir = pt.BatchRetrieve(ir_system.index_ref, wmodel=model)
                pipelines.append(ir)

        results = pt.Experiment(
            pipelines,
            self.dataset.get_topics("disease"),
            self.dataset.get_qrels(),
            eval_metrics=["num_rel_ret", "P_50", "map", "recip_rank", "ndcg_cut_50", "recall_50", "mrt"]
        )

        return results


if __name__ == "__main__":
    os.environ["JAVA_HOME"] = "C:/Users/Edrick/Documents/jdk-21.0.1"

    if not pt.started():
        pt.init()
        pt.ApplicationSetup.setProperty("max.term.length", "500")

    ir_systems = [
        InformationRetriever(createPath("control"), stemmer="porter", stopwords="terrier", tokeniser="english"),
        InformationRetriever(createPath("ir1"), stemmer="none", stopwords="terrier", tokeniser="english"),
        InformationRetriever(createPath("ir2"), stemmer="porter", stopwords="none", tokeniser="english"),
        InformationRetriever(createPath("ir3"), stemmer="porter", stopwords="terrier", tokeniser="whitespace"),
        InformationRetriever(createPath("ir4"), stemmer="none", stopwords="none", tokeniser="english"),
        InformationRetriever(createPath("ir5"), stemmer="none", stopwords="terrier", tokeniser="whitespace"),
        InformationRetriever(createPath("ir6"), stemmer="porter", stopwords="none", tokeniser="whitespace"),
        InformationRetriever(createPath("ir7"), stemmer="none", stopwords="none", tokeniser="whitespace")
    ]

    threads = []
    for ir_system in ir_systems:
        thread = threading.Thread(target=ir_system.buildIndex)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    ev = Evaluator(ir_systems)
    results = ev.compareSystems(["BM25", "TF_IDF", "Tf"])
    print(results)
