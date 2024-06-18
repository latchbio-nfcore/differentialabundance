from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, contrasts: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], matrix: typing.Optional[LatchFile], transcript_length_matrix: typing.Optional[str], observations_name_col: typing.Optional[str], sizefactors_from_controls: typing.Optional[bool], control_features: typing.Optional[LatchFile], features: typing.Optional[str], affy_destructive: typing.Optional[bool], affy_rm_mask: typing.Optional[bool], affy_rm_outliers: typing.Optional[bool], affy_rm_extra: typing.Optional[bool], filtering_min_proportion: typing.Optional[float], filtering_grouping_var: typing.Optional[str], filtering_min_samples_not_na: typing.Optional[float], exploratory_log2_assays: typing.Optional[str], differential_file_suffix: typing.Optional[str], differential_subset_to_contrast_samples: typing.Optional[bool], deseq2_use_t: typing.Optional[bool], limma_ndups: typing.Optional[float], limma_trend: typing.Optional[bool], limma_robust: typing.Optional[bool], limma_confint: typing.Optional[bool], gsea_run: typing.Optional[bool], gsea_median: typing.Optional[bool], gsea_save_rnd_lists: typing.Optional[bool], gsea_zip_report: typing.Optional[bool], gprofiler2_run: typing.Optional[bool], gprofiler2_organism: typing.Optional[str], gprofiler2_correction_method: typing.Optional[str], gprofiler2_sources: typing.Optional[str], gprofiler2_token: typing.Optional[str], gprofiler2_background_file: typing.Optional[str], gprofiler2_background_column: typing.Optional[str], shinyngs_deploy_to_shinyapps_io: typing.Optional[bool], report_file: LatchFile, email: typing.Optional[str], report_contributors: typing.Optional[str], genome: typing.Optional[str], gtf: typing.Optional[LatchFile], email_on_fail: typing.Optional[str], study_name: str, study_type: str, study_abundance_type: str, affy_cel_files_archive: typing.Optional[str], querygse: typing.Optional[str], observations_id_col: str, observations_type: str, features_id_col: str, features_name_col: str, features_type: str, features_metadata_cols: typing.Optional[str], features_gtf_feature_type: typing.Optional[str], features_gtf_table_first_field: typing.Optional[str], affy_file_name_col: typing.Optional[str], affy_background: typing.Optional[bool], affy_bgversion: typing.Optional[int], affy_cdfname: typing.Optional[str], affy_build_annotation: typing.Optional[bool], proteus_measurecol_prefix: typing.Optional[str], proteus_norm_function: typing.Optional[str], proteus_plotsd_method: typing.Optional[str], proteus_plotmv_loess: typing.Optional[bool], proteus_palette_name: typing.Optional[str], filtering_min_abundance: float, filtering_min_samples: typing.Optional[float], filtering_min_proportion_not_na: typing.Optional[float], exploratory_clustering_method: str, exploratory_cor_method: str, exploratory_n_features: int, exploratory_whisker_distance: typing.Optional[float], exploratory_mad_threshold: typing.Optional[int], exploratory_main_variable: str, exploratory_palette_name: str, differential_feature_id_column: str, differential_fc_column: str, differential_pval_column: typing.Optional[str], differential_qval_column: str, differential_min_fold_change: float, differential_max_pval: float, differential_max_qval: float, differential_feature_name_column: typing.Optional[str], differential_foldchanges_logged: typing.Optional[bool], differential_palette_name: str, deseq2_test: typing.Optional[str], deseq2_fit_type: typing.Optional[str], deseq2_sf_type: typing.Optional[str], deseq2_min_replicates_for_replace: typing.Optional[int], deseq2_independent_filtering: typing.Optional[bool], deseq2_lfc_threshold: typing.Optional[int], deseq2_alt_hypothesis: typing.Optional[str], deseq2_p_adjust_method: typing.Optional[str], deseq2_alpha: typing.Optional[float], deseq2_minmu: typing.Optional[float], deseq2_vs_method: typing.Optional[str], deseq2_shrink_lfc: typing.Optional[bool], deseq2_cores: typing.Optional[int], deseq2_vs_blind: typing.Optional[bool], deseq2_vst_nsub: typing.Optional[int], limma_spacing: typing.Optional[str], limma_block: typing.Optional[str], limma_correlation: typing.Optional[str], limma_method: typing.Optional[str], limma_proportion: typing.Optional[float], limma_stdev_coef_lim: typing.Optional[str], limma_winsor_tail_p: typing.Optional[str], limma_lfc: typing.Optional[int], limma_adjust_method: typing.Optional[str], limma_p_value: typing.Optional[float], gsea_permute: typing.Optional[str], gsea_nperm: typing.Optional[int], gsea_scoring_scheme: typing.Optional[str], gsea_metric: typing.Optional[str], gsea_sort: typing.Optional[str], gsea_order: typing.Optional[str], gsea_set_max: typing.Optional[int], gsea_set_min: typing.Optional[int], gsea_norm: typing.Optional[str], gsea_rnd_type: typing.Optional[str], gsea_make_sets: typing.Optional[bool], gsea_num: typing.Optional[int], gsea_plot_top_x: typing.Optional[int], gsea_rnd_seed: typing.Optional[str], gprofiler2_significant: typing.Optional[bool], gprofiler2_measure_underrepresentation: typing.Optional[bool], gprofiler2_evcodes: typing.Optional[bool], gprofiler2_max_qval: typing.Optional[float], gprofiler2_domain_scope: typing.Optional[str], gprofiler2_min_diff: typing.Optional[int], gprofiler2_palette_name: typing.Optional[str], shinyngs_build_app: typing.Optional[bool], shinyngs_shinyapps_account: typing.Optional[str], shinyngs_shinyapps_app_name: typing.Optional[str], shinyngs_guess_unlog_matrices: typing.Optional[bool], gene_sets_files: typing.Optional[str], logo_file: str, css_file: str, citations_file: typing.Optional[str], report_title: typing.Optional[str], report_author: typing.Optional[str], report_description: typing.Optional[str], report_scree: typing.Optional[bool], report_round_digits: typing.Optional[int], publish_dir_mode: typing.Optional[str], validate_params: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('study_name', study_name),
                *get_flag('study_type', study_type),
                *get_flag('input', input),
                *get_flag('contrasts', contrasts),
                *get_flag('outdir', outdir),
                *get_flag('study_abundance_type', study_abundance_type),
                *get_flag('matrix', matrix),
                *get_flag('transcript_length_matrix', transcript_length_matrix),
                *get_flag('affy_cel_files_archive', affy_cel_files_archive),
                *get_flag('querygse', querygse),
                *get_flag('observations_id_col', observations_id_col),
                *get_flag('observations_type', observations_type),
                *get_flag('observations_name_col', observations_name_col),
                *get_flag('features_id_col', features_id_col),
                *get_flag('features_name_col', features_name_col),
                *get_flag('features_type', features_type),
                *get_flag('sizefactors_from_controls', sizefactors_from_controls),
                *get_flag('control_features', control_features),
                *get_flag('features_metadata_cols', features_metadata_cols),
                *get_flag('features', features),
                *get_flag('features_gtf_feature_type', features_gtf_feature_type),
                *get_flag('features_gtf_table_first_field', features_gtf_table_first_field),
                *get_flag('affy_file_name_col', affy_file_name_col),
                *get_flag('affy_background', affy_background),
                *get_flag('affy_bgversion', affy_bgversion),
                *get_flag('affy_destructive', affy_destructive),
                *get_flag('affy_cdfname', affy_cdfname),
                *get_flag('affy_build_annotation', affy_build_annotation),
                *get_flag('affy_rm_mask', affy_rm_mask),
                *get_flag('affy_rm_outliers', affy_rm_outliers),
                *get_flag('affy_rm_extra', affy_rm_extra),
                *get_flag('proteus_measurecol_prefix', proteus_measurecol_prefix),
                *get_flag('proteus_norm_function', proteus_norm_function),
                *get_flag('proteus_plotsd_method', proteus_plotsd_method),
                *get_flag('proteus_plotmv_loess', proteus_plotmv_loess),
                *get_flag('proteus_palette_name', proteus_palette_name),
                *get_flag('filtering_min_abundance', filtering_min_abundance),
                *get_flag('filtering_min_samples', filtering_min_samples),
                *get_flag('filtering_min_proportion', filtering_min_proportion),
                *get_flag('filtering_grouping_var', filtering_grouping_var),
                *get_flag('filtering_min_proportion_not_na', filtering_min_proportion_not_na),
                *get_flag('filtering_min_samples_not_na', filtering_min_samples_not_na),
                *get_flag('exploratory_clustering_method', exploratory_clustering_method),
                *get_flag('exploratory_cor_method', exploratory_cor_method),
                *get_flag('exploratory_n_features', exploratory_n_features),
                *get_flag('exploratory_whisker_distance', exploratory_whisker_distance),
                *get_flag('exploratory_mad_threshold', exploratory_mad_threshold),
                *get_flag('exploratory_main_variable', exploratory_main_variable),
                *get_flag('exploratory_log2_assays', exploratory_log2_assays),
                *get_flag('exploratory_palette_name', exploratory_palette_name),
                *get_flag('differential_file_suffix', differential_file_suffix),
                *get_flag('differential_feature_id_column', differential_feature_id_column),
                *get_flag('differential_fc_column', differential_fc_column),
                *get_flag('differential_pval_column', differential_pval_column),
                *get_flag('differential_qval_column', differential_qval_column),
                *get_flag('differential_min_fold_change', differential_min_fold_change),
                *get_flag('differential_max_pval', differential_max_pval),
                *get_flag('differential_max_qval', differential_max_qval),
                *get_flag('differential_feature_name_column', differential_feature_name_column),
                *get_flag('differential_foldchanges_logged', differential_foldchanges_logged),
                *get_flag('differential_palette_name', differential_palette_name),
                *get_flag('differential_subset_to_contrast_samples', differential_subset_to_contrast_samples),
                *get_flag('deseq2_test', deseq2_test),
                *get_flag('deseq2_fit_type', deseq2_fit_type),
                *get_flag('deseq2_sf_type', deseq2_sf_type),
                *get_flag('deseq2_min_replicates_for_replace', deseq2_min_replicates_for_replace),
                *get_flag('deseq2_use_t', deseq2_use_t),
                *get_flag('deseq2_independent_filtering', deseq2_independent_filtering),
                *get_flag('deseq2_lfc_threshold', deseq2_lfc_threshold),
                *get_flag('deseq2_alt_hypothesis', deseq2_alt_hypothesis),
                *get_flag('deseq2_p_adjust_method', deseq2_p_adjust_method),
                *get_flag('deseq2_alpha', deseq2_alpha),
                *get_flag('deseq2_minmu', deseq2_minmu),
                *get_flag('deseq2_vs_method', deseq2_vs_method),
                *get_flag('deseq2_shrink_lfc', deseq2_shrink_lfc),
                *get_flag('deseq2_cores', deseq2_cores),
                *get_flag('deseq2_vs_blind', deseq2_vs_blind),
                *get_flag('deseq2_vst_nsub', deseq2_vst_nsub),
                *get_flag('limma_ndups', limma_ndups),
                *get_flag('limma_spacing', limma_spacing),
                *get_flag('limma_block', limma_block),
                *get_flag('limma_correlation', limma_correlation),
                *get_flag('limma_method', limma_method),
                *get_flag('limma_proportion', limma_proportion),
                *get_flag('limma_trend', limma_trend),
                *get_flag('limma_robust', limma_robust),
                *get_flag('limma_stdev_coef_lim', limma_stdev_coef_lim),
                *get_flag('limma_winsor_tail_p', limma_winsor_tail_p),
                *get_flag('limma_lfc', limma_lfc),
                *get_flag('limma_confint', limma_confint),
                *get_flag('limma_adjust_method', limma_adjust_method),
                *get_flag('limma_p_value', limma_p_value),
                *get_flag('gsea_run', gsea_run),
                *get_flag('gsea_permute', gsea_permute),
                *get_flag('gsea_nperm', gsea_nperm),
                *get_flag('gsea_scoring_scheme', gsea_scoring_scheme),
                *get_flag('gsea_metric', gsea_metric),
                *get_flag('gsea_sort', gsea_sort),
                *get_flag('gsea_order', gsea_order),
                *get_flag('gsea_set_max', gsea_set_max),
                *get_flag('gsea_set_min', gsea_set_min),
                *get_flag('gsea_norm', gsea_norm),
                *get_flag('gsea_rnd_type', gsea_rnd_type),
                *get_flag('gsea_make_sets', gsea_make_sets),
                *get_flag('gsea_median', gsea_median),
                *get_flag('gsea_num', gsea_num),
                *get_flag('gsea_plot_top_x', gsea_plot_top_x),
                *get_flag('gsea_rnd_seed', gsea_rnd_seed),
                *get_flag('gsea_save_rnd_lists', gsea_save_rnd_lists),
                *get_flag('gsea_zip_report', gsea_zip_report),
                *get_flag('gprofiler2_run', gprofiler2_run),
                *get_flag('gprofiler2_organism', gprofiler2_organism),
                *get_flag('gprofiler2_significant', gprofiler2_significant),
                *get_flag('gprofiler2_measure_underrepresentation', gprofiler2_measure_underrepresentation),
                *get_flag('gprofiler2_correction_method', gprofiler2_correction_method),
                *get_flag('gprofiler2_sources', gprofiler2_sources),
                *get_flag('gprofiler2_evcodes', gprofiler2_evcodes),
                *get_flag('gprofiler2_max_qval', gprofiler2_max_qval),
                *get_flag('gprofiler2_token', gprofiler2_token),
                *get_flag('gprofiler2_background_file', gprofiler2_background_file),
                *get_flag('gprofiler2_background_column', gprofiler2_background_column),
                *get_flag('gprofiler2_domain_scope', gprofiler2_domain_scope),
                *get_flag('gprofiler2_min_diff', gprofiler2_min_diff),
                *get_flag('gprofiler2_palette_name', gprofiler2_palette_name),
                *get_flag('shinyngs_build_app', shinyngs_build_app),
                *get_flag('shinyngs_deploy_to_shinyapps_io', shinyngs_deploy_to_shinyapps_io),
                *get_flag('shinyngs_shinyapps_account', shinyngs_shinyapps_account),
                *get_flag('shinyngs_shinyapps_app_name', shinyngs_shinyapps_app_name),
                *get_flag('shinyngs_guess_unlog_matrices', shinyngs_guess_unlog_matrices),
                *get_flag('gene_sets_files', gene_sets_files),
                *get_flag('report_file', report_file),
                *get_flag('email', email),
                *get_flag('logo_file', logo_file),
                *get_flag('css_file', css_file),
                *get_flag('citations_file', citations_file),
                *get_flag('report_title', report_title),
                *get_flag('report_author', report_author),
                *get_flag('report_contributors', report_contributors),
                *get_flag('report_description', report_description),
                *get_flag('report_scree', report_scree),
                *get_flag('report_round_digits', report_round_digits),
                *get_flag('genome', genome),
                *get_flag('gtf', gtf),
                *get_flag('publish_dir_mode', publish_dir_mode),
                *get_flag('email_on_fail', email_on_fail),
                *get_flag('validate_params', validate_params)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_differentialabundance", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_differentialabundance(input: LatchFile, contrasts: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], matrix: typing.Optional[LatchFile], transcript_length_matrix: typing.Optional[str], observations_name_col: typing.Optional[str], sizefactors_from_controls: typing.Optional[bool], control_features: typing.Optional[LatchFile], features: typing.Optional[str], affy_destructive: typing.Optional[bool], affy_rm_mask: typing.Optional[bool], affy_rm_outliers: typing.Optional[bool], affy_rm_extra: typing.Optional[bool], filtering_min_proportion: typing.Optional[float], filtering_grouping_var: typing.Optional[str], filtering_min_samples_not_na: typing.Optional[float], exploratory_log2_assays: typing.Optional[str], differential_file_suffix: typing.Optional[str], differential_subset_to_contrast_samples: typing.Optional[bool], deseq2_use_t: typing.Optional[bool], limma_ndups: typing.Optional[float], limma_trend: typing.Optional[bool], limma_robust: typing.Optional[bool], limma_confint: typing.Optional[bool], gsea_run: typing.Optional[bool], gsea_median: typing.Optional[bool], gsea_save_rnd_lists: typing.Optional[bool], gsea_zip_report: typing.Optional[bool], gprofiler2_run: typing.Optional[bool], gprofiler2_organism: typing.Optional[str], gprofiler2_correction_method: typing.Optional[str], gprofiler2_sources: typing.Optional[str], gprofiler2_token: typing.Optional[str], gprofiler2_background_file: typing.Optional[str], gprofiler2_background_column: typing.Optional[str], shinyngs_deploy_to_shinyapps_io: typing.Optional[bool], report_file: LatchFile, email: typing.Optional[str], report_contributors: typing.Optional[str], genome: typing.Optional[str], gtf: typing.Optional[LatchFile], email_on_fail: typing.Optional[str], study_name: str = 'study', study_type: str = 'rnaseq', study_abundance_type: str = 'counts', affy_cel_files_archive: typing.Optional[str] = 'null', querygse: typing.Optional[str] = 'null', observations_id_col: str = 'sample', observations_type: str = 'sample', features_id_col: str = 'gene_id', features_name_col: str = 'gene_name', features_type: str = 'gene', features_metadata_cols: typing.Optional[str] = 'gene_id,gene_name,gene_biotype', features_gtf_feature_type: typing.Optional[str] = 'transcript', features_gtf_table_first_field: typing.Optional[str] = 'gene_id', affy_file_name_col: typing.Optional[str] = 'file', affy_background: typing.Optional[bool] = True, affy_bgversion: typing.Optional[int] = 2, affy_cdfname: typing.Optional[str] = 'null', affy_build_annotation: typing.Optional[bool] = True, proteus_measurecol_prefix: typing.Optional[str] = 'LFQ intensity', proteus_norm_function: typing.Optional[str] = 'normalizeMedian', proteus_plotsd_method: typing.Optional[str] = 'violin', proteus_plotmv_loess: typing.Optional[bool] = True, proteus_palette_name: typing.Optional[str] = 'Set1', filtering_min_abundance: float = 1.0, filtering_min_samples: typing.Optional[float] = 1.0, filtering_min_proportion_not_na: typing.Optional[float] = 0.5, exploratory_clustering_method: str = 'ward.D2', exploratory_cor_method: str = 'spearman', exploratory_n_features: int = 500, exploratory_whisker_distance: typing.Optional[float] = 1.5, exploratory_mad_threshold: typing.Optional[int] = -5, exploratory_main_variable: str = 'auto_pca', exploratory_palette_name: str = 'Set1', differential_feature_id_column: str = 'gene_id', differential_fc_column: str = 'log2FoldChange', differential_pval_column: typing.Optional[str] = 'pvalue', differential_qval_column: str = 'padj', differential_min_fold_change: float = 2.0, differential_max_pval: float = 1.0, differential_max_qval: float = 0.05, differential_feature_name_column: typing.Optional[str] = 'gene_name', differential_foldchanges_logged: typing.Optional[bool] = True, differential_palette_name: str = 'Set1', deseq2_test: typing.Optional[str] = 'Wald', deseq2_fit_type: typing.Optional[str] = 'parametric', deseq2_sf_type: typing.Optional[str] = 'ratio', deseq2_min_replicates_for_replace: typing.Optional[int] = 7, deseq2_independent_filtering: typing.Optional[bool] = True, deseq2_lfc_threshold: typing.Optional[int] = 0, deseq2_alt_hypothesis: typing.Optional[str] = 'greaterAbs', deseq2_p_adjust_method: typing.Optional[str] = 'BH', deseq2_alpha: typing.Optional[float] = 0.1, deseq2_minmu: typing.Optional[float] = 0.5, deseq2_vs_method: typing.Optional[str] = 'vst', deseq2_shrink_lfc: typing.Optional[bool] = True, deseq2_cores: typing.Optional[int] = 1, deseq2_vs_blind: typing.Optional[bool] = True, deseq2_vst_nsub: typing.Optional[int] = 1000, limma_spacing: typing.Optional[str] = 'null', limma_block: typing.Optional[str] = 'null', limma_correlation: typing.Optional[str] = 'null', limma_method: typing.Optional[str] = 'ls', limma_proportion: typing.Optional[float] = 0.01, limma_stdev_coef_lim: typing.Optional[str] = '0.1,4', limma_winsor_tail_p: typing.Optional[str] = '0.05,0.1', limma_lfc: typing.Optional[int] = 0, limma_adjust_method: typing.Optional[str] = 'BH', limma_p_value: typing.Optional[float] = 1.0, gsea_permute: typing.Optional[str] = 'phenotype', gsea_nperm: typing.Optional[int] = 1000, gsea_scoring_scheme: typing.Optional[str] = 'weighted', gsea_metric: typing.Optional[str] = 'Signal2Noise', gsea_sort: typing.Optional[str] = 'real', gsea_order: typing.Optional[str] = 'descending', gsea_set_max: typing.Optional[int] = 500, gsea_set_min: typing.Optional[int] = 15, gsea_norm: typing.Optional[str] = 'meandiv', gsea_rnd_type: typing.Optional[str] = 'no_balance', gsea_make_sets: typing.Optional[bool] = True, gsea_num: typing.Optional[int] = 100, gsea_plot_top_x: typing.Optional[int] = 20, gsea_rnd_seed: typing.Optional[str] = 'timestamp', gprofiler2_significant: typing.Optional[bool] = True, gprofiler2_measure_underrepresentation: typing.Optional[bool] = False, gprofiler2_evcodes: typing.Optional[bool] = False, gprofiler2_max_qval: typing.Optional[float] = 0.05, gprofiler2_domain_scope: typing.Optional[str] = 'annotated', gprofiler2_min_diff: typing.Optional[int] = 1, gprofiler2_palette_name: typing.Optional[str] = 'Blues', shinyngs_build_app: typing.Optional[bool] = True, shinyngs_shinyapps_account: typing.Optional[str] = 'null', shinyngs_shinyapps_app_name: typing.Optional[str] = 'null', shinyngs_guess_unlog_matrices: typing.Optional[bool] = True, gene_sets_files: typing.Optional[str] = 'null', logo_file: str = '${projectDir}/docs/images/nf-core-differentialabundance_logo_light.png', css_file: str = '${projectDir}/assets/nf-core_style.css', citations_file: typing.Optional[str] = '${projectDir}/CITATIONS.md', report_title: typing.Optional[str] = 'null', report_author: typing.Optional[str] = 'null', report_description: typing.Optional[str] = 'null', report_scree: typing.Optional[bool] = True, report_round_digits: typing.Optional[int] = 4, publish_dir_mode: typing.Optional[str] = 'copy', validate_params: typing.Optional[bool] = True) -> None:
    """
    nf-core/differentialabundance

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, study_name=study_name, study_type=study_type, input=input, contrasts=contrasts, outdir=outdir, study_abundance_type=study_abundance_type, matrix=matrix, transcript_length_matrix=transcript_length_matrix, affy_cel_files_archive=affy_cel_files_archive, querygse=querygse, observations_id_col=observations_id_col, observations_type=observations_type, observations_name_col=observations_name_col, features_id_col=features_id_col, features_name_col=features_name_col, features_type=features_type, sizefactors_from_controls=sizefactors_from_controls, control_features=control_features, features_metadata_cols=features_metadata_cols, features=features, features_gtf_feature_type=features_gtf_feature_type, features_gtf_table_first_field=features_gtf_table_first_field, affy_file_name_col=affy_file_name_col, affy_background=affy_background, affy_bgversion=affy_bgversion, affy_destructive=affy_destructive, affy_cdfname=affy_cdfname, affy_build_annotation=affy_build_annotation, affy_rm_mask=affy_rm_mask, affy_rm_outliers=affy_rm_outliers, affy_rm_extra=affy_rm_extra, proteus_measurecol_prefix=proteus_measurecol_prefix, proteus_norm_function=proteus_norm_function, proteus_plotsd_method=proteus_plotsd_method, proteus_plotmv_loess=proteus_plotmv_loess, proteus_palette_name=proteus_palette_name, filtering_min_abundance=filtering_min_abundance, filtering_min_samples=filtering_min_samples, filtering_min_proportion=filtering_min_proportion, filtering_grouping_var=filtering_grouping_var, filtering_min_proportion_not_na=filtering_min_proportion_not_na, filtering_min_samples_not_na=filtering_min_samples_not_na, exploratory_clustering_method=exploratory_clustering_method, exploratory_cor_method=exploratory_cor_method, exploratory_n_features=exploratory_n_features, exploratory_whisker_distance=exploratory_whisker_distance, exploratory_mad_threshold=exploratory_mad_threshold, exploratory_main_variable=exploratory_main_variable, exploratory_log2_assays=exploratory_log2_assays, exploratory_palette_name=exploratory_palette_name, differential_file_suffix=differential_file_suffix, differential_feature_id_column=differential_feature_id_column, differential_fc_column=differential_fc_column, differential_pval_column=differential_pval_column, differential_qval_column=differential_qval_column, differential_min_fold_change=differential_min_fold_change, differential_max_pval=differential_max_pval, differential_max_qval=differential_max_qval, differential_feature_name_column=differential_feature_name_column, differential_foldchanges_logged=differential_foldchanges_logged, differential_palette_name=differential_palette_name, differential_subset_to_contrast_samples=differential_subset_to_contrast_samples, deseq2_test=deseq2_test, deseq2_fit_type=deseq2_fit_type, deseq2_sf_type=deseq2_sf_type, deseq2_min_replicates_for_replace=deseq2_min_replicates_for_replace, deseq2_use_t=deseq2_use_t, deseq2_independent_filtering=deseq2_independent_filtering, deseq2_lfc_threshold=deseq2_lfc_threshold, deseq2_alt_hypothesis=deseq2_alt_hypothesis, deseq2_p_adjust_method=deseq2_p_adjust_method, deseq2_alpha=deseq2_alpha, deseq2_minmu=deseq2_minmu, deseq2_vs_method=deseq2_vs_method, deseq2_shrink_lfc=deseq2_shrink_lfc, deseq2_cores=deseq2_cores, deseq2_vs_blind=deseq2_vs_blind, deseq2_vst_nsub=deseq2_vst_nsub, limma_ndups=limma_ndups, limma_spacing=limma_spacing, limma_block=limma_block, limma_correlation=limma_correlation, limma_method=limma_method, limma_proportion=limma_proportion, limma_trend=limma_trend, limma_robust=limma_robust, limma_stdev_coef_lim=limma_stdev_coef_lim, limma_winsor_tail_p=limma_winsor_tail_p, limma_lfc=limma_lfc, limma_confint=limma_confint, limma_adjust_method=limma_adjust_method, limma_p_value=limma_p_value, gsea_run=gsea_run, gsea_permute=gsea_permute, gsea_nperm=gsea_nperm, gsea_scoring_scheme=gsea_scoring_scheme, gsea_metric=gsea_metric, gsea_sort=gsea_sort, gsea_order=gsea_order, gsea_set_max=gsea_set_max, gsea_set_min=gsea_set_min, gsea_norm=gsea_norm, gsea_rnd_type=gsea_rnd_type, gsea_make_sets=gsea_make_sets, gsea_median=gsea_median, gsea_num=gsea_num, gsea_plot_top_x=gsea_plot_top_x, gsea_rnd_seed=gsea_rnd_seed, gsea_save_rnd_lists=gsea_save_rnd_lists, gsea_zip_report=gsea_zip_report, gprofiler2_run=gprofiler2_run, gprofiler2_organism=gprofiler2_organism, gprofiler2_significant=gprofiler2_significant, gprofiler2_measure_underrepresentation=gprofiler2_measure_underrepresentation, gprofiler2_correction_method=gprofiler2_correction_method, gprofiler2_sources=gprofiler2_sources, gprofiler2_evcodes=gprofiler2_evcodes, gprofiler2_max_qval=gprofiler2_max_qval, gprofiler2_token=gprofiler2_token, gprofiler2_background_file=gprofiler2_background_file, gprofiler2_background_column=gprofiler2_background_column, gprofiler2_domain_scope=gprofiler2_domain_scope, gprofiler2_min_diff=gprofiler2_min_diff, gprofiler2_palette_name=gprofiler2_palette_name, shinyngs_build_app=shinyngs_build_app, shinyngs_deploy_to_shinyapps_io=shinyngs_deploy_to_shinyapps_io, shinyngs_shinyapps_account=shinyngs_shinyapps_account, shinyngs_shinyapps_app_name=shinyngs_shinyapps_app_name, shinyngs_guess_unlog_matrices=shinyngs_guess_unlog_matrices, gene_sets_files=gene_sets_files, report_file=report_file, email=email, logo_file=logo_file, css_file=css_file, citations_file=citations_file, report_title=report_title, report_author=report_author, report_contributors=report_contributors, report_description=report_description, report_scree=report_scree, report_round_digits=report_round_digits, genome=genome, gtf=gtf, publish_dir_mode=publish_dir_mode, email_on_fail=email_on_fail, validate_params=validate_params)

