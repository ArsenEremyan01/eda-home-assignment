import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas


def get_visualize_comparison_of_spent_imp(dataset):
    region_metrics = dataset.groupby('region').agg({
        'user_spending': lambda x: round(x.sum(), 2),
        'impressions_count': 'sum'
    }).reset_index()
    region_metrics.sort_values(by='user_spending', ascending=False)
    plt.figure(figsize=(10, 6))
    plt.bar(region_metrics['region'], region_metrics['user_spending'], label='Spending by region')
    plt.bar(region_metrics['region'], region_metrics['impressions_count'], label='Impressions Count')
    plt.xlabel('Region')
    plt.ylabel('Value')
    plt.title('Comparison of Spent and Impressions Count by Region')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def get_visualize_impressions_by_us_state(dataset):
    states = geopandas.read_file('geopandas_data/usa-states-census-2014.shp')
    max_spending_by_region_ad_type = dataset.groupby(['region', 'adt'])['user_spending'].max().reset_index(
        name='spending')
    max_indices = max_spending_by_region_ad_type.groupby('region')['spending'].idxmax()
    result = max_spending_by_region_ad_type.loc[max_indices].reset_index(drop=True)

    merged_states = states.merge(result, left_on='STUSPS', right_on='region', how='left')
    fig, ax = plt.subplots(figsize=(25, 12))
    merged_states.plot(ax=ax, cmap='magma')
    for index, row in merged_states.iterrows():
        centroid = row['geometry'].centroid
        region = row['STUSPS']
        adt = row['adt']
        ax.annotate(f'{region}\n{adt}', (centroid.x, centroid.y), fontsize=7, color='white', ha='center', va='center')

    plt.title("Max Profitable Ad Type by U.S. State")
    plt.show()


def total_user_spending_per_ad_type(dataset):
    result = dataset[['adt', 'user_spending']].groupby(['adt']).sum('user_spending').sort_values(by='user_spending')
    plt.bar(result.index, result['user_spending'])
    plt.title("Spending for Each Type Across All Regions")
    plt.xlabel("Ad Type")
    plt.ylabel("Total User Spending")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def visualize_avg_imp_to_spending(dataset):
    dataset['impression_to_spending_ratio'] = dataset['impressions_count'] / dataset['user_spending']
    average_ratio_by_region = dataset.groupby('region')['impression_to_spending_ratio'].mean()
    plt.figure(figsize=(10, 6))
    average_ratio_by_region.plot(kind='bar')
    plt.xlabel('Region')
    plt.ylabel('Average Impression-to-Spending Ratio')
    plt.title('Average Impression-to-Spending Ratio by Region')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def get_avg_spend_by_os(dataset):
    average_spending_by_os = dataset.groupby('os')['user_spending'].mean()
    plt.figure(figsize=(12, 6))
    average_spending_by_os.sort_values().plot(kind='bar')
    plt.xlabel('Operating System')
    plt.ylabel('Average Spending')
    plt.title('Average Spending by Operating System')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
