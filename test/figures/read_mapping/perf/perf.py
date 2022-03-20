import numpy as np
import pandas as pd
import csv
import seaborn as sns
import sys
import matplotlib.pyplot as plt
from collections import OrderedDict
from argparse import ArgumentParser
import pathlib

def main():
    args = get_args()
    sns.set(style='white')
    palette=sns.color_palette('tab10')
    colors = ["#4b71bb", "#f0c041", "#5FA137", "#db8043", "#a3a3a3", "#aa4499"]
    
    for f in args.input:
        sample = f.replace(".csv", "")
        enums = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z']
        with open(f, 'r') as csvfile:
            data = pd.read_csv(csvfile)
            fig, ax = plt.subplots(2, 1, figsize=(11,5))
            g = []
            g.append(sns.barplot(ax=ax[0], x = "Data", y = "CPU Time", hue = "Tool", data = data, palette=colors, alpha=0.9, edgecolor='black', linewidth=1.2))
            ax[0].grid(linestyle='--', linewidth=0.4)
            handles, labels = ax[0].get_legend_handles_labels()
            ax[0].legend(bbox_to_anchor=(0.5,1.15), loc='upper center', ncol=len(labels), facecolor='white', framealpha=0, fontsize="medium")
            # labels = ['('+enums[idx]+') '+item.get_text() for idx, item in enumerate(ax[0].get_xticklabels())]
            # labels = [item.get_text() for idx, item in enumerate(ax[0].get_xticklabels())]

            ax[0].set_xticklabels('')
            # ax[0].set_xticklabels(labels, rotation = 0, ha = 'center', fontweight='bold', fontsize='medium')
            ax[0].set_xlabel("")
            ax[0].set_ylabel("CPU Time (sec)", fontweight='bold', fontsize='large')
            ax[0].set_yscale("log")
            
            ax[0].tick_params(axis="y", which="both", direction="in", left=True, width=0.5)
            ax[0].tick_params(axis="x", which="both", direction="in", top=True)

            blend = data[data.Tool.eq('BLEND')]
            uniqtool = len(data.Tool.unique())
            labels = []
            vals = []
            for item in data.Data.unique():
                blendval = min(blend[blend.Data.eq(item)]["CPU Time"])
                for tool in data.Tool.unique():
                    if tool != 'BLEND':
                        tooldat = data[data.Tool.eq(tool)]
                        if len(tooldat[tooldat.Data.eq(item)]["CPU Time"]) > 0:
                            val = min(tooldat[tooldat.Data.eq(item)]["CPU Time"])/blendval
                            labels.append(r'$%.1f{\times}$' % val)
                            vals.append(val)
                        else: 
                            labels += ' '
                            vals.append(None)
                    else:
                        labels += ' '
                        vals.append(None)
            left,right = ax[0].get_ylim()
            ax[0].set_ylim(left, right+right*35)

            ind = 0
            for c in ax[0].containers:
                speedups = [x for x in vals[ind::uniqtool] if x is not None]
                if ind == 1:
                    print("\\newcommand\\avgrmpM{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmpHM{$%.1f\\times$\\xspace}\n\\newcommand\\rmpM{$%.1f\\times$\\xspace}\n\\newcommand\\mrmpM{$%.1f\\times$\\xspace}\n" % (sum(speedups)/len(speedups), sum(speedups[:3])/3, max(speedups), min(speedups)))
                elif ind == 2:
                    print("\\newcommand\\avgrmpL{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmpHL{$%.1f\\times$\\xspace}\n\\newcommand\\rmpL{$%.1f\\times$\\xspace}\n\\newcommand\\mrmpL{$%.1f\\times$\\xspace}\n" % (sum(speedups)/(len(speedups)-1), sum(speedups[:3])/3, max(speedups), min(speedups)))
                elif ind == 3:
                    print("\\newcommand\\avgrmpW{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmpHW{$%.1f\\times$\\xspace}\n\\newcommand\\rmpW{$%.1f\\times$\\xspace}\n\\newcommand\\mrmpW{$%.1f\\times$\\xspace}\n" % (sum(speedups)/len(speedups), sum(speedups[:3])/3, max(speedups), min(speedups)))
                elif ind == 4:
                    print("\\newcommand\\avgrmpS{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmpHS{$%.1f\\times$\\xspace}\n\\newcommand\\rmpS{$%.1f\\times$\\xspace}\n\\newcommand\\mrmpS{$%.1f\\times$\\xspace}\n" % (sum(speedups)/len(speedups), sum(speedups[:2])/2, max(speedups), min(speedups)))
                ax[0].bar_label(c, labels=labels[ind::uniqtool], fmt='%gs', color='red', size='medium', rotation='90', fontweight='bold')
                ind += 1

            g.append(sns.barplot(ax=ax[1], x = "Data", y = "Peak Memory (GB)", hue = "Tool", data = data, palette=colors, alpha=0.9, edgecolor='black', linewidth=1.2))
            ax[1].grid(linestyle='--', linewidth=0.4)
            # handles, labels = ax[1].get_legend_handles_labels()
            # ax[1].legend(bbox_to_anchor=(0.5,1.12), loc='upper center', ncol=len(labels), facecolor='white', framealpha=0, fontsize="medium")
            ax[1].get_legend().set_visible(False)
            labels = [item.get_text() for idx, item in enumerate(ax[1].get_xticklabels())]

            ax[1].set_xticklabels(labels, rotation = 0, ha = 'center', fontweight='bold', fontsize='large')
            ax[1].set_xlabel("")
            ax[1].set_ylabel("Peak Memory (GB)", fontweight='bold', fontsize='large')
            ax[1].set_yscale("log")
            
            ax[1].tick_params(axis="y", which="both", direction="in", left=True, width=0.5)
            ax[1].tick_params(axis="x", which="both", direction="in", top=True)

            blend = data[data.Tool.eq('BLEND')]
            uniqtool = len(data.Tool.unique())
            labels = []
            vals = []
            for item in data.Data.unique():
                blendval = min(blend[blend.Data.eq(item)]["Peak Memory (GB)"])
                for tool in data.Tool.unique():
                    if tool != 'BLEND':
                        tooldat = data[data.Tool.eq(tool)]
                        if len(tooldat[tooldat.Data.eq(item)]["Peak Memory (GB)"]) > 0:
                            val = min(tooldat[tooldat.Data.eq(item)]["Peak Memory (GB)"])/blendval
                            labels.append(r'$%.1f{\times}$' % val)
                            vals.append(val)
                        else: 
                            labels += ' '
                            vals.append(None)
                    else:
                        labels += ' '
                        vals.append(None)
            left,right = ax[1].get_ylim()
            ax[1].set_ylim(left, right+right*5)

            ind = 0
            for c in ax[1].containers:
                mems = [x for x in vals[ind::uniqtool] if x is not None]
                if ind == 1:
                    print("\\newcommand\\avgrmmM{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmmHM{$%.1f\\times$\\xspace}\n\\newcommand\\rmmM{$%.1f\\times$\\xspace}\n\\newcommand\\mrmmM{$%.1f\\times$\\xspace}\n" % (sum(mems)/len(mems), sum(mems[:3])/3, max(mems), min(mems)))
                elif ind == 2:
                    print("\\newcommand\\avgrmmL{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmmHL{$%.1f\\times$\\xspace}\n\\newcommand\\rmmL{$%.1f\\times$\\xspace}\n\\newcommand\\mrmmL{$%.1f\\times$\\xspace}\n" % (sum(mems)/len(mems), sum(mems[:3])/3, max(mems), min(mems)))
                elif ind == 3:
                    print("\\newcommand\\avgrmmW{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmmHW{$%.1f\\times$\\xspace}\n\\newcommand\\rmmW{$%.1f\\times$\\xspace}\n\\newcommand\\mrmmW{$%.1f\\times$\\xspace}\n" % (sum(mems)/len(mems), sum(mems[:3])/3, max(mems), min(mems)))
                elif ind == 4:
                    print("\\newcommand\\avgrmmS{$%.1f\\times$\\xspace}\n\\newcommand\\avgrmmHS{$%.1f\\times$\\xspace}\n\\newcommand\\rmmS{$%.1f\\times$\\xspace}\n\\newcommand\\mrmmS{$%.1f\\times$\\xspace}\n" % (sum(mems)/len(mems), sum(mems[:2])/2, max(mems), min(mems)))
                ax[1].bar_label(c, labels=labels[ind::uniqtool], fmt='%gs', color='red', size='medium', rotation='90')
                ind += 1

            plt.tight_layout()
            plt.subplots_adjust(top=0.95, bottom=0.04, left=0.05, right=0.994, hspace=0.05, wspace=0.2)
            plt.savefig(f'read_mapping-perf-all_{sample}.pdf')
            plt.show()

def get_args():
    parser = ArgumentParser(description="Creates PDF plots")
    parser.add_argument("input",
                        nargs='+',
                        help="the dist file(s) to use for plotting")
    return parser.parse_args()

if __name__ == '__main__':
    main()