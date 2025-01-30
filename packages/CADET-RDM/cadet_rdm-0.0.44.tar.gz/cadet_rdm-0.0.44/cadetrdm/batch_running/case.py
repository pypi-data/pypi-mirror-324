import traceback
from pathlib import Path

from .study import Study
from .options import Options

class Case:
    def __init__(self, study: Study, options: Options, name: str = None):
        if name is None:
            name = options.get_hash()

        self.name = name
        self.study = study
        self.options = options
        self._options_hash = options.get_hash()
        self._results_branch = None

    @property
    def status_file(self):
        return Path(self.study.path).parent / (Path(self.study.path).name + ".status")

    @property
    def status(self):
        status, _ = self._read_status()
        return status

    @status.setter
    def status(self, status):
        """Update the status file with the current execution status."""

        with open(self.status_file, "w") as f:
            f.write(f"{status}@{self.study.current_commit_hash}")

    @property
    def status_hash(self):
        _, status_hash = self._read_status()
        return status_hash

    def _read_status(self):
        """Check the status of the study and decide whether to proceed.

        Args:
            repo_path (Path): The path to the repository containing the status file.

        Returns:
            tuple: A tuple containing the status string and the current hash,
            or None, None if the status cannot be determined.
        """

        if not self.status_file.exists():
            return None, None

        with open(self.status_file) as f:
            status = f.read().strip()
            try:
                status, current_hash = status.split("@")
            except ValueError as e:
                if status == '':
                    return None, None
                else:
                    raise e

            return status, current_hash

    @property
    def is_running(self, ):
        if self.status == 'running':
            return True

        return False

    @property
    def has_results_for_this_run(self):
        self._results_branch = self._get_results_branch()
        if self._results_branch is None:
            return False
        else:
            return True

    def _get_results_branch(self):
        output_log = self.study.output_log
        study_options_hash = self.options.get_hash()
        study_commit_hash = self.study.current_commit_hash
        has_been_run_with_these_options = False
        has_been_run_with_this_commit = False
        semi_correct_hits = []
        for log_entry in output_log:
            entry_options_hash = log_entry.options_hash
            entry_commit_hash = log_entry.project_repo_commit_hash
            if study_commit_hash == entry_commit_hash and study_options_hash == entry_options_hash:
                return log_entry.output_repo_branch
            elif study_commit_hash == entry_commit_hash and study_options_hash != entry_options_hash:
                has_been_run_with_this_commit = True
                semi_correct_hits.append(
                    f"Found matching study commit hash {study_commit_hash[:7]}, but incorrect options hash "
                    f"(needs: {study_options_hash[:7]}, has: {entry_options_hash[:7]})"
                )
            elif study_commit_hash != entry_commit_hash and study_options_hash == entry_options_hash:
                has_been_run_with_these_options = True
                semi_correct_hits.append(
                    f"Found matching options hash  {study_options_hash[:7]}, but incorrect study commit hash "
                    f"(needs: {study_commit_hash[:7]}, has: {entry_commit_hash[:7]})"
                )
        if has_been_run_with_these_options:
            [print(line) for line in semi_correct_hits]
            print(
                "No matching results were found for this study version, but results with these options were found for "
                "other study versions. Did you recently update the study?"
            )
        elif has_been_run_with_this_commit:
            [print(line) for line in semi_correct_hits]
            print(
                "No matching results were found for these options, but results with other options were found for "
                "this study versions. Did you recently change the options?"
            )
        else:
            print("No matching results were found for these options and study version.")
        return None

    def run_study(self, force=False):
        """Run specified study commands in the given repository."""
        if not force and self.is_running:
            print(f"{self.study.name} is currently running. Skipping...")
            return

        print(f"Running {self.name} in {self.study.path} with: {self.options}")
        if not self.options.debug:
            self.study.update()
        else:
            print("WARNING: Not updating the repositories while in debug mode.")

        if not force and self.has_results_for_this_run:
            print(f"{self.study.path} has already been computed with these options. Skipping...")
            return

        try:
            self.status = 'running'

            self.study.module.main(self.options, str(self.study.path))

            print("Command execution successful.")
            self.status = 'finished'

        except (KeyboardInterrupt, Exception) as e:
            traceback.print_exc()
            self.status = 'failed'
            return

    @property
    def _results_path(self):
        if self._results_branch is None:
            return None
        else:
            return self.study.path / (self.study._output_folder + "_cached") / self._results_branch

    def load(self, ):
        if self._results_branch is None or self.options.get_hash() != self._options_hash:
            self._results_branch = self._get_results_branch()
            self._options_hash = self.options.get_hash()

        if self._results_branch is None:
            print(f"No results available for Case({self.study.path, self.options.get_hash()[:7]})")
            return None

        if self._results_path.exists():
            return

        self.study.copy_data_to_cache(self._results_branch)

    @property
    def results_path(self):
        self.load()

        return self._results_path
