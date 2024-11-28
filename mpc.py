import pandas as pd
import numpy as np





def func(array):
    unique_rows = set(tuple(row) for row in array)
    unique_array = [list(row) for row in unique_rows]
    return unique_array

def minimalilty(elements):
    # Extract all unique numbers from the second components
    all_numbers = set()
    for element in elements:
        # Ensure the second component is a list
        if isinstance(element[1], list):
            all_numbers.update(element[1])
        else:
            all_numbers.add(element[1])

    covered_numbers = set()
    selected_elements = []

    # While not all numbers are covered
    while covered_numbers != all_numbers:
        best_element = None
        best_coverage = 0

        # Find the element that covers the most uncovered numbers
        for element in elements:
            if isinstance(element[1], list):
                coverage = len(set(element[1]) - covered_numbers)
            else:
                coverage = 1 if element[1] not in covered_numbers else 0
            if coverage > best_coverage:
                best_element = element
                best_coverage = coverage

        # Add the best element to the selected set
        selected_elements.append(best_element)
        if isinstance(best_element[1], list):
            covered_numbers.update(best_element[1])
        else:
            covered_numbers.add(best_element[1])

        # Remove the selected element from the list of elements
        elements.remove(best_element)

    return selected_elements


def main():

    df = pd.read_csv('data_supp.csv')

    df1 = df[['sp|Q99832|TCPH_HUMAN', 'sp|A0A0B4J1X5|HV374_HUMAN', 'sp|P24557|THAS_HUMAN', 'sp|P15169|CBPN_HUMAN', 'tr|I3L3Q7|I3L3Q7_HUMAN;tr|I3L3B0|I3L3B0_HUMAN;sp|Q07021|C1QBP_HUMAN', 'sp|P02549|SPTA1_HUMAN', 'tr|B4DUR8|B4DUR8_HUMAN;sp|P49368|TCPG_HUMAN', 'sp|Q92619|HMHA1_HUMAN;tr|K7ES98|K7ES98_HUMAN;tr|K7EM85|K7EM85_HUMAN;tr|K7ES92|K7ES92_HUMAN;tr|F5H1R4|F5H1R4_HUMAN', 'sp|P33151|CADH5_HUMAN;tr|I3L1J2|I3L1J2_HUMAN', 'sp|P02647|APOA1_HUMAN;tr|F8W696|F8W696_HUMAN', 'sp|P01780|HV307_HUMAN;sp|P01763|HV348_HUMAN;sp|P01762|HV311_HUMAN;sp|A0A0B4J1V1|HV321_HUMAN', 'sp|P63241|IF5A1_HUMAN;tr|I3L397|I3L397_HUMAN;tr|I3L504|I3L504_HUMAN;sp|Q6IS14|IF5AL_HUMAN', 'tr|A0A2R8YEA7|A0A2R8YEA7_HUMAN', 'sp|Q15833|STXB2_HUMAN;tr|M0R1A1|M0R1A1_HUMAN;tr|M0R0M7|M0R0M7_HUMAN', 'tr|A0A8Q3SI37|A0A8Q3SI37_HUMAN;tr|A0A8Q3SI95|A0A8Q3SI95_HUMAN;sp|P02748|CO9_HUMAN;tr|A0A8Q3SI39|A0A8Q3SI39_HUMAN', 'sp|Q70J99|UN13D_HUMAN;tr|A0A8V8TNG5|A0A8V8TNG5_HUMAN;tr|K7EN29|K7EN29_HUMAN', 'sp|P09486|SPRC_HUMAN;tr|F5GY03|F5GY03_HUMAN', 'tr|A0A7P0TAE1|A0A7P0TAE1_HUMAN;tr|H0YIV0|H0YIV0_HUMAN;sp|P14625|ENPL_HUMAN;tr|A0A7P0T823|A0A7P0T823_HUMAN;tr|A0A7P0TAT8|A0A7P0TAT8_HUMAN;tr|A0A7P0T917|A0A7P0T917_HUMAN;tr|A0A087WT78|A0A087WT78_HUMAN;tr|A0A7P0TAY2|A0A7P0TAY2_HUMAN', 'sp|P02787|TRFE_HUMAN', 'tr|A0A2R8YE50|A0A2R8YE50_HUMAN;tr|A0A2R8YH74|A0A2R8YH74_HUMAN;tr|B1ALS0|B1ALS0_HUMAN;tr|A0A2R8Y507|A0A2R8Y507_HUMAN', 'sp|Q8NG11|TSN14_HUMAN;tr|H7BXY6|H7BXY6_HUMAN;tr|A6NEP9|A6NEP9_HUMAN', 'tr|A0A8V8TKR9|A0A8V8TKR9_HUMAN;sp|P26038|MOES_HUMAN']]

    df1['result'] = [1 if i <10 or (i <30 and i>=20) else 0 for i in range(35)]

    df1.to_csv('new1.csv',index=False)


    df = df1.copy()

    df1 = df.iloc[:, 1:]
    df = df1.copy()


    df2 = df[df['result'] == 1]
    col = df.columns.tolist()
    cause = []
    for index, row in df2.iterrows():
        for i in range(len(row)-1):
            dfc = df[(df['result']==0) & (df[col[i]]==row[i])]
            if len(dfc)>0:
                continue
                
            cause.append(col[i])

    cause = list(dict.fromkeys(cause))



    c = list()

    col = df.columns.tolist()
    results = {}
    comparison_columns = df.columns[:-1]

    for index in df2.index:
        current_row = df2.loc[index]
        results[index] = {}
        
        for feature in comparison_columns:
            if feature not in cause:
                continue
            if df[feature][index] == 0:
                continue

            all_data = df[df[feature]==df[feature][index]]
            actual = df[(df[feature] == df[feature][index]) & (df['result'] == 1)]
        

            mask = (df.drop(columns=[feature]) == df.drop(columns=[feature]).iloc[index]).all(axis=1)

            counterfactual = df[mask & (df[feature] != df[feature].iloc[index])]

            if len(counterfactual) > 0 :
                continue
            else:
                c.append([feature, df[feature][index], len(actual)/len(all_data)])

    x  = func(c)
    print(x)

if __name__ == "__main__":
    main()
