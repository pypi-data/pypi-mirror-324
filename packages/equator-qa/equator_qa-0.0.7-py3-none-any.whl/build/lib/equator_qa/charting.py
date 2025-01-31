import os               
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
from equator_qa.stats import load_all_llm_answers_from_json, get_llm_stats


# Mapping of model identifiers to more readable names
mapper = {
    'gpt-4-turbo-preview': 'GPT-4 Turbo',
    'gpt-4o': 'GPT-4o',
    'gpt-4o-mini-2024-07-18': 'GPT-4o Mini',
    'claude-3-opus-20240229': 'Claude 3 Opus',
    'claude-3-5-sonnet-20240620': 'Claude 3.5 Sonnet',
    'gemini-1_5-pro': 'Gemini 1.5 Pro',
    'gemini-1_0-pro': 'Gemini 1.0 Pro',
    'gemini-1_5-pro-exp-0801': 'Gemini 1.5 Pro Ex',
    'mistral-large-latest': 'Mistral Large 2',
    'open-mixtral-8x22b': 'Mistral 8x22B',
    'meta_llama3-70b-instruct-v1_0': 'Llama 3 70B',
    'meta_llama3-1-70b-instruct-v1_0': 'Llama 3.1 70B',
    'command-r': 'Command R',
    'command-r-plus': 'Command R Pro',
    'Meta-Llama-3-1-405B-Instruct-jjo_eastus_models_ai_azure_com': 'Llama 3.1 405B',
    'Meta-Llama-3-1-70B-Instruct-ostu_eastus_models_ai_azure_com': 'Llama 3.1 70B',
}


def define_data(final_stats: pd.DataFrame) -> pd.DataFrame:
    """
    Process and structure the final statistics DataFrame for visualization.

    This function maps model identifiers to readable names, adds a 
    "Human level*" entry, sorts the DataFrame based on mean scores, and 
    organizes the data into a format suitable for plotting.

    Parameters
    ----------
    final_stats : pd.DataFrame
        A DataFrame containing statistical metrics for each model, including
        columns like 'model', 'mean_score', 'ci_lower', and 'ci_upper'.

    Returns
    -------
    pd.DataFrame
        A structured DataFrame with columns:
            - "Model": Readable model names.
            - "Average": Mean scores of the models.
            - "Confidence Interval Low": Lower bound of the 95% confidence interval.
            - "Confidence Interval High": Upper bound of the 95% confidence interval.
    """
    # Map model identifiers to readable names
    final_stats['model'] = final_stats['model'].map(mapper).fillna(final_stats['model'])
    
    # Add a "Human level*" entry
    final_stats.loc[-1] = {
        'model': 'Human level*',
        'mean_score': 86,
        'std_dev_score': 0,
        'z_interval_error': 0,
        'ci_lower': 78,
        'ci_upper': 93,
    }
    
    # Sort the DataFrame by mean_score in descending order
    final_stats = final_stats.sort_values(by='mean_score', ascending=False)
    
    # Extract lists for plotting
    models = final_stats['model'].to_list()
    mean_scores = final_stats['mean_score'].to_list()
    lower_bounds = final_stats['ci_lower'].to_list()
    upper_bounds = final_stats['ci_upper'].to_list()
    
    # Organize data into a dictionary
    data = {
        "Model": models,
        "Average": mean_scores,
        "Confidence Interval Low": lower_bounds,
        "Confidence Interval High": upper_bounds,
    }
    
    return pd.DataFrame(data)


def create_performance_chart(
    final_stats: pd.DataFrame,
    title: str = "LLM Linguistic Benchmark Performance",
    highlight_models: list = None
) -> tuple[sns.axisgrid.FacetGrid, plt.Figure]:
    """
    Create a performance bar chart for LLMs with confidence intervals.

    This function generates a seaborn barplot displaying the average scores
    of various language models along with their confidence intervals. Specific
    models can be highlighted with different colors.

    Parameters
    ----------
    final_stats : pd.DataFrame
        A DataFrame containing the structured statistics for each model, 
        including "Model", "Average", "Confidence Interval Low", and 
        "Confidence Interval High".
    title : str, optional
        The title of the performance chart, by default "LLM Linguistic Benchmark Performance".
    highlight_models : list of str, optional
        A list of model names to highlight in the chart, by default None.

    Returns
    -------
    tuple[sns.axisgrid.FacetGrid, plt.Figure]
        A tuple containing the seaborn barplot object and the matplotlib figure.
    """
    if highlight_models is None:
        highlight_models = []

    # Prepare data for plotting
    df = define_data(final_stats)
    
    # Set the seaborn theme
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Assign colors based on whether the model is highlighted
    colors = ['skyblue' if model not in highlight_models else 'orange' for model in df["Model"]]
    
    # Create the barplot
    barplot = sns.barplot(data=df, x="Model", y="Average", palette=colors, errorbar=None)
    
    # Apply hatching to the "Human level*" bar
    for i, bar in enumerate(barplot.patches):
        if df["Model"][i] == "Human level*":
            bar.set_hatch('///')  # Apply hatching
    
    # Add confidence intervals as vertical lines with caps
    capwidth = 0.1  # Width of the cap lines
    for i, model in enumerate(df["Model"]):
        plt.plot(
            [i, i],
            [df["Confidence Interval Low"][i], df["Confidence Interval High"][i]],
            color='grey',
            lw=1
        )
        # Add horizontal caps at the ends of the confidence intervals
        plt.plot(
            [i - capwidth / 2, i + capwidth / 2],
            [df["Confidence Interval Low"][i], df["Confidence Interval Low"][i]],
            color='grey',
            lw=1
        )
        plt.plot(
            [i - capwidth / 2, i + capwidth / 2],
            [df["Confidence Interval High"][i], df["Confidence Interval High"][i]],
            color='grey',
            lw=1
        )
    
    # Set chart titles and labels
    plt.title(title, fontsize=18)
    plt.xlabel("", fontsize=14)
    plt.ylabel("Average Score (%)", fontsize=14)
    plt.xticks(rotation=60, fontsize=14)
    plt.tight_layout()
    
    return barplot, plt


def create_basic_charts(
    execution_steps: list,
    answer_rounds: int,
    benchmark_name: str,
    date_now: str
) -> None:
    """
    Generate and save various performance and token usage charts based on LLM statistics.

    This function orchestrates the creation of statistical analyses and visualizations
    for language models. It handles loading data, computing statistics, generating
    performance charts, and creating token usage comparisons.

    Parameters
    ----------
    execution_steps : list of str
        A list of steps to execute. If "generate_statistics" is included, the function proceeds to generate statistics and charts.
    answer_rounds : int
        The number of answer rounds to process.
    benchmark_name : str
        The name of the benchmark being evaluated.
    date_now : str
        The current date, used for naming folders and files.
    """
    if "generate_statistics" in execution_steps:
        # Define paths for saving outputs
        folder_name = f"{date_now}-{benchmark_name}"
        auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
        stats_save_path = f"./{folder_name}/tables_and_charts"
        sub_eval_folders = [f"/round_{r+1}" for r in range(answer_rounds)]
        
        print("2. GENERATING STATISTICS")
        all_stats_dfs = {}
        
        # Information for saving charts
        save_info = [
            {
                "path": auto_eval_save_path,
                "chart_title": "LLM Linguistic Benchmark Performance",
                "type": "",
            }
        ]
        
        for info in save_info:
            save_path = info["path"]
            chart_title = info["chart_title"]
            info_type = info["type"]
            
            print("Generating charts for path:", save_path)
            
            # Load all LLM evaluations
            all_llm_evals = load_all_llm_answers_from_json(
                save_path,
                prefix_replace="auto_eval-",
                sub_folders=sub_eval_folders,
            )
            
            # Compute statistics
            stats_df = get_llm_stats(
                all_llm_evals, stats_save_path, file_suffix=info_type, bootstrap_n=10000
            )
            
            # Display the statistics DataFrame
            display(stats_df)
            
            # Create and save the performance chart
            barplot, plt_obj = create_performance_chart(
                stats_df.reset_index(),
                chart_title,
                highlight_models=["o1-preview"],
            )
            barplot.figure.savefig(
                f"{stats_save_path}/performance_chart{info_type}.png"
            )
            plt_obj.show()
            
            # Store the statistics DataFrame
            all_stats_dfs[chart_title] = stats_df
            
            # Read data from the saved CSV file
            df = pd.read_csv(f'{stats_save_path}/final_stats.csv')
            
            # Sort the DataFrame by mean_score in descending order
            df_sorted = df.sort_values(by='mean_score', ascending=False)
            
            # Define a color palette
            colors = {
                'blue_200': '#90caf9',
                'yellow_600': '#fdd835',
                'pink_200': '#f48fb1',
                'cyan_200': '#80deea',
                'orange_400': '#ffa726',
                'deep_purple_A100': '#b388ff',
                'red_700': '#d32f2f'
            }
            
            # Horizontal Bar Chart for Mean Score, CI Lower, and CI Upper for Each Model
            y = np.arange(len(df_sorted['model']))  # Label locations
            height = 0.25  # Height of the bars
            
            fig, ax = plt.subplots(figsize=(14, 10))
            bars1 = ax.barh(y - height, df_sorted['mean_score'], height, label='Mean Score', color=colors['blue_200'])
            bars2 = ax.barh(y, df_sorted['ci_lower'], height, label='CI Lower', color=colors['yellow_600'])
            bars3 = ax.barh(y + height, df_sorted['ci_upper'], height, label='CI Upper', color=colors['cyan_200'])
            
            # Set labels and title
            ax.set_yticks(y)
            ax.set_yticklabels(df_sorted['model'])
            ax.set_xlabel('Scores')
            ax.set_title('Comparison of Mean Score, CI Lower, and CI Upper for Each Model')
            ax.invert_yaxis()  # Higher values at the top
            ax.legend()
            
            plt.tight_layout()
            plt.grid(axis='x', linestyle='--', alpha=0.5)
            plt.show()
            
            # Horizontal Bar Chart for Z Interval Error for Each Model
            fig, ax = plt.subplots(figsize=(14, 10))
            bars = ax.barh(df_sorted['model'], df_sorted['z_interval_error'], color=colors['pink_200'])
            
            plt.ylabel('Models')
            plt.xlabel('Z Interval Error')
            plt.title('Z Interval Error for Each Model')
            ax.invert_yaxis()  # Higher values at the top
            plt.tight_layout()
            plt.grid(axis='x', linestyle='--', alpha=0.5)
            plt.show()
            
            # Horizontal Bar Chart for Mean Score of Each Model
            fig, ax = plt.subplots(figsize=(14, 10))
            bars = ax.barh(df_sorted['model'], df_sorted['mean_score'], color=colors['orange_400'])
            
            plt.ylabel('Models')
            plt.xlabel('Mean Score')
            plt.title('Mean Score for Each Model')
            ax.invert_yaxis()  # Higher values at the top
            plt.tight_layout()
            plt.grid(axis='x', linestyle='--', alpha=0.5)
            plt.show()
            
            # Plotting Mean Score with Error Bars for Confidence Intervals
            ci_error = (df_sorted['ci_upper'] - df_sorted['ci_lower']).abs() / 2
            plt.figure(figsize=(14, 10))
            plt.errorbar(
                df_sorted['mean_score'], 
                df_sorted['model'], 
                xerr=ci_error, 
                fmt='o', 
                ecolor=colors['red_700'], 
                capsize=5, 
                label='Mean Score with CI'
            )
            plt.ylabel('Models')
            plt.xlabel('Mean Score')
            plt.title('Mean Score with Confidence Intervals for Various Models')
            plt.gca().invert_yaxis()  # Higher values at the top
            plt.tight_layout()
            plt.legend()
            plt.grid(axis='x', linestyle='--', alpha=0.5)
            plt.show()
            
            # Bar Chart of Standard Deviations for Each Model
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot standard deviation scores for each model
            ax.bar(df['model'], df['std_dev_score'], color='#90caf9', edgecolor='black')
            
            # Add labels and title
            plt.xticks(rotation=45, ha='right', fontsize=8)
            plt.xlabel('Model')
            plt.ylabel('Standard Deviation')
            plt.title('Standard Deviation for Each Model')
            plt.tight_layout()
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            
            plt.show()
        
        # Define the directory to save charts
        charts_dir = stats_save_path
        os.makedirs(charts_dir, exist_ok=True)
        
        # Inner functions for processing JSON files and counting tokens

        def collect_json_files(directory: str) -> list:
            """
            Collect all JSON file paths within a specified directory.

            Parameters
            ----------
            directory : str
                The directory path to search for JSON files.

            Returns
            -------
            list
                A list of full file paths to JSON files in the directory.
            """
            return [
                os.path.join(directory, file) 
                for file in os.listdir(directory) 
                if file.endswith('.json')
            ]

        def process_json_files(file_paths: list) -> list:
            """
            Process a list of JSON files to extract token counts.

            This function reads each JSON file, extracts relevant fields, 
            calculates token counts based on the text length, and aggregates 
            the results.

            Parameters
            ----------
            file_paths : list
                A list of file paths to JSON files to be processed.

            Returns
            -------
            list
                A list of dictionaries containing token counts for each category.
            """
            results = []
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for _, entry in data.items():
                    # Token calculation for each category
                    question_tokens = count_tokens(entry.get("question", ""))
                    human_answer_tokens = count_tokens(entry.get("human_answer", ""))
                    model_answer_input_tokens = count_tokens(entry.get("model_answer", ""))
                    eval_response_tokens = count_tokens(entry.get("eval_response", ""))
                    score_tokens = count_tokens(str(entry.get("score", "")))
                    bernard_evaluator_response_tokens = count_tokens(entry.get("bernard_evaluator_response", ""))
                    
                    results.append({
                        "question_tokens": question_tokens,
                        "human_answer_tokens": human_answer_tokens,
                        "model_answer_input_tokens": model_answer_input_tokens,
                        "eval_response_tokens": eval_response_tokens,
                        "score_tokens": score_tokens,
                        "bernard_evaluator_response_tokens": bernard_evaluator_response_tokens,
                        "total_tokens": (
                            question_tokens + 
                            human_answer_tokens + 
                            model_answer_input_tokens +
                            eval_response_tokens + 
                            score_tokens + 
                            bernard_evaluator_response_tokens
                        )
                    })
            return results

        def count_tokens(text: str) -> int:
            """
            Calculate the number of tokens in a text based on character count.

            The function assumes that 1 token is approximately equal to 4 characters.

            Parameters
            ----------
            text : str
                The text for which to count tokens.

            Returns
            -------
            int
                The estimated number of tokens in the text.
            """
            return max(1, len(text) // 4)

        # Process files for each round
        all_results = []

        for round_num in range(1, answer_rounds + 1):
            round_dir = os.path.join(auto_eval_save_path, f'round_{round_num}')
            
            # Collect JSON files from the current round
            json_files = collect_json_files(round_dir)

            # Process the JSON files and aggregate results
            all_results.extend(process_json_files(json_files))

            # Convert aggregated results to a DataFrame for analysis
            df = pd.DataFrame(all_results)

            # Summarize total tokens per category
            summary = df.sum()

            # Define categories for comparison
            categories = [
                "Question", 
                "Human Answer", 
                "Student Response", 
                "Eval Response", 
                "Score",  
                "Total"
            ]
            
            # Aggregate token usage per category
            token_usage = [
                summary["question_tokens"],
                summary["human_answer_tokens"],
                summary["model_answer_input_tokens"],
                summary["eval_response_tokens"],
                summary["score_tokens"],
                summary["total_tokens"]
            ]

            # Create a DataFrame for token usage comparison
            usage_df = pd.DataFrame({
                "Category": categories,
                "Token Usage": token_usage
            })

            # Save the token comparison table to a CSV file
            usage_csv_path = os.path.join(charts_dir, 'token_usage_comparison.csv')
            usage_df.to_csv(usage_csv_path, index=False)

            # Create a bar chart for token usage comparison
            x = np.arange(len(categories))
            width = 0.35  # Width of the bars

            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(x, token_usage, width, label="Token Usage", color="#4C72B0")

            # Add values above the bars
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, 
                    bar.get_height() + 5, 
                    f"{int(bar.get_height())}", 
                    ha="center", 
                    fontsize=10
                )

            # Adjust the y-axis dynamically
            max_value = max(token_usage)
            ax.set_ylim(0, max_value * 1.2)  # Add 20% headroom above the tallest bar

            # Add labels, title, and legend
            ax.set_ylabel("Token Count (Approx)", fontsize=12)
            ax.set_title("Token Usage Comparison for Question-Answer Pairs", fontsize=14)
            ax.set_xticks(x)
            ax.set_xticklabels(categories)
            ax.legend()

            # Save the chart as a PNG file
            chart_path = os.path.join(charts_dir, 'token_usage_comparison_chart.png')
            plt.savefig(chart_path, bbox_inches='tight')
            plt.show()
