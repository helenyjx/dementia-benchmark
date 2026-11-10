from common import *
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
GR='#52514e'; GRID='#e4e3df'; SP_C='#8a8984'
def clean(ax,left_only=True):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    for s in ('left','bottom'): ax.spines[s].set_color(SP_C); ax.spines[s].set_linewidth(0.8)
    ax.tick_params(colors=GR,labelsize=9,width=0.8); 
def save(fig,name):
    for e in ('png','svg'): fig.savefig(OUT_S+name+'.'+e,dpi=300)
    plt.close(fig)
def sqleg(fig,items,y,x0,fs=10):
    pass
# ---------- S2 imputation comparison
def s2():
    S={'mean':('#35a2ef','#9ad0f7','Mean imputation'),'complete_case':('#ee655a','#f6b2ac','No imputation (complete-case)'),'miceforest':('#2fc268','#97e0b3','MICE')}
    D={k:strat(6,k) for k in S}
    fig,axs=plt.subplots(1,3,figsize=(1061.09/72,355.43/72),dpi=300)
    for ax,met in zip(axs,['AUPRC','AUROC','Accuracy']):
        for j,(k,(ec,fc,_)) in enumerate(S.items()):
            pos=np.arange(8)+(j-1)*0.25
            boxes(ax,[D[k][D[k].model==m][met].values for m in MODELS],pos,[fc]*8,[ec]*8,width=0.21,lw=1.0)
        style_cat(ax,MODELS); ax.set_xlim(-0.6,7.6); ax.set_title(met,fontsize=13.2,pad=8)
    fig.subplots_adjust(left=0.035,right=0.995,top=0.92,bottom=0.30,wspace=0.17)
    fig.legend(handles=[Rectangle((0,0),1,1,fc=v[0],ec=v[0]) for v in S.values()],labels=[v[2] for v in S.values()],loc='lower center',ncol=3,frameon=False,fontsize=10,handlelength=3,bbox_to_anchor=(0.5,0.0))
    save(fig,'S2_imputation_comparison_all_8_models')
# ---------- S3 complete-case
def s3():
    im=pd.read_csv(A+'internal_metrics.csv'); tm=pd.read_csv(A+'temporal_metrics.csv')
    order=PANEL
    fig,axs=plt.subplots(2,4,figsize=(1001.76/72,530.75/72),dpi=300)
    cols=[('Internal','AUROC',im),('Internal','AUPRC',im),('Temporal','AUROC',tm),('Temporal','AUPRC',tm)]
    for r,h in enumerate([6,8]):
        cd=COL if h==6 else LCOL
        for c,(kind,met,df) in enumerate(cols):
            ax=axs[r,c]; ys=np.arange(8)[::-1]
            for y,m in zip(ys,order):
                for pop,off,filled in [('all',0.17,True),('complete',-0.17,False)]:
                    row=df[(df.horizon==h)&(df.model==m)&(df.metric==met)&(df.population==pop)].iloc[0]
                    ax.plot([row.ci_low*100,row.ci_high*100],[y+off]*2,color=cd[m],lw=1.5,solid_capstyle='butt')
                    ax.plot(row.estimate*100,y+off,'o',ms=4.5,mfc=cd[m] if filled else 'white',mec=cd[m],mew=1.2)
            clean(ax); ax.set_yticks(ys); ax.set_ylim(-0.6,7.6)
            ax.set_yticklabels([pn(m) for m in order] if c==0 else [],fontsize=11)
            if c>0: ax.tick_params(axis='y',length=0)
            ax.xaxis.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True)
            ax.xaxis.set_major_locator(plt.MaxNLocator(4))
            ax.set_title(f'{h}-year horizon\n{kind} {met} (%)',fontsize=11,pad=6)
    fig.subplots_adjust(left=0.085,right=0.995,top=0.82,bottom=0.07,wspace=0.12,hspace=0.45)
    fig.legend(handles=[Line2D([],[],color=GR,marker='o',mfc=GR,lw=1.5,ms=5),Line2D([],[],color=GR,marker='o',mfc='white',lw=1.5,ms=5)],labels=['All participants (primary)','Complete predictors'],loc='upper center',ncol=2,frameon=False,fontsize=9,bbox_to_anchor=(0.5,1.0))
    ov=fig.add_axes([0,0,1,1],facecolor='none'); ov.axis('off'); ov.set_xlim(0,1); ov.set_ylim(0,1)
    ov.text(0.085,0.932,'Model colors (6-year | 8-year):',fontsize=9,va='center',ha='left')
    x=0.265
    for m in PANEL:
        ov.add_patch(Rectangle((x,0.9245),0.0075,0.015,color=COL[m],lw=0))
        ov.add_patch(Rectangle((x+0.0095,0.9245),0.0075,0.015,color=LCOL[m],lw=0))
        ov.text(x+0.0215,0.932,pn(m),fontsize=9,va='center',ha='left')
        x+=0.0215+0.0052*len(pn(m))+0.014
    save(fig,'S3_complete_case_sensitivity_CI')
# ---------- S4 decision curves
def s4():
    d=pd.read_csv(A+'decision_curves.csv'); d=d[d.population=='all']
    fig,axs=plt.subplots(2,4,figsize=(864/72,449.04/72),dpi=300,sharex=True,sharey=True)
    top=np.ceil((d.net_benefit.max()+0.004)/0.01)*0.01
    for i,m in enumerate(PANEL):
        ax=axs[i//4,i%4]
        for h,cd,tc in [(6,COL,'#4d4d4d'),(8,LCOL,'#a6a6a6')]:
            x=d[(d.model==m)&(d.horizon==h)].sort_values('threshold')
            ax.plot(x.threshold*100,x.net_benefit,color=cd[m],lw=1.8)
            ax.plot(x.threshold*100,x.treat_all,color=tc,lw=1.1,ls='--')
        ax.axhline(0,color='#0b0b0b',lw=0.8)
        clean(ax); ax.set_xlim(5,40); ax.set_ylim(-0.03,top)
        ax.set_xticks([5,10,20,30,40]); yt=np.arange(0,top,0.05) if top>0.1 else np.arange(0,top,0.02); ax.set_yticks(yt); ax.set_yticklabels([f'{v:.2f}' for v in yt])
        ax.yaxis.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True)
        ax.set_title(pn(m),fontsize=11,pad=6)
        if i%4==0: ax.set_ylabel('Net benefit',fontsize=10,color=GR)
        if i//4==1: ax.set_xlabel('Risk threshold (%)',fontsize=10,color=GR)
    fig.subplots_adjust(left=0.065,right=0.995,top=0.94,bottom=0.2,wspace=0.1,hspace=0.45)
    ov=fig.add_axes([0,0,1,1],facecolor='none'); ov.axis('off'); ov.set_xlim(0,1); ov.set_ylim(0,1)
    y=0.055; x=0.14
    for cd,lab,xx in [(COL,'6-year model',0.14),(LCOL,'8-year model',0.355)]:
        for i,m in enumerate(MODELS): ov.add_patch(Rectangle((xx+i*0.0105,y-0.008),0.0075,0.017,color=cd[m],lw=0))
        ov.text(xx+8*0.0105+0.005,y,lab,fontsize=10,va='center')
    for xx,col,ls,lab in [(0.58,'#4d4d4d','--','6-year treat all'),(0.72,'#a6a6a6','--','8-year treat all'),(0.865,'#0b0b0b','-','Treat none')]:
        ov.plot([xx-0.02,xx+0.005],[y,y],color=col,ls=ls,lw=1.1); ov.text(xx+0.01,y,lab,fontsize=10,va='center')
    save(fig,'S4_decision_curves_6_and_8y')
# ---------- S7 calibration
def s7():
    c=pd.read_csv(A+'calibration_curves.csv'); c=c[(c.setting=='temporal')&(c.population=='all')]
    t=pd.read_csv(A+'temporal_metrics.csv'); t=t[t.population=='all']
    fig,axs=plt.subplots(2,4,figsize=(850.41/72,475.86/72),dpi=300,sharex=True,sharey=True)
    for i,m in enumerate(PANEL):
        ax=axs[i//4,i%4]
        ax.plot([0,1],[0,1],color=SP_C,lw=1.2,zorder=1)
        txt=[]
        for h,cd in [(6,COL),(8,LCOL)]:
            x=c[(c.model==m)&(c.horizon==h)].sort_values('bin')
            ax.plot(x.predicted,x.observed,'-o',color=cd[m],lw=1.4,ms=3.2,mec='white',mew=0.5,zorder=3 if h==6 else 2)
            oe=t[(t.model==m)&(t.horizon==h)&(t.metric=='OE_ratio')].estimate.iloc[0]; sl=t[(t.model==m)&(t.horizon==h)&(t.metric=='calibration_slope')].estimate.iloc[0]
            txt.append(f'{h} years: O/E {oe:.2f}, slope {sl:.2f}')
        ax.text(0.04,0.96,'\n'.join(txt),transform=ax.transAxes,fontsize=7.5,va='top',color='#333333')
        clean(ax); ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True); ax.tick_params(labelsize=11)
        ax.set_title(pn(m),fontsize=11,pad=6)
        if i%4==0: ax.set_ylabel('Observed incidence',fontsize=11,color=GR)
        if i//4==1: ax.set_xlabel('Mean predicted risk',fontsize=11,color=GR)
    fig.subplots_adjust(left=0.075,right=0.995,top=0.9,bottom=0.1,wspace=0.13,hspace=0.14)
    ov=fig.add_axes([0,0,1,1],facecolor='none'); ov.axis('off'); ov.set_xlim(0,1); ov.set_ylim(0,1)
    for cd,lab,xx in [(COL,'6-year horizon',0.35),(LCOL,'8-year horizon',0.53)]:
        for i,m in enumerate(MODELS): ov.add_patch(Rectangle((xx+i*0.0075,0.97),0.0055,0.016,color=cd[m],lw=0))
        ov.text(xx+8*0.0075+0.004,0.978,lab,fontsize=9,va='center')
    save(fig,'S7_calibration')
LAB={'ageym':'Age','edstg':'Education','raceeth':'Race/ethnicity','gender':'Sex','mapa':'Difficulty using a map','shlt':'Self-rated health','slfmem':'Self-rated memory','doctim':'Doctor visits (2 years)','nrstim':'Nursing-home stays (2 years)','nrsnit':'Nursing-home nights (2 years)','livpar':'Living parents','livsib':'Living siblings','weight':'Weight','height':'Height','drink':'Ever drinks alcohol','proxy':'Proxy interview','adl5a':'ADL difficulties (0-5)','lbrf':'Labor force status','mstat':'Marital status','stroke':'Stroke','effort':'CES-D: everything\nan effort','depres':'CES-D: felt depressed','flone':'CES-D: felt lonely','grossa':'Gross-motor difficulties (0-5)','momage':"Mother's age",'dadage':"Father's age",'cendiv':'Census division'}
def lab(v): return LAB.get(v,v)
# ---------- S8 permutation importance
def s8():
    p=pd.read_csv(A+'importance_permutation_h6.csv')
    fig,axs=plt.subplots(2,4,figsize=(1131.84/72,649.33/72),dpi=300)
    for i,m in enumerate(PANEL):
        ax=axs[i//4,i%4]; x=p[p.model==m].sort_values('rank')
        a=x.iloc[0]; b=x.iloc[1:11].iloc[::-1]
        ax.barh(range(10),b.importance_AUPRC_drop*100,height=0.62,color=COL[m])
        ax.errorbar(b.importance_AUPRC_drop*100,range(10),xerr=[(b.importance_AUPRC_drop-b.ci_low)*100,(b.ci_high-b.importance_AUPRC_drop)*100],fmt='none',ecolor='#262626',elinewidth=1.1,capsize=0)
        ax.set_yticks(range(10)); ax.set_yticklabels([lab(v) for v in b.variable],fontsize=9.3,color='#0b0b0b'); ax.set_ylim(-0.6,9.6)
        clean(ax); ax.xaxis.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True); ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        ax.set_title(f'{pn(m)}\nAge (rank 1): {a.importance_AUPRC_drop*100:.1f} ({a.ci_low*100:.1f}–{a.ci_high*100:.1f})',fontsize=11,pad=6)
    fig.subplots_adjust(left=0.115,right=0.972,top=0.9,bottom=0.1,wspace=1.25,hspace=0.45)
    fig.text(0.5,0.02,'Decrease in AUPRC (percentage points); lines indicate 95% household-bootstrap confidence intervals',ha='center',fontsize=11,color='#0b0b0b')
    save(fig,'S8_permutation_importance_CI')
# ---------- S9 shap vs perm
def s9():
    p=pd.read_csv(A+'importance_permutation_h6.csv'); s=pd.read_csv(A+'importance_shap_h6.csv'); ra=pd.read_csv(A+'importance_rank_agreement_h6.csv').set_index('model')
    order=['TabICL','CatBoost','LightGBM','LR','RealMLP','GAT','DT','GNB']
    fig,axs=plt.subplots(3,3,figsize=(849.46/72,1006.15/72),dpi=300,sharex=True,sharey=True)
    for i,m in enumerate(order):
        ax=axs[i//3,i%3]; a=p[p.model==m].merge(s[s.model==m],on='variable',suffixes=('_p','_s'))
        approx='approx' in ra.loc[m,'method'] or 'Kernel' in ra.loc[m,'method']
        pts=a[['rank_p','rank_s']].drop_duplicates()
        ax.plot([0,60],[0,60],color=SP_C,lw=0.8,zorder=1)
        if approx: ax.scatter(pts.rank_p,pts.rank_s,s=14,facecolors='none',edgecolors=COL[m],linewidths=0.8,zorder=3,alpha=0.85)
        else: ax.scatter(pts.rank_p,pts.rank_s,s=14,color=COL[m],edgecolors='white',linewidths=0.4,zorder=3,alpha=0.85)
        clean(ax); ax.set_xlim(-1,61); ax.set_ylim(61,-1); ax.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True)
        ax.set_xticks(range(0,61,10)); ax.set_yticks(range(0,61,10)); ax.tick_params(labelsize=10)
        ax.set_title(f"{pn(m)}{' (approximate)' if approx else ''}\nSpearman {ra.loc[m,'spearman_rank_correlation']:.2f}; top 10 shared: {ra.loc[m,'shared_top10']}",fontsize=11,pad=4)
        nt=int((a.rank_s.duplicated(keep=False)).sum())
        if m=='DT':
            tied=a.groupby('rank_s').size(); k=int(tied.max())
            if k>1: ax.text(0.98,0.97,f'{k} predictors not used by\nthe model are tied\n(one point)',transform=ax.transAxes,fontsize=6.6,ha='right',va='top',color='#333333')
    axs[2,2].axis('off')
    axs[2,2].text(0.0,0.9,'Filled: exact SHAP\nOpen: approximate SHAP\n(KernelSHAP, 500 participants)',fontsize=8,va='top',color='#333333',transform=axs[2,2].transAxes)
    fig.subplots_adjust(left=0.065,right=0.995,top=0.965,bottom=0.045,wspace=0.07,hspace=0.18)
    fig.text(0.015,0.5,'SHAP rank',rotation=90,fontsize=8,va='center',color='#333333')
    fig.text(0.5,0.012,'Permutation-importance rank',ha='center',fontsize=8,color='#333333')
    save(fig,'S9_shap_vs_permutation')
if __name__=='__main__':
    import sys
    for f in (sys.argv[1:] or ['s2','s3','s4','s7','s8','s9']): globals()[f]()
