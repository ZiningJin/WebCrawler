import pandas as pd
import re

# --------- CCEUP Util Functions ---------
import pandas as pd
import re

# Assuming df is your DataFrame and 'Content' is the column to process
patterns_abcd = {
    'A': r'\n[aA]\.([\s\S]*?)\n[bB]\.',
    'B': r'\n[bB]\.([\s\S]*?)\n[cC]\.',
    'C': r'\n[cC]\.([\s\S]*?)\n[dD]\.',
    'D': r'\n[dD]\.([\s\S]*?)\n'
}

patterns_e = [
    r'^([\s\S]*?)\n[aA].',
    r'\n[aA]\.([\s\S]*?)\n[bB]\.',
    r'\n[bB]\.([\s\S]*?)\n[cC]\.',
    r'\n[cC]\.([\s\S]*?)\n[dD]\.',
    r'\n[dD]\.([\s\S]*?)\n',
    r'该项目调研结果([\s\S]*)'
]

def cceup_util_extract_abcd(df, column_name, patterns):
    """
    Extracts content based on specified patterns from a DataFrame column and assigns it to new columns.

    :param df: DataFrame to process.
    :param column_name: Name of the column from which to extract content.
    :param patterns: A dictionary where keys are new column names (A, B, C, D)
                     and values are the regex patterns to search for in the specified column.
    """

    def find_matched(content, pattern):
        match = re.findall(pattern, content, re.IGNORECASE)
        return match[0] if match else None

    for new_column_name, pattern in patterns.items():
        df[new_column_name] = df[column_name].apply(lambda x: find_matched(x, pattern))
    
    return df

def cceup_util_extract_e(df, column_name, patterns):
    """
    Replaces content matched by specified patterns in a DataFrame column with an empty string,
    and assigns the cleaned content to a new column named 'E'.

    :param df: DataFrame to process.
    :param column_name: Name of the column to search and replace content.
    :param patterns: A list of regex patterns to search for and replace with ''.
    """

    def replace_matched(content):
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        return content

    df['E'] = df[column_name].apply(replace_matched)
    df['E_block1'] = df['E'].apply(lambda x: re.split('\n\n',x)[0])
    return df


patterns_co = ['(.*局|.*公司)']
patterns_person = ['\n联系人\s*(.*)', '\n姓名\s*(.*)']
patterns_phone = ['\n手机\s*(.*)', '\n电话\s*(.*)', '\n座机\s*(.*)']
patterns_city = ['省(.*?)市', '项目地址：(.*?)市', '项目地址：(.*?)县']

def cceup_extract_info(df, column_name, patterns, default=None):
    """
    Extracts information from a DataFrame column using a list of regex patterns.

    :param df: DataFrame to process.
    :param column_name: Name of the column to extract information from.
    :param patterns: List of regex patterns to apply in order.
    :param default: Default value to return if no pattern matches.
    :return: A Series with extracted information.
    """
    def match_pattern(text):
        for pattern in patterns:
            match = re.findall(pattern, text)
            if match:
                return match[0]
        return default

    return df[column_name].apply(match_pattern)

def cceup_clean_text(df, column_name, pattern, replacement=''):
    """
    Cleans a DataFrame column based on a regex pattern.

    :param df: DataFrame to process.
    :param column_name: Name of the column to clean.
    :param pattern: Regex pattern to match for cleaning.
    :param replacement: Replacement text for matched patterns.
    :return: DataFrame with cleaned column.
    """
    df[column_name] = df[column_name].apply(lambda x: re.sub(pattern, replacement, str(x)) if x is not None else x)
    return df


# Cleaning 'Contact_co' with multiple replacements
co_cases = ['\n','\nE.联系人信息：','E.联系人信息：','\n单位：','\n单位： ','\nE.联系人介绍其他内容：','\nE.其他说明：','E.其它说明：','\nE.特殊说明：','E.特殊说明：',
            '\n企业名称  ','\nE.其它内容：','E.其它内容：','\n企业单位： ','企业单位： ','\nE.联系人介绍其他内容（与工程相关的信息）：','E.联系人介绍其他内容（与工程相关的信息）：',
            'E.联系人介绍其他内容：',' \n[业主单位]','\n[业主单位] ','[业主单位]','[业主单位] ','F.其它说明：','E.备注：']

def cceup_clean_co(x):
    if x is not None:
        for case in co_cases:
            x = x.replace(case, '')
    return x


