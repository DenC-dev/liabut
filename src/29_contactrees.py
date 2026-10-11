"""E19 (Addendum 7): a phylogeny with contact edges, using contacTrees (Neureiter et al. 2022) on BEAST 2.6.

BEAST 2.6.7 is compiled from github.com/CompEvol/beast2 (tag v2.6.7) with javac, and the prebuilt contacTrees 1.1.0
jar (github.com/NicoNeureiter/contacTrees, dist/) is added to the classpath. Maven Central is not reachable here.

Model (fixed before running):
  data      step-7 matrix (24 taxa, D1 LexStat 0.55, primary), one block per concept, ascertainment-corrected
  sites     binary CTMC, estimated frequencies, no rate heterogeneity
  clock     strict, rate fixed at 1 (no calibrations; heights in substitution units)
  tree      Yule prior on the ACG
  contact   expectedConversions ~ Exponential(mean 1), estimated; pMove ~ Beta(2, 16), as in the IE case study
  operators as in the IE case study (contacTrees-IndoEuropean, xml_snippets.py)

    CT_CHAIN=1500000 CT_CAP=200 CT_TAG=ct_A_nogamma python3 src/29_contactrees.py xml
    CT_CHAIN=1500000 CT_CAP=200 CT_GAMMA=1 CT_TAG=ct_B_gamma python3 src/29_contactrees.py xml
    java -cp <beast-2.6.7 classes and lib/*.jar>:contactrees.addon.jar:guava-23.0.jar \
        beast.app.beastapp.BeastMain -seed 7 -java results/literature/e19_contactrees/ct_A_nogamma.xml

Both chains kept adding contact edges (about 100 by 250,000 steps, each moving 14-23% of words) and were stopped
before stationarity; see results/literature/e19_trajectory.json. The first run, with the IE study's cap of 50
edges, hit the cap within 100,000 steps.
"""
import importlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from common import RES  # noqa: E402
from pipeline import variant_rows  # noqa: E402

bayes = importlib.import_module("09_bayes")
te = importlib.import_module("20_total_evidence")
OUT = os.path.join(RES, "literature", "e19_contactrees")
CHAIN = int(os.environ.get("CT_CHAIN", "3000000"))
CAP = int(os.environ.get("CT_CAP", "50"))          # upper bound on contact edges (50 in the IE study)
GAMMA = os.environ.get("CT_GAMMA", "0") == "1"     # among-site rate heterogeneity (4 gamma categories)
TAG = os.environ.get("CT_TAG", "timor_contactrees")


def blocks():
    rows = [r for r in variant_rows("d1", "lexstat", "primary") if r["Lect_ID"] in bayes.BAYES_TAXA]
    by_concept = defaultdict(lambda: defaultdict(set))
    attested = defaultdict(set)
    for r in rows:
        by_concept[r["Concept_ID"]][r["Cognateset_ID"]].add(r["Lect_ID"])
        attested[r["Concept_ID"]].add(r["Lect_ID"])
    data = {}
    for c in sorted(by_concept):
        sets = sorted(by_concept[c])
        data[c] = {t: ("0" + "".join("1" if t in by_concept[c][s] else "0" for s in sets)) if t in attested[c]
                   else "?" * (len(sets) + 1) for t in bayes.BAYES_TAXA}
    return data


def start_tree():
    """UPGMA on IQ-TREE's ML distances, as an ultrametric starting tree."""
    from scipy.cluster.hierarchy import average, to_tree
    from scipy.spatial.distance import squareform
    path = os.path.join(RES, "total_evidence", "lex_only.mldist")
    lines = open(path).read().split("\n")
    n = int(lines[0].strip())
    names, D = [], np.zeros((n, n))
    for i in range(n):
        p = lines[1 + i].split()
        names.append(p[0])
        D[i] = [float(x) for x in p[1:1 + n]]
    Z = average(squareform((D + D.T) / 2, checks=False))
    root = to_tree(Z)

    def nwk(node, parent_h):
        h = node.dist / 2
        if node.is_leaf():
            return f"{names[node.id]}:{parent_h - 0:.6f}"
        return f"({nwk(node.left, h)},{nwk(node.right, h)}):{parent_h - h:.6f}"

    def rec(node):
        h = node.dist / 2
        if node.is_leaf():
            return names[node.id], 0.0
        l, hl = rec(node.left)
        r, hr = rec(node.right)
        return f"({l}:{h - hl:.6f},{r}:{h - hr:.6f})", h
    s, _ = rec(root)
    return s + ":0.0;"


def xml():
    os.makedirs(OUT, exist_ok=True)
    data = blocks()
    concepts = [re.sub(r"[^A-Za-z0-9_]", "_", c) for c in data]
    taxa = [te.tx(t) for t in bayes.BAYES_TAXA]
    full, filt, start = {t: "" for t in bayes.BAYES_TAXA}, [], 1
    for c, cid in zip(data, concepts):
        L = len(next(iter(data[c].values())))
        for t in bayes.BAYES_TAXA:
            full[t] += data[c][t]
        filt.append(f'<data id="feature_data:{cid}" spec="FilteredAlignment" data="@data" filter="{start}-{start + L - 1}" '
                    f'ascertained="true" excludeto="1" userDataType="@dtype"/>')
        start += L
    seqs = "\n".join(f'  <sequence id="seq:{te.tx(t)}" taxon="{te.tx(t)}" value="{full[t]}"/>' for t in bayes.BAYES_TAXA)
    lik = "\n".join(
        f'      <distribution id="treeLikelihood.{c}" spec="TreeLikelihood" useAmbiguities="true" siteModel="@SiteModel" '
        f'data="@feature_data:{c}">\n        <tree id="marginalTree.{c}" spec="MarginalTree" network="@acg" '
        f'block="@{c}" branchRateModel="@clock"/>\n      </distribution>' for c in concepts)
    tl = "\n".join(f'          <treeLikelihood idref="treeLikelihood.{c}"/>' for c in concepts)
    gibbs_args = 'acg="@acg" pMove="@pMove" conversionRate="@conversionRate" blockSet="@allBlocks" networkPrior="@ACGYule"'
    doc = f'''<?xml version='1.0' encoding='UTF-8'?>
<beast version="2.0" namespace="beast.core:beast.evolution.alignment:beast.evolution.tree:beast.core.util:beast.evolution.operators:beast.evolution.sitemodel:beast.evolution.substitutionmodel:beast.evolution.likelihood:beast.evolution.branchratemodel:beast.math.distributions:beast.core.parameter:contactrees:contactrees.model:contactrees.util:contactrees.operators">
<taxonset id="taxa" spec="TaxonSet">
{chr(10).join(f'  <taxon id="{t}" spec="Taxon"/>' for t in taxa)}
</taxonset>
<data id="data" name="data" dataType="integer">
{seqs}
</data>
<userDataType id="dtype" spec="beast.evolution.datatype.Binary"/>
{chr(10).join(filt)}
<branchRateModel id="clock" spec="StrictClockModel" clock.rate="1.0"/>
<substModel id="substModel" spec="GeneralSubstitutionModel">
  <rates spec="RealParameter" dimension="2" estimate="false" id="rates.binaryCTMC">1.0 1.0</rates>
  <frequencies id="frequenciesCTMC" spec="Frequencies" frequencies="@freqParameter"/>
</substModel>
{'<siteModel id="SiteModel" spec="SiteModel" substModel="@substModel" gammaCategoryCount="4" shape="@gammaShape"/>' if GAMMA else '<siteModel id="SiteModel" spec="SiteModel" substModel="@substModel"/>'}
<stateNode spec="BlockSet" id="allBlocks" network="@acg">
{chr(10).join(f'  <block spec="Block" id="{c}"/>' for c in concepts)}
</stateNode>
<run id="mcmc" spec="MCMC" chainLength="{CHAIN}">
  <state id="state" storeEvery="5000">
    <stateNode id="acg" spec="contactrees.ConversionGraph" taxonset="@taxa" newick="{start_tree()}"/>
    <stateNode id="birthRate" spec="RealParameter" lower="0.0">5.0</stateNode>
    <stateNode id="freqParameter" spec="RealParameter" dimension="2" lower="0.0" upper="1.0">0.8 0.2</stateNode>
{chr(10).join(f'    <stateNode idref="{c}"/>' for c in concepts)}
    <stateNode id="expectedConversions" spec="RealParameter" lower="0.0" value="1.0"/>
    <stateNode id="conversionRate" spec="ConversionRate" expectedConversions="@expectedConversions" linearContactGrowth="true" network="@acg"/>
    <stateNode id="pMove" spec="RealParameter" lower="0.0" upper="0.4" value="0.1"/>
{'    <stateNode id="gammaShape" spec="RealParameter" lower="0.01">1.0</stateNode>' if GAMMA else ''}
  </state>
  <distribution id="posterior" spec="util.CompoundDistribution">
    <distribution id="prior" spec="util.CompoundDistribution">
      <distribution id="ACGYule" spec="contactrees.model.ACGDistribution" network="@acg" conversionRate="@conversionRate" linearContactGrowth="true" upperConvCountBound="{CAP}">
        <cfModel id="Yule" spec="beast.evolution.speciation.YuleModel" tree="@acg" birthDiffRate="@birthRate"/>
      </distribution>
      <distribution id="ConvMovePrior" spec="ConversionMovePrior" network="@acg" blockSet="@allBlocks" pMove="@pMove"/>
      <prior id="prior:expectedConversions" spec="beast.math.distributions.Prior" name="distribution" x="@expectedConversions"><distr spec="Exponential" mean="1.0"/></prior>
      <prior id="prior:pMove" spec="beast.math.distributions.Prior" name="distribution" x="@pMove"><distr spec="Beta" alpha="2" beta="16"/></prior>
      <prior id="prior:birthRate" spec="beast.math.distributions.Prior" name="distribution" x="@birthRate"><distr spec="OneOnX"/></prior>
{'      <prior id="prior:gammaShape" spec="beast.math.distributions.Prior" name="distribution" x="@gammaShape"><distr spec="Exponential" mean="1.0"/></prior>' if GAMMA else ''}
    </distribution>
    <distribution id="likelihood" spec="util.CompoundDistribution">
{lik}
    </distribution>
  </distribution>
  <operator id="CFWilsonBalding" spec="CFWilsonBalding" acg="@acg" conversionRate="@conversionRate" pMove="@pMove" blockSet="@allBlocks" includeRoot="false" alpha="0.1" networkPrior="@ACGYule" weight="1.0"/>
  <operator id="CFNarrowExchange" spec="CFSubtreeExchange" acg="@acg" conversionRate="@conversionRate" pMove="@pMove" blockSet="@allBlocks" isNarrow="true" networkPrior="@ACGYule" weight="10.0"/>
  <operator id="CFWideExchange" spec="CFSubtreeExchange" acg="@acg" conversionRate="@conversionRate" pMove="@pMove" blockSet="@allBlocks" isNarrow="false" networkPrior="@ACGYule" weight="1.0"/>
  <operator id="ACGscaler" spec="ACGScaler" acg="@acg" scaleFactor="0.9" weight="10.0"/>
  <operator id="ACGscaler.rootOnly" spec="ACGScaler" acg="@acg" scaleFactor="0.75" weight="1.0" rootOnly="true"/>
  <operator id="CFUniform" spec="CFUniform" acg="@acg" conversionRate="@conversionRate" pMove="@pMove" blockSet="@allBlocks" scaleFactor="0.9" networkPrior="@ACGYule" weight="28.0"/>
  <operator id="AddRemoveConversion" spec="AddRemoveConversionGibbs" weight="50.0" {gibbs_args}>
{tl}
  </operator>
  <operator id="GibbsMoves" spec="GibbsSampleMovesPerConversion" weight="10.0" acg="@acg" pMove="@pMove" blockSet="@allBlocks" mcmcmc="true">
{tl}
  </operator>
  <operator id="ConvertedEdgeSlide" spec="ConvertedEdgeSlide" acg="@acg" apertureSize="0.2" weight="15.0"/>
  <operator id="ConvertedEdgeFlip" spec="ConvertedEdgeFlip" acg="@acg" weight="1.0"/>
  <operator id="ConversionSplit" spec="ConversionSplit" acg="@acg" weight="1.0" blockSet="@allBlocks" conversionRate="@conversionRate" networkPrior="@ACGYule" flip="false" pMove="@pMove"/>
  <operator id="EdgeHop.source" spec="ConvertedEdgeHopGibbs" sourceOnly="true" weight="2.0" {gibbs_args}>
{tl}
  </operator>
  <operator id="EdgeHop.source.narrow" spec="ConvertedEdgeHopGibbs" sourceOnly="true" nClosestRelatives="3" weight="6.0" {gibbs_args}>
{tl}
  </operator>
  <operator id="EdgeHop.narrow" spec="ConvertedEdgeHopGibbs" nClosestRelatives="3" weight="2.0" {gibbs_args}>
{tl}
  </operator>
  <operator id="BirthRateScaler" spec="ScaleOperator" parameter="@birthRate" scaleFactor="0.5" weight="2.0"/>
  <operator id="FreqExchange" spec="DeltaExchangeOperator" parameter="@freqParameter" delta="0.015" weight="1.0"/>
  <operator id="ExpConvScaler" spec="ScaleOperator" parameter="@expectedConversions" scaleFactor="0.6" weight="2.0"/>
  <operator id="pMoveScaler" spec="ScaleOperator" parameter="@pMove" scaleFactor="0.6" weight="2.0"/>
{'  <operator id="gammaShapeScaler" spec="ScaleOperator" parameter="@gammaShape" scaleFactor="0.5" weight="2.0"/>' if GAMMA else ''}
  <logger id="screenlog" spec="Logger" logEvery="20000">
    <log idref="posterior"/>
    <log idref="likelihood"/>
    <log spec="ACGStatsLogger" network="@acg" blockSet="@allBlocks"/>
  </logger>
  <logger id="tracelog" spec="Logger" fileName="$(filebase).log" logEvery="2000" sanitiseHeaders="true">
    <log idref="posterior"/>
    <log idref="likelihood"/>
    <log idref="prior"/>
    <log spec="ACGStatsLogger" network="@acg" blockSet="@allBlocks"/>
    <log idref="conversionRate"/>
    <log idref="expectedConversions"/>
    <log idref="pMove"/>
    <log idref="birthRate"/>
    <log idref="freqParameter"/>
{'    <log idref="gammaShape"/>' if GAMMA else ''}
  </logger>
  <logger spec="Logger" fileName="$(filebase).trees" logEvery="5000" mode="tree">
    <log spec="ACGWithMetaDataLogger" network="@acg" blockSet="@allBlocks"/>
  </logger>
</run>
</beast>
'''
    open(os.path.join(OUT, f"{TAG}.xml"), "w").write(doc)
    json.dump(dict(taxa=len(taxa), concepts=len(concepts), sites=start - 1, chain=CHAIN, cap=CAP, gamma=GAMMA),
              open(os.path.join(OUT, f"{TAG}.setup.json"), "w"), indent=1)
    print(len(taxa), "taxa,", len(concepts), "concepts,", start - 1, "sites")


if __name__ == "__main__":
    {"xml": xml}[sys.argv[1]]()
