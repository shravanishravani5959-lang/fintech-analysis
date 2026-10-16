"""
Project Title: FinTech Campaign Performance & Attribution Dashboard
Description: Simulates multi-channel fintech marketing data, calculates key ROI 
             and conversion metrics, and optimizes marketing budget allocation.
Author: Shravani Pendyala
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_campaign_data(num_records=10000, random_state=42):
  """Simulates multi-channel user acquisition and transactional campaign logs."""
  np.random.seed(random_state)

  channels = ['Email', 'Paid Social', 'Organic Search', 'Referral', 'Display']
  campaigns = ['Welcome_Offer_Q1', 'Retargeting_V2', 'Brand_Awareness', 'App_Launch']

  data = {
      'user_id': [f'USR_{i:05d}' for i in range(num_records)],
      'channel': np.random.choice(channels, num_records, p=[0.3, 0.3, 0.2, 0.1, 0.1]),
      'campaign_name': np.random.choice(campaigns, num_records),
      'impressions': np.random.randint(100, 5000, num_records),
      'clicks': np.random.randint(10, 500, num_records),
      'spend': np.round(np.random.uniform(5.0, 150.0, num_records), 2),
      'conversions': np.random.choice([0, 1], num_records, p=[0.75, 0.25]),
  }

  df = pd.DataFrame(data)
  # Ensure clicks do not exceed impressions
  df['clicks'] = df[['impressions', 'clicks']].min(axis=1)
  # Simulated customer lifetime value (LTV) for converted users
  df['revenue'] = df['conversions'] * np.round(
      np.random.uniform(50.0, 300.0, num_records), 2
  )

  return df


def analyze_channel_performance(df):
  """Aggregates metrics by channel to evaluate ROI, CPA, and Conversion Rates."""
  summary = (
      df.groupby('channel')
      .agg(
          total_spend=('spend', 'sum'),
          total_conversions=('conversions', 'sum'),
          total_revenue=('revenue', 'sum'),
          total_clicks=('clicks', 'sum'),
          total_impressions=('impressions', 'sum'),
      )
      .reset_index()
  )

  # Calculate Key Marketing Metrics
  summary['CPA'] = np.where(
      summary['total_conversions'] > 0,
      np.round(summary['total_spend'] / summary['total_conversions'], 2),
      0,
  )
  summary['ROI_%'] = np.round(
      (
          (summary['total_revenue'] - summary['total_spend'])
          / summary['total_spend']
      )
      * 100,
      2,
  )
  summary['Conversion_Rate_%'] = np.round(
      (summary['total_conversions'] / summary['total_clicks']) * 100, 2
  )

  return summary.sort_values(by='ROI_%', ascending=False)


def plot_channel_performance(summary_df):
  """Generates and saves a visualization chart comparing ROI and CPA across channels."""
  fig, ax1 = plt.subplots(figsize=(10, 6))

  ax1.bar(
      summary_df['channel'],
      summary_df['ROI_%'],
      color='#1f77b4',
      alpha=0.8,
      label='ROI (%)',
  )
  ax1.set_xlabel('Marketing Channel', fontweight='bold')
  ax1.set_ylabel('Return on Investment (ROI %)', color='#1f77b4', fontweight='bold')
  ax1.tick_params(axis='y', labelcolor='#1f77b4')
  plt.xticks(rotation=15)

  ax2 = ax1.twinx()
  ax2.plot(
      summary_df['channel'],
      summary_df['CPA'],
      color='#ff7f0e',
      marker='o',
      linewidth=2,
      label='CPA ($)',
  )
  ax2.set_ylabel(
      'Cost Per Acquisition (CPA)', color='#ff7f0e', fontweight='bold'
  )
  ax2.tick_params(axis='y', labelcolor='#ff7f0e')

  plt.title(
      'FinTech Campaign Performance: ROI vs. Cost Per Acquisition (CPA)',
      pad=15,
      fontweight='bold',
  )
  plt.tight_layout()

  # Save figure for GitHub portfolio
  plt.savefig('campaign_performance_overview.png', dpi=300)
  print(
      '\n[Success] Visualization saved as "campaign_performance_overview.png"'
  )


if __name__ == '__main__':
  print('--- Initializing FinTech Campaign Analysis Pipeline ---')

  # Step 1: Generate dataset
  df_campaigns = generate_campaign_data()
  print(f'Generated {len(df_campaigns)} simulated campaign interaction records.')

  # Step 2: Run performance metrics
  metrics_summary = analyze_channel_performance(df_campaigns)
  print('\n--- Channel Performance Summary ---')
  print(metrics_summary.to_string(index=False))

  # Step 3: Plot and save visual asset
  plot_channel_performance(metrics_summary)