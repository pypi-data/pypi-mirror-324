from __future__ import annotations

from mteb.abstasks.AbsTaskClassification import AbsTaskClassification
from mteb.abstasks.TaskMetadata import TaskMetadata


class ToxicConversationsClassification(AbsTaskClassification):
    metadata = TaskMetadata(
        name="ToxicConversationsClassification",
        description="Collection of comments from the Civil Comments platform together with annotations if the comment is toxic or not.",
        reference="https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/overview",
        dataset={
            "path": "mteb/toxic_conversations_50k",
            "revision": "edfaf9da55d3dd50d43143d90c1ac476895ae6de",
        },
        type="Classification",
        category="s2s",
        modalities=["text"],
        eval_splits=["test"],
        eval_langs=["eng-Latn"],
        main_score="accuracy",
        date=(
            "2017-01-01",
            "2018-12-31",
        ),  # Estimated range for the collection of comments
        domains=["Social", "Written"],
        task_subtypes=["Sentiment/Hate speech"],
        license="cc-by-4.0",
        annotations_creators="human-annotated",
        dialect=[],
        sample_creation="found",
        bibtex_citation="""@misc{jigsaw-unintended-bias-in-toxicity-classification,
    author = {cjadams and Daniel Borkan and inversion and Jeffrey Sorensen and Lucas Dixon and Lucy Vasserman and nithum},
    title = {Jigsaw Unintended Bias in Toxicity Classification},
    publisher = {Kaggle},
    year = {2019},
    url = {https://kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification}
}""",
        prompt="Classify the given comments as either toxic or not toxic",
    )

    samples_per_label = 16

    def dataset_transform(self):
        self.dataset = self.stratified_subsampling(
            self.dataset, seed=self.seed, splits=["test"]
        )
