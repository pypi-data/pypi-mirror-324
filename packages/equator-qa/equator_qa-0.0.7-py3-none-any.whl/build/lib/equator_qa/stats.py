import os
import pandas as pd
import numpy as np


def load_all_llm_answers_from_json(
    answers_save_path: str,
    prefix_replace: str = "auto-eval",
    sub_folders: list[str] = [""],
) -> dict[str, pd.DataFrame]:
    """
    Load all LLM answers from JSON files.

    This function traverses the specified directory and its subfolders,
    loads JSON files containing LLM answers, and aggregates them into a
    dictionary mapping each model to its corresponding DataFrame of answers.

    Parameters
    ----------
    answers_save_path : str
        The base path where answer JSON files are stored.
    prefix_replace : str, optional
        The prefix to remove from file names to extract model names,
        by default "auto-eval".
    sub_folders : list of str, optional
        A list of subfolder names to search within the base path,
        by default [""].

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary where keys are model names and values are DataFrames
        containing the answers for each model.
    """
    # Reload all the scored answers from JSON files
    all_llm_answers = {}
    for sub_folder in sub_folders:
        answers_save_path_sub = f"{answers_save_path}{sub_folder}"
        if not os.path.exists(answers_save_path_sub):
            continue
        for output_file in os.listdir(f"{answers_save_path_sub}/"):
            if output_file.endswith(".json"):
                outputs_df = pd.read_json(
                    f"{answers_save_path_sub}/{output_file}", orient="index"
                )
                model = output_file.replace(prefix_replace, "").replace(".json", "")
                all_llm_answers.setdefault(model, pd.DataFrame())
                all_llm_answers[model] = pd.concat([all_llm_answers[model], outputs_df])
    print("Test statistics, all answers", all_llm_answers)
    return all_llm_answers


def get_llm_stats(
    all_llm_answers: dict[str, pd.DataFrame],
    stats_save_path: str,
    file_suffix: str = "",
    bootstrap_n: int = 10000,
) -> pd.DataFrame:
    """
    Calculate and save LLM statistics.

    This function computes statistical metrics for each LLM based on the
    provided answers, saves the statistics to a CSV file, and returns
    a DataFrame containing the statistics.

    Parameters
    ----------
    all_llm_answers : dict[str, pd.DataFrame]
        A dictionary where keys are model names and values are DataFrames
        containing the answers for each model.
    stats_save_path : str
        The directory path where the statistics CSV file will be saved.
    file_suffix : str, optional
        An optional suffix to append to the statistics file name,
        by default "".
    bootstrap_n : int, optional
        The number of bootstrap samples to use for confidence interval
        calculation, by default 10000.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing statistical metrics for each model,
        sorted by mean score in descending order.
    """
    all_llm_stats = calculate_llm_stats(all_llm_answers, bootstrap_n)
    stats_df = (
        pd.DataFrame(all_llm_stats)
        .transpose()
        .sort_values("mean_score", ascending=False)
    )
    stats_df.index.name = "model"
    os.makedirs(stats_save_path, exist_ok=True)
    stats_df.to_csv(f"./{stats_save_path}/final_stats{file_suffix}.csv")
    return stats_df


def calculate_llm_stats(all_llm_answers: dict[str, pd.DataFrame], bootstrap_n: int = 10000) -> dict:
    """
    Calculate statistical metrics for each LLM.

    This function computes the mean score, standard deviation, z-interval
    error, and 95% confidence intervals for each model's scores using
    bootstrap sampling.

    Parameters
    ----------
    all_llm_answers : dict[str, pd.DataFrame]
        A dictionary where keys are model names and values are DataFrames
        containing the answers for each model.
    bootstrap_n : int, optional
        The number of bootstrap samples to use for confidence interval
        calculation, by default 10000.

    Returns
    -------
    dict
        A dictionary where each key is a model name and the value is another
        dictionary containing the following statistical metrics:
            - mean_score (float): The mean of the scores.
            - std_dev_score (float): The standard deviation of the scores.
            - z_interval_error (float): The z-interval error for 95% confidence.
            - ci_lower (float): The lower bound of the 95% confidence interval.
            - ci_upper (float): The upper bound of the 95% confidence interval.
            - output_count (int): The number of outputs/scores.
    """
    all_llm_stats = {}
    for model, outputs in all_llm_answers.items():
        print(f"Calculating stats for {model}")
        mean_score = outputs["score"].mean()
        std_dev_score = outputs["score"].std()
        # Perform bootstrap sampling to get the 95% confidence interval
        bootstrap_scores = []
        for _ in range(bootstrap_n):
            bootstrap_scores.append(
                outputs["score"].sample(frac=1, replace=True).mean()
            )
        ci_lower = np.percentile(bootstrap_scores, 2.5)
        ci_upper = np.percentile(bootstrap_scores, 97.5)
        # Calculate z-interval error for 95% confidence
        z = 1.96
        z_interval_error = z * (std_dev_score / np.sqrt(len(outputs)))
        all_llm_stats[model] = {
            "mean_score": mean_score,
            "std_dev_score": std_dev_score,
            "z_interval_error": z_interval_error,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "output_count": len(outputs),
        }
    return all_llm_stats

