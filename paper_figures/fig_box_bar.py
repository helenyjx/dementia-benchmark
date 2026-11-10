from common import *
from matplotlib.patches import Rectangle
def box_fig(metrics,titles,fname,h=6,prefix=True):
    d=per_repeat(h)
    fig,axs=plt.subplots(1,3,figsize=(1053.47/72,296.41/72),dpi=300)
    for k,(ax,met,t) in enumerate(zip(axs,metrics,titles)):
        data=[d[d.model==m][met].values for m in MODELS]
        boxes(ax,data,range(len(MODELS)),[LCOL[m] for m in MODELS],[COL[m] for m in MODELS])
        style_cat(ax,MODELS)
        ax.set_title((f"({'abc'[k]}) " if prefix else '')+t,fontsize=14,pad=8)
    fig.subplots_adjust(left=0.035,right=0.995,top=0.90,bottom=0.195,wspace=0.17)
    for e in ('png','svg'): fig.savefig(fname+'.'+e,dpi=300)
    plt.close(fig)
def legend2(fig,x0,y0,dx=0.0070,dy=0.031):
    ov=fig.add_axes([0,0,1,1],facecolor='none'); ov.axis('off'); ov.set_xlim(0,1); ov.set_ylim(0,1)
    for r,(lab,cd) in enumerate([('6-year',COL),('8-year',LCOL)]):
        for i,m in enumerate(MODELS):
            ov.add_patch(Rectangle((x0+i*dx,y0-r*dy),0.0045,0.016,color=cd[m],lw=0))
        ov.text(x0+8*dx+0.003,y0-r*dy+0.008,lab,fontsize=8,va='center')
def bar_fig(metrics,titles,fname,prefix=True):
    t=pd.read_csv(A+'temporal_metrics.csv'); t=t[t.population=='all']
    fig,axs=plt.subplots(1,3,figsize=(1047.1/72,345.41/72),dpi=300)
    for k,(ax,met,ti) in enumerate(zip(axs,metrics,titles)):
        mx=0
        for j,(h,cd,off) in enumerate([(6,COL,-0.175),(8,LCOL,0.175)]):
            v=[t[(t.horizon==h)&(t.model==m)&(t.metric==met)].estimate.iloc[0] for m in MODELS]; mx=max(mx,max(v))
            ax.bar(np.arange(8)+off,v,0.33,color=[cd[m] for m in MODELS],edgecolor='white',linewidth=0.8)
        style_cat(ax,MODELS)
        ax.set_xlim(-0.6,7.6)
        ax.set_ylim(0,1.0 if met in('AUROC','Accuracy') else np.ceil(mx/0.05)*0.05+0.05)
        ax.set_title((f"({'abc'[k]}) " if prefix else '')+ti,fontsize=14,pad=10)
    fig.subplots_adjust(left=0.035,right=0.995,top=0.758,bottom=0.173,wspace=0.17)
    legend2(fig,0.905,0.953)
    for e in ('png','svg'): fig.savefig(fname+'.'+e,dpi=300)
    plt.close(fig)
if __name__=='__main__':
    box_fig(['AUPRC','AUROC','Accuracy'],['AUPRC','AUROC','Accuracy'],OUT_F+'Fig3_internal_boxplots')
    bar_fig(['AUPRC','AUROC','Accuracy'],['AUPRC','AUROC','Accuracy'],OUT_F+'Fig4_temporal_grouped_bars')
    box_fig(['Precision','Recall','F1'],['Precision','Recall','F1 Score'],OUT_S+'S5_internal_boxplots',prefix=False)
    bar_fig(['Precision','Recall','F1'],['Precision','Recall','F1 Score'],OUT_S+'S6_temporal_grouped_bars',prefix=False)
