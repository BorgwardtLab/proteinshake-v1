class Task:
    """
    Abstract class for Tasks. A task contains the logic for splitting, target generation, and evaluation.
    Optionally, we can consider the Task as a way of syncing with a paperwithcode instance https://github.com/paperswithcode/paperswithcode-client.
    """

    def __init__(
        self,
        dataset: proteinshake.Dataset,
        splitter: proteinshake.Splitter,
        target: proteinshake.Target,
        evaluator: proteinshake.Evaluator,
        task_id: int,
    ) -> None:
        self.dataset = dataset
        self.train_idx = splitter.train_idx()
        self.val_idx = splitter.val_idx()
        self.test_idx = splitter.test_idx()

        self.task_id = task_id

        self.target = target
        self.evaluator = evaluator
        pass

    def leaderboard_fetch(self):
        """Load current leaderboard results for this task"""

        if not self.task_id is None:
            return get_leaderboard(f"https:/paperswithcode.com/sota/{self.task_id}")
