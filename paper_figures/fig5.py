"""Fig. 5: top five predictors by permutation importance (2010 sample, 6-year horizon)."""
from common import *


def main():
    p=pd.read_csv(A+'importance_permutation_h6.csv')
    L={'ageym':'Age','edstg':'Education','raceeth':'Race/ethnicity','gender':'Sex','mapa':'Difficulty using\na map','shlt':'Self-rated health','slfmem':'Self-rated memory','doctim':'Doctor visits\n(previous 2 years)','nrstim':'Nursing-home stays\n(previous 2 years)','nrsnit':'Nursing-home nights\n(previous 2 years)','livpar':'Living parents','livsib':'Living siblings','weight':'Weight','height':'Height','drink':'Ever drinks alcohol','proxy':'Proxy interview','adl5a':'ADL difficulties (0-5)','lbrf':'Labor force status','mstat':'Marital status','stroke':'Stroke','effort':'CES-D: everything\nan effort','depres':'CES-D: felt\ndepressed','flone':'CES-D: felt lonely','grossa':'Gross-motor\ndifficulties (0-5)','momage':"Mother's age",'dadage':"Father's age",'cendiv':'Census division'}
    C={'ageym':'#ffb4b4','edstg':'#d9d0fa','raceeth':'#c6e6f3','gender':'#e2d2a8','mapa':'#fff6ac','nrsnit':'#d69a9b','livpar':'#d6e7e9','shlt':'#ffdfae','doctim':'#efb8e5','slfmem':'#d9e6cf','weight':'#cde5cd','drink':'#d9e6cf',
     'lbrf':'#f5c9a0','effort':'#c9d6f0','depres':'#e8cfe0','proxy':'#cfe8da','livsib':'#f3e1c3','mstat':'#d8dcb4','stroke':'#e3c5c5','adl5a':'#c5d9e8','nrstim':'#e4b8b8','flone':'#d3c5e8','grossa':'#c8e0c0','momage':'#e9d8f0','dadage':'#f0e0d0','height':'#c8c8c8','cendiv':'#e0e0b8'}
    top=p[p['rank']<=5]
    fig,ax=plt.subplots(figsize=(822.27/72,436.75/72),dpi=300)
    order=['LR','GNB','DT','LightGBM','CatBoost','GAT','RealMLP','TabICL']
    used=set()
    for r,m in enumerate(order):
        x=top[top.model==m].sort_values('rank')
        for _,row in x.iterrows():
            k=int(row['rank'])-1; v=row.variable; used.add(v)
            ax.add_patch(plt.Rectangle((k,r),1,1,fc=C.get(v,'#dddddd'),ec='white',lw=2))
            ax.text(k+0.5,r+0.5,L.get(v,v),ha='center',va='center',fontsize=10)
    ax.set_xlim(0,5); ax.set_ylim(8,0)
    ax.set_xticks([i+0.5 for i in range(5)]); ax.set_xticklabels([f'Rank {i+1}' for i in range(5)],fontsize=11)
    ax.set_yticks([i+0.5 for i in range(8)]); ax.set_yticklabels(order,fontsize=11)
    ax.tick_params(length=0)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    for s in ('left','bottom'): ax.spines[s].set_linewidth(0.6)
    fig.subplots_adjust(left=0.075,right=0.99,top=0.99,bottom=0.075)
    for e in ('png','svg'): fig.savefig(OUT_F+'Fig5_top5_feature_matrix.'+e,dpi=300)



if __name__ == "__main__":
    main()
