from urllib.parse import urlparse
from tabulate import tabulate
from json import loads
from numerize import numerize
from qlik_sdk import GenericObjectProperties, NxInfo, NxMetaDef, HyperCubeDef, NxCalcCond, ValueExpr, StringExpr, NxDimension, NxInlineDimensionDef, SortCriteria, NxPage, OtherTotalSpecProp, NxMeasure, NxInlineMeasureDef, FieldAttributes, NxMiniChartDef, LayoutExclude


def print_table(data, columns=None, cummulative_column=None, grand_total=[0]):
    global __SUM
    data = shrink_table(data, columns, cummulative_column, grand_total)
    print(tabulate(data, headers="keys"))


def shrink_table(data, columns=None, cummulative_column=None, grand_total=[0]):
    if type(data) == str:
        data = loads(data)
    if 'data' in data:
        data = data['data']
    if columns:
        data = [{col: row.get(col, None) for col in columns} for row in data]
        if cummulative_column:
            for i in range(len(data)):
                grand_total[0] = grand_total[0] + data[i][cummulative_column]
                data[i]["sum_" +
                        cummulative_column] = numerize.numerize(grand_total[0])
    return data


def check_next(data):
    if type(data) == str:
        data = loads(data)
    if 'links' in data:
        if 'next' in data['links']:
            return data['links']['next']
    return None


def return_relative_url(url: str):
    url = urlparse(url)
    if "v1" in url.path:
        return url.path.split("v1")[1]
    return url.path


def barchart_template() -> GenericObjectProperties:
    return GenericObjectProperties(qExtendsId=None, qInfo=NxInfo(qId='zRJda', qType='barchart'), qMetaDef=NxMetaDef(), qStateName=None, qAppObjectListDef=None, qBookmarkListDef=None, qChildListDef=None, qDimensionListDef=None, qEmbeddedSnapshotDef=None, qExtensionListDef=None, qFieldListDef=None, qHyperCubeDef=HyperCubeDef(qAlwaysFullyExpanded=None, qCalcCond=ValueExpr(qv=None), qCalcCondition=NxCalcCond(qCond=ValueExpr(qv=None), qMsg=StringExpr(qv=None)), qColumnOrder=[], qContextSetExpression=None, qDimensions=[NxDimension(qAttributeDimensions=[], qAttributeExpressions=[], qCalcCond=ValueExpr(qv=None), qCalcCondition=NxCalcCond(qCond=ValueExpr(qv=None), qMsg=StringExpr(qv=None)), qDef=NxInlineDimensionDef(qActiveField=0, qFieldDefs=['A'], qFieldLabels=[''], qGrouping='N', qLabelExpression=None, qNumberPresentations=[], qReverseSort=None, qSortCriterias=[SortCriteria(qExpression=ValueExpr(qv=None), qSortByAscii=1, qSortByExpression=None, qSortByFrequency=None, qSortByGreyness=None, qSortByLoadOrder=1, qSortByNumeric=1, qSortByState=None)]), qIncludeElemValue=None, qLibraryId=None, qNullSuppression=None, qOtherLabel=StringExpr(qv='Others'), qOtherTotalSpec=OtherTotalSpecProp(qApplyEvenWhenPossiblyWrongResult=True, qForceBadValueKeeping=True, qGlobalOtherGrouping=None, qOtherCollapseInnerDimensions=None, qOtherCounted=ValueExpr(qv='10'), qOtherLimit=ValueExpr(qv='0'), qOtherLimitMode='OTHER_GE_LIMIT', qOtherMode='OTHER_OFF', qOtherSortMode='OTHER_SORT_DESCENDING', qReferencedExpression=StringExpr(qv=None), qSuppressOther=None, qTotalMode='TOTAL_OFF'), qShowAll=None, qShowTotal=None, qTotalLabel=StringExpr(qv=None))], qDynamicScript=[], qExpansionState=[], qIndentMode=None, qInitialDataFetch=[NxPage(qHeight=500, qLeft=0, qTop=0, qWidth=17)], qInterColumnSortOrder=[1, 0], qMaxStackedCells=5000, qMeasures=[NxMeasure(qAttributeDimensions=[], qAttributeExpressions=[], qCalcCond=ValueExpr(qv=None), qCalcCondition=NxCalcCond(qCond=ValueExpr(qv=None), qMsg=StringExpr(qv=None)), qDef=NxInlineMeasureDef(qAccumulate=0, qActiveExpression=0, qAggrFunc=None, qBrutalSum=None, qDef='rand()', qDescription=None, qExpressions=[], qGrouping='N', qLabel=None, qLabelExpression=None, qNumFormat=FieldAttributes(qDec=None, qFmt=None, qThou=None, qType='U', qUseThou=0, qnDec=10), qRelative=None, qReverseSort=None, qTags=[]), qLibraryId=None, qMiniChartDef=NxMiniChartDef(qAttributeExpressions=[], qDef=None, qLibraryId=None, qMaxNumberPoints=-1, qNullSuppression=None, qOtherTotalSpec=OtherTotalSpecProp(qApplyEvenWhenPossiblyWrongResult=True, qForceBadValueKeeping=True, qGlobalOtherGrouping=None, qOtherCollapseInnerDimensions=None, qOtherCounted=ValueExpr(qv=None), qOtherLimit=ValueExpr(qv=None), qOtherLimitMode='OTHER_GT_LIMIT', qOtherMode='OTHER_OFF', qOtherSortMode='OTHER_SORT_DESCENDING', qReferencedExpression=StringExpr(qv=None), qSuppressOther=None, qTotalMode='TOTAL_OFF'), qSortBy=SortCriteria(qExpression=ValueExpr(qv=None), qSortByAscii=None, qSortByExpression=None, qSortByFrequency=None, qSortByGreyness=None, qSortByLoadOrder=None, qSortByNumeric=None, qSortByState=None)), qSortBy=SortCriteria(qExpression=ValueExpr(qv=None), qSortByAscii=None, qSortByExpression=None, qSortByFrequency=None, qSortByGreyness=None, qSortByLoadOrder=1, qSortByNumeric=-1, qSortByState=None), qTrendLines=[])], qMode='S', qNoOfLeftDims=-1, qPopulateMissing=None, qPseudoDimPos=-1, qReductionMode='N', qShowTotalsAbove=None, qSortbyYValue=None, qStateName=None, qSuppressMissing=True, qSuppressZero=None, qTitle=StringExpr(qv=None)), qLayoutExclude=LayoutExclude(), qListObjectDef=None, qMeasureListDef=None, qMediaListDef=None, qNxLibraryDimensionDef=None, qNxLibraryMeasureDef=None, qSelectionObjectDef=None, qStaticContentUrlDef=None, qStringExpression=None, qTreeDataDef=None, qUndoInfoDef=None, qValueExpression=None, qVariableListDef=None)
