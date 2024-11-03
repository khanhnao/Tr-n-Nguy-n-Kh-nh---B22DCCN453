import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

def radar_chart(player1_data, player2_data, attributes, player1_name, player2_name):
    num_vars = len(attributes)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    player1_values = player1_data + player1_data[:1]
    player2_values = player2_data + player2_data[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    #cầu thủ 1
    ax.plot(angles, player1_values, linewidth=1, linestyle='solid', label=player1_name)
    ax.fill(angles, player1_values, 'b', alpha=0.1)

    #cầu thủ 2
    ax.plot(angles, player2_values, linewidth=1, linestyle='solid', label=player2_name)
    ax.fill(angles, player2_values, 'r', alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    plt.title(f'Radar Chart: {player1_name} vs {player2_name}', size=15)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Radar chart comparison for two players')
    parser.add_argument('--p1', type=str, required=True, help='Name of Player 1')
    parser.add_argument('--p2', type=str, required=True, help='Name of Player 2')
    parser.add_argument('--Atribute', type=str, required=True, help='list of attributes')

    args = parser.parse_args()
    player1_name = args.p1
    player2_name = args.p2
    attributes = args.Atribute.split(',')

    df = pd.read_csv('result.csv')

    player1_data = df[df['Name'] == player1_name][attributes].values.flatten().tolist()
    player2_data = df[df['Name'] == player2_name][attributes].values.flatten().tolist()

    radar_chart(player1_data, player2_data, attributes, player1_name, player2_name)

if __name__ == "__main__":
    main()
