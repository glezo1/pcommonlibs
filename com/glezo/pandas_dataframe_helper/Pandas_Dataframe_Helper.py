
import pandas       as pd
from tabulate       import tabulate
import numpy        as np

class Pandas_Dataframe_helper:
    #---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def print(df):
        #with pd.option_context('display.max_rows', None, 'display.max_columns', None,'display.expand_frame_repr', False):  # more options can be specified also
        #    print(df)
        print(tabulate(df, showindex=True, headers=df.columns))
    #---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def print_types(df):
        list_of_column_types    =   []
        max_colname_length      =   0
        for current_col in df:
            if(len(current_col)>max_colname_length):
                max_colname_length  =   len(current_col)
        for current_col in df:
            current_col_type    =   type(df[current_col].iat[0])
            list_of_column_types.append(current_col_type)
            print(current_col.ljust(max_colname_length)+' '+str(current_col_type)[len("<class '"):-len("'>")])
    #---------------------------------------------------------------------------------------------------------------------
    '''
        pretty slow!!! 2*N^2
    '''
    @staticmethod
    def check_dfs_differences(df_left, df_right, pk=None):   #pk must be a list or None to take all columns as PK!
        df_result           =   None
        column_names_1      =   [x for x in df_left.columns]
        column_names_2      =   [x for x in df_right.columns]
        if (column_names_1 != column_names_2):
            df_result                       =   pd.DataFrame(columns=['ERROR'])
            df_result.loc[len(df_result)]   =   ["Columns does not match or order is different"]
            return df_result
        # if no pk is specified, all columns are taken as pk
        if (pk == None):
            pk          =   column_names_1
        df_result_columns   =   [x for x in pk]
        df_result_columns.extend(['tipology','offending_column','left_value','right_value'])
        df_result           =   pd.DataFrame(columns = df_result_columns)
        #iterate left and search in right
        for _, current_left_row in df_left.iterrows():
            #find rows in right
            match           =   df_right
            row_to_append   =   []          #in case this rows produces an error, this is the df_result new row
            for current_col in pk:
                current_left_row_current_col_value  =   current_left_row[current_col]
                row_to_append.append(current_left_row_current_col_value)
                match                               =   match[match[current_col]==current_left_row_current_col_value]
            if(len(match)==0):
                row_to_append.extend(['LEFT_NOT_IN_RIGHT',None,None,None])
                df_result.loc[len(df_result)]   =   row_to_append
            elif(len(match)>1):
                row_to_append.extend(['NOT_VALID_PK',None,None,None])
                df_result                       =   pd.DataFrame(columns=df_result_columns)
                df_result.loc[len(df_result)]   =   row_to_append
                return df_result
            else:
                for current_col in column_names_1:
                    left_cell   =   current_left_row[current_col]
                    match_cell  =   match[current_col].iloc[0]
                    if(left_cell != match_cell):
                        row_to_append.extend(['IN_BOTH_BUT_DIFFERENT',current_col,left_cell,match_cell])
                        df_result.loc[len(df_result)]   =   row_to_append

        #iterate right and search in left
        for _, current_right_row in df_right.iterrows():
            #find rows in right
            match           =   df_left
            row_to_append   =   []          #in case this rows produces an error, this is the df_result new row
            for current_col in pk:
                current_right_row_current_col_value =   current_right_row[current_col]
                row_to_append.append(current_right_row_current_col_value)
                match                               =   match[match[current_col]==current_right_row_current_col_value]
            if(len(match)==0):
                row_to_append.extend(['RIGHT_NOT_IN_LEFT',None,None,None])
                df_result.loc[len(df_result)]   =   row_to_append
            elif(len(match)>1):
                row_to_append.extend(['NOT_VALID_PK',None,None,None])
                df_result                       =   pd.DataFrame(columns=df_result_columns)
                df_result.loc[len(df_result)]   =   row_to_append
                return df_result
            #IN_BOTH_BUT_DIFFERENT is already covered in the left-vs-right analysis.

        return df_result
    #---------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def column_biass(df_column):
        df_column_as_list           =   list(df_column)
        N                           =   len(df_column_as_list)
        values,counts               =   np.unique(df_column_as_list, return_counts=True)
        #generate synth list (TODO! what if not even number? Minimum Comun Multiple of(num_different_labels,[x for x in counts]))
        num_different_labels        =   len(values)
        num_items_per_label         =   N // num_different_labels
        synthetic_list              =   []
        for current_value in values:
            synthetic_list.extend([current_value] * num_items_per_label)
        #TODO! aproximacion
        if(len(synthetic_list) != len(df_column_as_list)):
            synthetic_list.extend([current_value] * (len(df_column_as_list) - len(synthetic_list)))
        #now, extrapolate differences between sorted-input-list and synsthetic_list
        df_column_as_list_sorted    =   sorted(df_column_as_list)
        counter_unmatches           =   0
        for i in range(0,N):
            if(df_column_as_list_sorted[i] != synthetic_list[i]):
                counter_unmatches   +=  1
        #upper_bound = g(N,num_different_labels)
        #((K-1)M)-1 K==num_different_labels , M==num theorically perfect distribution's items per label 
        upper_bound                 =   ((num_different_labels-1)*num_items_per_label)-1
        return counter_unmatches/upper_bound
    #---------------------------------------------------------------------------------------------------------------------
