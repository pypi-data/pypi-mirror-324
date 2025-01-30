"""Runmanager module.

This module contains the Runmanager class which is responsible for managing the 
runs of the experiment.
"""

import nkululeko.glob_conf as glob_conf
from nkululeko.modelrunner import Modelrunner
from nkululeko.reporting.reporter import Reporter
from nkululeko.utils.util import Util


class Runmanager:
    """Class to manage the runs of the experiment (e.g. when results differ caused by random initialization)."""

    model = None  # The underlying model
    df_train, df_test, feats_train, feats_test = (
        None,
        None,
        None,
        None,
    )  # The dataframes
    reports = []

    def __init__(self, df_train, df_test, feats_train, feats_test):
        """Constructor setting up the dataframes.

        Args:
            df_train: train dataframe
            df_test: test dataframe
            feats_train: train features
            feats_train: test features

        """
        self.df_train, self.df_test, self.feats_train, self.feats_test = (
            df_train,
            df_test,
            feats_train,
            feats_test,
        )
        self.util = Util("runmanager")
        self.target = glob_conf.config["DATA"]["target"]
        # intialize a new model
        # model_type = glob_conf.config['MODEL']['type']
        # self._select_model(model_type)

    def do_runs(self):
        """Start the runs."""
        self.best_results = []  # keep the best result per run
        self.last_epochs = []  # keep the epoch of best result per run
        # for all runs
        for run in range(int(self.util.config_val("EXP", "runs", 1))):
            self.util.debug(
                f"run {run} using model {glob_conf.config['MODEL']['type']}"
            )
            # set the run index as global variable for reporting
            self.util.set_config_val("EXP", "run", run)
            self.modelrunner = Modelrunner(
                self.df_train,
                self.df_test,
                self.feats_train,
                self.feats_test,
                run,
            )
            self.reports, last_epoch = self.modelrunner.do_epochs()
            # wrap up the run
            plot_anim_progression = self.util.config_val("PLOT", "anim_progression", 0)
            if plot_anim_progression:
                plot_name_suggest = self.util.get_exp_name()
                plot_name = (
                    self.util.config_val("PLOT", "name", plot_name_suggest)
                    + "_conf_anim.gif"
                )
                self.util.debug(f"plotting animated confusion to {plot_name}")
                self.reports[-1].make_conf_animation(plot_name)
            plot_epoch_progression = self.util.config_val(
                "PLOT", "epoch_progression", 0
            )
            try:
                epoch_num = int(glob_conf.config["EXP"]["epochs"])
            except KeyError:
                # possibly this value has not been set
                epoch_num = 1
            if epoch_num > 1 and plot_epoch_progression:
                plot_name_suggest = self.util.get_exp_name()
                plot_name = (
                    self.util.config_val("PLOT", "name", plot_name_suggest)
                    + "_epoch_progression"
                )
                self.util.debug(f"plotting progression to {plot_name}")
                self.reports[-1].plot_epoch_progression(self.reports, plot_name)
            # remember the best run
            best_report = self.get_best_result(self.reports)
            plot_best_model = self.util.config_val("PLOT", "best_model", False)

            if epoch_num > 1 and plot_best_model:
                plot_name_suggest = self.util.get_exp_name()
                plot_name = (
                    self.util.config_val("PLOT", "name", plot_name_suggest)
                    + f"_BEST_{best_report.run}_{best_report.epoch:03d}_BEST_cnf"
                )
                self.util.debug(
                    f"best result with run {best_report.run} and epoch"
                    f" {best_report.epoch}:"
                    f" {best_report.result.get_test_result()}"
                )
                self.print_model(best_report, plot_name)
            # finally, print out the numbers for this run
            best_report.print_results(best_report.epoch)
            best_report.print_probabilities()
            self.best_results.append(best_report)
            self.last_epochs.append(last_epoch)

    def print_best_result_runs(self):
        """Print the best result for all runs."""
        best_report = self.get_best_result(self.best_results)
        self.util.debug(
            f"best result all runs with run {best_report.run}             and"
            f" epoch {best_report.epoch}: {best_report.result.test:.3f}"
        )
        plot_name_suggest = self.util.get_exp_name()
        plot_name = (
            self.util.config_val("PLOT", "name", plot_name_suggest)
            + f"_BEST_{best_report.run}_{best_report.epoch:03d}_BEST_cnf"
        )
        self.print_model(best_report, plot_name)

    def print_given_result(self, run, epoch):
        """Print a result (confusion matrix) for a given epoch and run.

        Args:
            run: for which run
            epoch: for which epoch

        """
        report = Reporter([], [])
        report.set_id(run, epoch)
        self.util.debug(f"Re-testing result with run {run} and epoch {epoch}")
        plot_name_suggest = self.util.get_exp_name()
        plot_name = (
            self.util.config_val("PLOT", "name", plot_name_suggest)
            + f"_extra_{run}_{epoch:03d}_cnf"
        )
        self.print_model(report, plot_name)

    def print_model(self, reporter, plot_name):
        """Print a confusion matrix for a special report.

        Args:
            report: for which report (will be computed newly from model)
            plot_name: name of plot file
        """
        # self.load_model(report)
        # report = self.model.predict()
        self.util.debug(f"plotting conf matrix to {plot_name}")
        reporter.plot_confmatrix(plot_name)
        reporter.print_results()

    def load_model(self, report):
        """Load a model from disk for a specific run and epoch and evaluate it.

        Args:
            report: for which report (will be re-evaluated)

        """
        run = report.run
        epoch = report.epoch
        self.util.set_config_val("EXP", "run", run)
        model_type = glob_conf.config["MODEL"]["type"]
        model = self.modelrunner._select_model(model_type)
        model.load(run, epoch)
        return model

    def get_best_model(self):
        best_report = self.get_best_result(self.best_results)
        return self.load_model(best_report)

    def get_best_result(self, reports):
        best_r = Reporter([], [], None, 0, 0)
        if self.util.high_is_good():
            best_r = self.search_best_result(reports, "ascending")
        else:
            best_r = self.search_best_result(reports, "descending")
        return best_r

    def search_best_result(self, reports, order):
        best_r = Reporter([], [], None, 0, 0)
        if order == "ascending":
            best_result = 0
            for r in reports:
                res = r.result.test
                if res > best_result:
                    best_result = res
                    best_r = r
        else:
            best_result = 10000
            for r in reports:
                res = r.result.test
                if res < best_result:
                    best_result = res
                    best_r = r
        return best_r
